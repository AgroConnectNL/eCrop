#!/usr/bin/env python3
"""Build a business-case specific distribution of openapi/ecrop.yaml.

Usage: python scripts/build-distribution.py <name> [<name> ...]

<name> is one of the `apis:` entries in redocly.yaml (without the "@v1" suffix),
e.g. contractor-task-planning. Steps:

  1. redocly bundle <name>@v1                 (filter the operations on x-usecases)
  2. drop path items without operations and unused tags, strip the x-usecases markers
  3. redocly bundle --remove-unused-components (prune what no operation references)
  4. apply the example overrides in usecases/<name>/examples.yaml, if present
  5. write dist/<name>.yaml and lint it
"""
import os
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from yamlio import dump, load  # noqa: E402

HTTP_METHODS = {'get', 'put', 'post', 'delete', 'options', 'head', 'patch', 'trace'}
NPX = shutil.which('npx') or 'npx'


def run(*args):
    subprocess.run([NPX, '--yes', '@redocly/cli', *args], check=True)


def strip_key(node, key):
    if isinstance(node, dict):
        node.pop(key, None)
        for v in node.values():
            strip_key(v, key)
    elif isinstance(node, list):
        for v in node:
            strip_key(v, key)


def write(path, spec):
    with open(path, 'w', encoding='utf-8', newline='') as f:
        f.write(dump(spec))


def build(name):
    os.makedirs('dist', exist_ok=True)
    step1, step2 = f'dist/.{name}.1.yaml', f'dist/.{name}.2.yaml'
    out = f'dist/{name}.yaml'

    # 1. filter the operations on x-usecases
    run('bundle', f'{name}@v1', '-o', step1)
    spec = load(step1)

    # 2. drop path items without operations and tags that are no longer used
    for path in [p for p, item in spec['paths'].items() if not HTTP_METHODS & set(item)]:
        del spec['paths'][path]
    used_tags = {t for item in spec['paths'].values()
                 for m, op in item.items() if m in HTTP_METHODS for t in op.get('tags', [])}
    spec['tags'] = [t for t in spec.get('tags', []) if t['name'] in used_tags]
    strip_key(spec, 'x-usecases')
    write(step1, spec)

    # 3. remove the components that nothing references anymore
    run('bundle', step1, '--remove-unused-components', '-o', step2)
    spec = load(step2)
    os.remove(step1)
    os.remove(step2)

    # 4. business-case specific examples
    override = f'usecases/{name}/examples.yaml'
    if os.path.exists(override):
        for section, patches in load(override)['components'].items():
            components = spec['components'].setdefault(section, {})
            for key, value in patches.items():
                if key not in components:
                    sys.exit(f'{override}: components/{section}/{key} is not used by the {name} distribution')
                if section == 'examples':
                    components[key] = value  # replace the whole example
                else:
                    components[key].update(value)  # e.g. replace the `example` of a schema/parameter

    write(out, spec)
    print(f'{out}: {sum(1 for i in spec["paths"].values() for m in i if m in HTTP_METHODS)} operations')
    run('lint', out)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for n in sys.argv[1:]:
        build(n)
