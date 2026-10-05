"""Consistency checks on the plot/feature examples of a specification or distribution.

The examples of the plot business objects, the plot-geometry (Feature) responses and the
plotSchemeId/plotId query parameters are written (and overridden per business case) separately,
but they describe the same plots. This checks that they agree:

  1. the `plot-features` backlink of every plot example queries that plot's own scheme and id;
  2. when the Feature examples are part of the specification: every backlinked plot, and the
     examples of the plotSchemeId/plotId query parameters, refer to a plot that a Feature
     example refers to (properties.plotId);
  3. the `plot` link of every Feature example contains the id of the plot in its own properties.plotId.

Usage: python scripts/check_consistency.py [<file.yaml> ...]   (default: openapi/ecrop.yaml)
"""
import os
import sys
from urllib.parse import parse_qs, urlparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from yamlio import load  # noqa: E402

REL_FEATURES = 'https://ecrop.agroconnect.nl/rel/plot-features'
REL_PLOT = 'https://ecrop.agroconnect.nl/rel/plot'


def walk(node):
    """yield every dict in a nested structure"""
    if isinstance(node, dict):
        yield node
        for v in node.values():
            yield from walk(v)
    elif isinstance(node, list):
        for v in node:
            yield from walk(v)


def pid(obj):
    """(schemeId, content) of an idType object, or None"""
    if isinstance(obj, dict) and 'content' in obj and 'schemeId' in obj:
        return obj['schemeId'], obj['content']
    return None


def check(spec, label):
    errors = []
    components = spec.get('components', {})
    examples = {k: v.get('value') for k, v in components.get('examples', {}).items()}

    feature_plots = set()   # plot ids that a Feature example refers to
    for name, value in examples.items():
        for d in walk(value):
            props = d.get('properties')
            if isinstance(props, dict) and pid(props.get('plotId')):
                plot = pid(props['plotId'])
                feature_plots.add(plot)
                # 3. the Feature's link back to the plot
                for link in d.get('links', []) or []:
                    if link.get('rel') == REL_PLOT and plot[1] not in link['href']:
                        errors.append(f'example {name}: feature link rel=plot ({link["href"]}) does not contain the '
                                      f'id {plot[1]} of its properties.plotId')

    backlinked = set()
    for name, value in examples.items():
        for d in walk(value):
            if pid(d.get('id')) and isinstance(d.get('links'), list):
                for link in d['links']:
                    if link.get('rel') != REL_FEATURES:
                        continue
                    own = pid(d['id'])
                    backlinked.add(own)
                    q = parse_qs(urlparse(link['href']).query)
                    got = (q.get('plotSchemeId', [None])[0], q.get('plotId', [None])[0])
                    if got != own:  # 1. the backlink queries the plot's own id
                        errors.append(f'example {name}: plot {own[0]}/{own[1]} has a plot-features link that queries '
                                      f'{got[0]}/{got[1]}')

    if feature_plots:  # 2. only when the Feature examples are part of this specification
        for own in sorted(backlinked - feature_plots):
            errors.append(f'plot {own[0]}/{own[1]} has a plot-features link, but no Feature example refers to it')
        params = components.get('parameters', {})
        if 'plotSchemeIdQuery' in params and 'plotIdQuery' in params:
            q = (params['plotSchemeIdQuery'].get('example'), params['plotIdQuery'].get('example'))
            if q not in feature_plots:
                errors.append(f'query parameter examples plotSchemeId/plotId ({q[0]}/{q[1]}) match no plot that a '
                              f'Feature example refers to ({", ".join("/".join(p) for p in sorted(feature_plots))})')

    if errors:
        sys.exit(f'{label}: inconsistent plot/feature examples:\n  - ' + '\n  - '.join(errors))
    print(f'{label}: plot/feature examples are consistent')


if __name__ == '__main__':
    for path in sys.argv[1:] or ['openapi/ecrop.yaml']:
        check(load(path), path)
