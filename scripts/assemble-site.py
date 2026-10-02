#!/usr/bin/env python3
"""Assemble the GitHub Pages site into site/.

Run scripts/build-distribution.py first. Layout:

  site/index.html                              redirects to docs/index.html
  site/docs/                                   the Swagger UI page(s) from docs/
  site/openapi/ecrop.yaml                      the complete specification
  site/openapi/ecrop-<usecase>.yaml            one distribution per business case (from dist/)
  site/openapi/distributions.json              list read by docs/index.html for its API selector
"""
import glob
import json
import os
import shutil

SITE = 'site'


def main():
    if os.path.exists(SITE):
        shutil.rmtree(SITE)
    shutil.copytree('docs', f'{SITE}/docs')
    shutil.copytree('openapi', f'{SITE}/openapi')

    distributions = []
    for path in sorted(glob.glob('dist/ecrop-*.yaml')):
        file = os.path.basename(path)
        shutil.copy(path, f'{SITE}/openapi/{file}')
        distributions.append({'name': file[len('ecrop-'):-len('.yaml')], 'url': file})

    with open(f'{SITE}/openapi/distributions.json', 'w', encoding='utf-8') as f:
        json.dump(distributions, f, indent=2)
        f.write('\n')
    with open(f'{SITE}/index.html', 'w', encoding='utf-8') as f:
        f.write('<meta http-equiv="refresh" content="0; url=docs/index.html">\n')
    print(f'{SITE}/: {len(distributions)} distribution(s)')


if __name__ == '__main__':
    main()
