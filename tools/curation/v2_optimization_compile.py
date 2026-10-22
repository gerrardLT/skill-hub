"""Compile isolated optimization candidate using the existing revision compiler."""
from pathlib import Path
import json
import v2_revision_compile as compiler

CONTROL = Path('curation/v2/optimization-1.1.0')
OUTPUT = Path('evals/candidates/capability-compiler-v2/optimization-1.1.0')


def main():
    compiler.REV = CONTROL
    compiler.OUT = OUTPUT
    print(json.dumps(compiler.compile_all(Path('.')), sort_keys=True))


if __name__ == '__main__':
    main()
