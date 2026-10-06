#!/usr/bin/env python3
"""Print the CHANGELOG.md section that belongs to a release tag, as the body of its GitHub release.

Usage: python scripts/release-notes.py <tag>

  v1.1.0        -> the section "## [1.1.0]"
  v1.1.0-rc.1   -> the section "## [1.1.0-rc.1]" if it exists, otherwise the section "## [1.1.0]",
                   preceded by a line saying that this is a pre-release of 1.1.0

Exits with status 1 (and a message on stderr) when there is no section for the tag.
"""
import re
import sys


def sections(text):
    """{version: body} for every "## [version]" heading of a Keep a Changelog file"""
    parts = re.split(r'^## \[([^\]]+)\][^\n]*\n', text, flags=re.M)
    return {parts[i]: parts[i + 1].strip('\n') for i in range(1, len(parts), 2)}


def release_notes(tag, text):
    version = tag[1:] if tag.startswith('v') else tag
    found = sections(text)
    if version in found:
        return found[version]
    base = version.split('-', 1)[0]
    if base != version and base in found:
        return f'Pre-release `{tag}` of version {base}.\n\n{found[base]}'
    return None


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    with open('CHANGELOG.md', encoding='utf-8') as f:
        notes = release_notes(sys.argv[1], f.read().replace('\r\n', '\n'))
    if not notes:
        sys.exit(f'CHANGELOG.md has no section for {sys.argv[1]}')
    sys.stdout.reconfigure(encoding='utf-8')
    print(notes)
