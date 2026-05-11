"""
passport_photo_specs - canonical passport photo specifications

Loads specs.json into typed dicts. Provides lookup helpers.

Usage:
    from passport_photo_specs import find_document, find_country, countries

    italy_visa = find_document('italy-visa-photo')
    print(italy_visa['widthMm'], italy_visa['heightMm'])  # 35 45

    india = find_country('india')
    for doc in india['documents']:
        print(doc['name'], doc['widthMm'], 'x', doc['heightMm'], 'mm')
"""

import json
import os
from typing import Optional

_SPECS_PATH = os.path.join(os.path.dirname(__file__), 'specs.json')

with open(_SPECS_PATH, encoding='utf-8') as _f:
    _data = json.load(_f)

meta: dict = _data['meta']
countries: list[dict] = _data['countries']

all_documents: list[dict] = [d for c in countries for d in c['documents']]
countries_by_id: dict[str, dict] = {c['id']: c for c in countries}
documents_by_slug: dict[str, dict] = {d['slug']: d for d in all_documents}


def find_country(country_id: str) -> Optional[dict]:
    """Look up a country by id, e.g. 'italy'."""
    return countries_by_id.get(country_id)


def find_document(slug: str) -> Optional[dict]:
    """Look up a document by slug, e.g. 'italy-visa-photo'."""
    return documents_by_slug.get(slug)


def documents_for_country(country_id: str) -> list[dict]:
    """All documents for a given country id."""
    country = countries_by_id.get(country_id)
    return country['documents'] if country else []


__all__ = [
    'meta',
    'countries',
    'all_documents',
    'countries_by_id',
    'documents_by_slug',
    'find_country',
    'find_document',
    'documents_for_country',
]
