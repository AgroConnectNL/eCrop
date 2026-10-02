"""YAML load/dump helpers for the distribution build.

Loads without implicit date/timestamp conversion (all example dates stay strings)
and dumps in the style used by openapi/ecrop.yaml: indented sequences, and
digit-like strings quoted so that YAML 1.2 parsers (e.g. Redocly) keep them strings.
"""
import re

import yaml


class _Loader(yaml.SafeLoader):
    pass


_Loader.yaml_implicit_resolvers = {
    k: [(tag, rx) for (tag, rx) in v if tag != 'tag:yaml.org,2002:timestamp']
    for k, v in yaml.SafeLoader.yaml_implicit_resolvers.items()
}


class _Dumper(yaml.SafeDumper):
    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, False)


def _str(dumper, s):
    if re.fullmatch(r'[-+]?[0-9][0-9_.,:eE+-]*', s):
        return dumper.represent_scalar('tag:yaml.org,2002:str', s, style="'")
    return dumper.represent_scalar('tag:yaml.org,2002:str', s)


_Dumper.add_representer(str, _str)


def load(path):
    with open(path, encoding='utf-8') as f:
        return yaml.load(f, Loader=_Loader)


def dump(data):
    return yaml.dump(data, Dumper=_Dumper, sort_keys=False, allow_unicode=True,
                     width=10000, default_flow_style=False, indent=2)
