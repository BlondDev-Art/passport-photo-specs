#!/usr/bin/env python3
"""
Example: load passport-photo-specs in Python.

Two ways to use:
  1. Local file (clone this repo)
  2. Remote HTTP fetch from idphotosnap.com/api/specs

Run: python3 example.py
"""

import json
import urllib.request


def load_local():
    """Load from local specs/specs.json (clone this repo first)."""
    with open('../../specs/specs.json') as f:
        return json.load(f)


def load_remote(country=None):
    """Load from public API at idphotosnap.com."""
    url = 'https://idphotosnap.com/api/specs?format=raw'
    if country:
        url += f'&country={country}'
    with urllib.request.urlopen(url, timeout=10) as resp:
        return json.load(resp)


def find_document(data, slug):
    """Look up a document by slug across all countries."""
    for country in data['countries']:
        for doc in country['documents']:
            if doc['slug'] == slug:
                return doc, country
    return None, None


def main():
    # Example 1: load remote, filter to India
    print('=== Indian passport photo specs (from remote API) ===')
    data = load_remote(country='india')
    for country in data['countries']:
        for doc in country['documents']:
            print(f"  {doc['name']:20} {doc['widthMm']}x{doc['heightMm']}mm  bg={doc['bgColorLabel']}")

    # Example 2: look up Chinese visa
    print('\n=== China visa lookup ===')
    data = load_remote()
    doc, country = find_document(data, 'china-visa-photo')
    if doc:
        print(f"  {country['name']} {doc['name']}: {doc['widthMm']}x{doc['heightMm']}mm")
        print(f"  Pixel dims @ {doc['dpi']} DPI: {doc['widthPx']}x{doc['heightPx']}")
        print(f"  Background: {doc['background']}")
        print(f"  Requirements:")
        for req in doc['requirements'][:5]:
            print(f"    - {req}")

    # Example 3: validate an arbitrary photo dimension matches a spec
    print('\n=== Validate dimensions ===')
    test_width_mm, test_height_mm = 35, 45
    matches = [
        (c['name'], d['name'])
        for c in data['countries']
        for d in c['documents']
        if d['widthMm'] == test_width_mm and d['heightMm'] == test_height_mm
    ]
    print(f"  {test_width_mm}x{test_height_mm}mm matches {len(matches)} document types:")
    for country_name, doc_name in matches[:10]:
        print(f"    - {country_name} {doc_name}")
    if len(matches) > 10:
        print(f"    ... and {len(matches) - 10} more")


if __name__ == '__main__':
    main()
