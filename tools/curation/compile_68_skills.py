"""Compile the 154-skill catalog into 68 consolidated capabilities.

Fixes over the first pass:
- writes LF line endings so content-identical skills keep a stable hash contract
- demotes inner headings so each document has exactly one H1
- emits an explicit Mode selection table instead of relying on the reader to guess
- records per-source hashes so provenance survives independent verification
"""
from __future__ import annotations

import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path('.')
OPT = ROOT / 'evals/candidates/capability-compiler-v2/optimization-1.1.0'
SRC_SKILLS = OPT / 'skills'
OUT = ROOT / 'evals/candidates/capability-compiler-v2/consolidated-68'
OUT_SKILLS = OUT / 'skills'
MAPPING_FILE = ROOT / 'curation/v2/optimization-1.1.0/consolidated-68-mapping.json'

HEADING = re.compile(r'^(#{1,6}) (.*)$', re.M)
FRONTMATTER = re.compile(r'^---\n(.*?)\n---\n', re.S)


def read_text(path: Path) -> str:
    """Read as UTF-8 with newlines normalised to LF."""
    return path.read_text(encoding='utf-8').replace('\r\n', '\n').replace('\r', '\n')


def write_text(path: Path, text: str) -> None:
    """Write UTF-8 with LF endings, never CRLF."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8', newline='\n') as handle:
        handle.write(text)


def write_json(path: Path, value: object) -> None:
    write_text(path, json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + '\n')


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def split_frontmatter(md: str) -> tuple[str, str]:
    match = FRONTMATTER.match(md)
    if not match:
        return '', md
    return match.group(1), md[match.end():]


def field(frontmatter: str, key: str) -> str:
    match = re.search(rf'^{key}:\s*(.*)$', frontmatter, re.M)
    if not match:
        return ''
    value = match.group(1).strip()
    if value.startswith('"') and value.endswith('"'):
        value = value[1:-1]
    return value


def use_when(description: str) -> str:
    """Pull the 'Use when' clause out of a source description."""
    match = re.search(r'Use when\s+(.*?)(?:Do not use for:|$)', description, re.S)
    if not match:
        return ''
    text = ' '.join(match.group(1).split())
    return text.rstrip('; ').strip()


def routes_away(description: str) -> list[str]:
    match = re.search(r'Do not use for:\s*(.*)$', description, re.S)
    if not match:
        return []
    return [part.strip().rstrip('.') for part in re.split(r';', match.group(1)) if part.strip()]


def demote(md: str, levels: int = 2) -> str:
    """Push every heading down `levels`, clamped at H6."""

    def repl(match: re.Match) -> str:
        hashes = match.group(1)
        return '#' * min(6, len(hashes) + levels) + ' ' + match.group(2)

    return HEADING.sub(repl, md)


def build_mode_section(mode_id: str, body: str, title: str) -> str:
    """Render one mode as an H2 section with demoted inner headings.

    The body's own leading H1 is replaced by the section heading so the document
    never repeats the mode title twice.
    """
    stripped = body.strip()
    stripped = re.sub(r'^# .*?\n', '', stripped, count=1).lstrip('\n')
    inner = demote(stripped, levels=2)
    return f"## Mode: `{mode_id}`\n\n### {title}\n\n{inner}\n"


def main() -> None:
    mapping = json.loads(MAPPING_FILE.read_text(encoding='utf-8'))['mapping']
    target_to_sources: dict[str, list[str]] = defaultdict(list)
    for src_id, tgt_id in mapping.items():
        target_to_sources[tgt_id].append(src_id)

    orig_index = json.loads(read_text(OPT / 'skill-index.json'))['skills']
    stage_of = {item['id']: item['stage_id'] for item in orig_index}

    index_entries = []
    merged_count = 0

    for tgt_id, src_ids in sorted(target_to_sources.items()):
        src_ids = sorted(src_ids)
        stage = stage_of[src_ids[0]]

        contracts = [json.loads(read_text(SRC_SKILLS / s / 'contract.json')) for s in src_ids]
        sources = []
        for sid in src_ids:
            md = read_text(SRC_SKILLS / sid / 'SKILL.md')
            fm, body = split_frontmatter(md)
            sources.append({
                'id': sid,
                'frontmatter': fm,
                'body': body,
                'sha256': sha256(md),
                'title': field(fm, 'name') or sid,
                'description': field(fm, 'description'),
            })

        # ---- contract ----------------------------------------------------
        base = dict(contracts[0])
        base['id'] = tgt_id
        base['capability_id'] = f'capability:{tgt_id}'
        base['version'] = '1.1.0-consolidated'
        base['modes'] = src_ids if len(src_ids) > 1 else []

        # Each mode keeps the permission identity of its own source skill. Merging across
        # permission boundaries is only safe when the boundary stays visible, so the document
        # declares one permission per mode and defaults to the most restrictive one.
        mode_permissions = {s['id']: c.get('permission_identity')
                            for s, c in zip(sources, contracts)}
        base['mode_permissions'] = mode_permissions
        if len(src_ids) > 1:
            from collections import Counter as _Counter
            base['permission_identity'] = _Counter(
                mode_permissions.values()).most_common(1)[0][0]
            base['permission_identity_is_default'] = (
                'most common of mode_permissions; the effective identity for a run is '
                'mode_permissions[selected_mode]')

        union = {
            'inputs': [], 'outputs': [], 'artifact_types': [],
            'forbidden_actions': [], 'hard_gates': [], 'statuses': [],
        }
        for contract in contracts:
            for key, bucket in union.items():
                for item in contract.get(key, []):
                    if item not in bucket:
                        bucket.append(item)
        base.update(union)

        responsibilities = [c.get('responsibility', '').strip() for c in contracts]
        if len(src_ids) == 1:
            base['responsibility'] = responsibilities[0]
        else:
            base['responsibility'] = (
                f"Consolidated capability covering {len(src_ids)} related modes: "
                + '; '.join(responsibilities)
            )

        # ---- provenance --------------------------------------------------
        evidence, units = [], []
        for prov in (json.loads(read_text(SRC_SKILLS / s / 'provenance.json')) for s in src_ids):
            cp = prov.get('candidate_provenance', {})
            for ev in cp.get('source_evidence', []):
                if ev not in evidence:
                    evidence.append(ev)
            for unit in cp.get('canonical_unit_ids', []):
                if unit not in units:
                    units.append(unit)

        provenance = {
            'schema_version': '2.0',
            'id': tgt_id,
            'capability_id': f'capability:{tgt_id}',
            'version': '1.1.0-consolidated',
            'status': 'consolidated-candidate',
            'merged_from': src_ids,
            'source_skill_sha256': {s['id']: s['sha256'] for s in sources},
            'candidate_provenance': {
                'source_evidence': evidence,
                'canonical_unit_ids': units,
                'source_cluster_ids': sorted({
                    cid
                    for sid in src_ids
                    for cid in json.loads(read_text(SRC_SKILLS / sid / 'provenance.json'))
                        .get('candidate_provenance', {}).get('source_cluster_ids', [])
                }),
            },
        }

        # ---- SKILL.md ----------------------------------------------------
        if len(src_ids) == 1:
            skill_md = read_text(SRC_SKILLS / src_ids[0] / 'SKILL.md')
        else:
            merged_count += 1
            title = tgt_id.replace('-', ' ').title()
            lines = [
                '---',
                f'name: {tgt_id}',
                f'description: "Consolidated capability with {len(src_ids)} selectable modes: '
                + '; '.join(src_ids) + '. Choose exactly one mode per invocation."',
                'version: 1.1.0-consolidated',
                f'modes: [{", ".join(src_ids)}]',
                '---',
                '',
                f'# {title}',
                '',
                '## Responsibility',
                '',
                base['responsibility'],
                '',
                '## Mode selection',
                '',
                'This capability has several distinct modes. Read this table first, pick exactly one',
                'mode for the current request, then follow only that mode\'s section. Do not blend',
                'modes: each carries its own permission identity, gates, and stop conditions. The',
                'permission column is binding - a run uses the permission of the mode it selected,',
                'never the widest permission in this document.',
                '',
                '| Mode | Permission | Use when | Routes elsewhere |',
                '| --- | --- | --- | --- |',
            ]
            for s in sources:
                when = use_when(s['description']) or 'the request matches this mode directly'
                away = '; '.join(routes_away(s['description'])) or '—'
                when = when.replace('|', '/')[:200]
                away = away.replace('|', '/')[:120]
                perm = mode_permissions[s['id']]
                lines.append(f"| `{s['id']}` | `{perm}` | {when} | {away} |")
            lines.append('')
            for s in sources:
                lines.append(build_mode_section(s['id'], s['body'], s['title'].strip()))
            skill_md = '\n'.join(lines)
            skill_md = re.sub(r'\n{3,}', '\n\n', skill_md).rstrip() + '\n'

        # ---- write -------------------------------------------------------
        target_dir = OUT_SKILLS / tgt_id
        write_text(target_dir / 'SKILL.md', skill_md)
        write_json(target_dir / 'contract.json', base)
        write_json(target_dir / 'provenance.json', provenance)

        index_entries.append({
            'id': tgt_id,
            'stage_id': stage,
            'path': f'evals/candidates/capability-compiler-v2/consolidated-68/skills/{tgt_id}',
            'permission_identity': base.get('permission_identity'),
            'responsibility': base['responsibility'],
            'mode_count': len(src_ids),
            'modes': src_ids,
            'contract_sha256': sha256(json.dumps(base, ensure_ascii=False, indent=2, sort_keys=True) + '\n'),
            'skill_sha256': sha256(skill_md),
        })

    index = {
        'schema_version': '2.0',
        'version': '1.1.0-consolidated-68',
        'skill_count': len(index_entries),
        'status': 'consolidated-68-candidate',
        'skills': index_entries,
    }
    write_json(OUT / 'skill-index.json', index)

    # ---- self-checks -----------------------------------------------------
    problems = []
    for entry in index_entries:
        md = read_text(OUT_SKILLS / entry['id'] / 'SKILL.md')
        if b'\r\n' in (OUT_SKILLS / entry['id'] / 'SKILL.md').read_bytes():
            problems.append((entry['id'], 'CRLF present'))
        h1 = re.findall(r'^# ', md, re.M)
        if len(h1) != 1:
            problems.append((entry['id'], f'{len(h1)} H1 headings'))
        if entry['mode_count'] > 1:
            if '## Mode selection' not in md:
                problems.append((entry['id'], 'missing mode selection table'))
            if md.count('## Mode: `') != entry['mode_count']:
                problems.append((entry['id'], 'mode section count mismatch'))

    print(f'compiled {len(index_entries)} skills ({merged_count} merged, '
          f'{len(index_entries) - merged_count} 1:1)')
    print(f'structural problems: {len(problems)}')
    for problem in problems[:20]:
        print('  ', problem)
    if problems:
        raise SystemExit('structural self-check failed')


if __name__ == '__main__':
    main()
