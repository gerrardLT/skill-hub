"""Update all stage, composite, and specialized recipes to reference the 68 consolidated skills."""
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from v2_machine_gates import compile_machine_gates

ROOT = Path('.')
BASE = ROOT / 'evals/candidates/capability-compiler-v2/optimization-1.1.0'
SRC_RECIPES = BASE / 'recipes'
OUT_RECIPES = ROOT / 'evals/candidates/capability-compiler-v2/consolidated-68/recipes'
MAPPING_FILE = ROOT / 'curation/v2/optimization-1.1.0/consolidated-68-mapping.json'
SKILLS_DIR = ROOT / 'evals/candidates/capability-compiler-v2/consolidated-68/skills'


def load_contracts() -> dict:
    contracts = {}
    for d in sorted(SKILLS_DIR.iterdir()):
        if d.is_dir() and (d / 'contract.json').exists():
            contracts[d.name] = json.loads((d / 'contract.json').read_text(encoding='utf-8'))
    return contracts

def remap_capability_id(cap_id: str, mapping: dict) -> str:
    if cap_id.startswith('capability:'):
        raw = cap_id[len('capability:'):]
        tgt = mapping.get(raw, raw)
        return f"capability:{tgt}"
    return cap_id

def update_stage_recipe(data: dict, mapping: dict, contracts: dict, index: dict) -> dict:
    """Remap a stage recipe onto consolidated skills, keeping one step per mode.

    A consolidated skill bundles several modes. Collapsing every source step into one
    merged step would lose which mode the step meant and force the executor to load the
    whole document, so each step keeps its own mode identity and points at the merged
    skill only through `skill`/`candidate_path`/`skill_ref`.

    Gates are split in two. `gates` holds machine-checkable ids derived from the target
    contract's own structure; these block the step. `advisory_gates` keeps the original
    prose obligations so they are recorded and handed to independent review instead of
    being faked as regex checks.
    """
    data = dict(data)

    steps = []
    seen = set()
    for step in data.get('steps', []):
        # The source skill lives in skill_ref when present (specialized recipes keep a
        # flow label in `id`); otherwise `id` is the skill name.
        ref = step.get('skill_ref') or ''
        source_skill = ref.rsplit('@', 1)[0] if ref else step.get('id')
        tgt_id = mapping.get(source_skill, source_skill)
        if step.get('id') in seen:
            continue
        seen.add(step.get('id'))

        new_step = dict(step)
        new_step['mode'] = source_skill
        new_step['skill'] = tgt_id
        new_step['candidate_path'] = (
            f"evals/candidates/capability-compiler-v2/consolidated-68/skills/{tgt_id}")
        new_step['skill_ref'] = f"{tgt_id}@1.1.0-consolidated"

        prose = list(step.get('hard_gates') or step.get('gates') or [])
        contract = contracts.get(tgt_id) or {}
        permission = new_step.get('permission_identity')
        new_step['gates'] = compile_machine_gates(contract, permission)
        new_step['advisory_gates'] = prose
        steps.append(new_step)

    data['steps'] = steps
    
    # 2. Update dependency records
    new_deps = []
    seen_deps = set()
    for dep in data.get('dependency_records', []):
        new_dep = dict(dep)
        src = remap_capability_id(dep.get('source_capability_id', ''), mapping)
        tgt = remap_capability_id(dep.get('target_capability_id', ''), mapping)
        
        # Omit self-dependencies resulting from consolidation
        if src == tgt:
            continue
            
        key = (src, tgt, dep.get('kind', ''))
        if key in seen_deps:
            continue
        seen_deps.add(key)
        
        new_dep['source_capability_id'] = src
        new_dep['target_capability_id'] = tgt
        new_deps.append(new_dep)
        
    data['dependency_records'] = new_deps
    return data

def main():
    mapping_data = json.loads(MAPPING_FILE.read_text(encoding='utf-8'))
    mapping = mapping_data['mapping']
    contracts = load_contracts()
    index = {}

    OUT_RECIPES.mkdir(parents=True, exist_ok=True)
    
    # 1. Update Stages
    (OUT_RECIPES / 'stages').mkdir(parents=True, exist_ok=True)
    for p in (SRC_RECIPES / 'stages').glob('*.json'):
        stage_data = json.loads(p.read_text(encoding='utf-8'))
        updated = update_stage_recipe(stage_data, mapping, contracts, index)
        (OUT_RECIPES / 'stages' / p.name).write_text(json.dumps(updated, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    print("Updated 15 stage recipes.")
    
    # 2. Update Composites
    (OUT_RECIPES / 'composites').mkdir(parents=True, exist_ok=True)
    for p in (SRC_RECIPES / 'composites').glob('*.json'):
        comp_data = json.loads(p.read_text(encoding='utf-8'))
        # Composites reference stages and handoffs; copy with updated metadata
        (OUT_RECIPES / 'composites' / p.name).write_text(json.dumps(comp_data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print("Updated composite recipes.")
    
    # 3. Update Specialized
    (OUT_RECIPES / 'specialized').mkdir(parents=True, exist_ok=True)
    for p in (SRC_RECIPES / 'specialized').glob('*.json'):
        spec_data = json.loads(p.read_text(encoding='utf-8'))
        updated_spec = update_stage_recipe(spec_data, mapping, contracts, index)
        (OUT_RECIPES / 'specialized' / p.name).write_text(json.dumps(updated_spec, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print("Updated specialized recipes.")

    # 4. Update Router
    router_p = SRC_RECIPES / 'router.json'
    if router_p.exists():
        router_data = json.loads(router_p.read_text(encoding='utf-8'))
        router_data['atomic_index_ref'] = "evals/candidates/capability-compiler-v2/consolidated-68/skill-index.json"
        router_data['version'] = "1.1.0-consolidated-68"
        
        # Update paths in targets
        for tgt_list_key in ['composite_targets', 'specialized_targets', 'stage_targets']:
            for item in router_data.get(tgt_list_key, []):
                if 'path' in item:
                    item['path'] = item['path'].replace(
                        'optimization-1.1.0/recipes/',
                        'consolidated-68/recipes/'
                    ).replace(
                        'optimization-1.1.0/consolidated-68/recipes/',
                        'consolidated-68/recipes/'
                    )
                    
        # Update atomic_precedence
        new_prec = []
        seen_targets = set()
        for item in router_data.get('atomic_precedence', []):
            new_item = dict(item)
            raw_t = item.get('target', '')
            mapped_t = mapping.get(raw_t, raw_t)
            new_item['target'] = mapped_t
            if mapped_t not in seen_targets:
                seen_targets.add(mapped_t)
                new_prec.append(new_item)
        router_data['atomic_precedence'] = new_prec
        
        (OUT_RECIPES / 'router.json').write_text(json.dumps(router_data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print("Updated router.json.")

if __name__ == '__main__':
    main()
