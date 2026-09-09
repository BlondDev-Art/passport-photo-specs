"""
passport-photo-specs
====================

Canonical passport, visa, and ID document photo specifications validated against
15+ official government sources. 100+ countries, 248 document formats.

Quick start
-----------

    from passport_photo_specs import find_document, find_country, countries, documents

    italy_visa = find_document("italy-visa-photo")
    # {'widthMm': 35, 'heightMm': 45, 'widthPx': 413, 'heightPx': 531,
    #  'dpi': 300, 'background': 'Plain light grey', ...}

    italy = find_country("italy")
    # {'id': 'italy', 'name': 'Italy', 'documents': [...]}

    print(f"Total countries: {len(countries())}")  # 100+
    print(f"Total document formats: {len(documents())}")  # 248

Citation
--------

Dataset DOI: https://doi.org/10.5281/zenodo.20409880

License: MIT
"""

from __future__ import annotations

import json
from importlib.resources import files
from typing import Any, Dict, List, Optional

__version__ = "1.4.0"
__all__ = [
    "countries",
    "documents",
    "find_country",
    "find_document",
    "raw",
]


def _load() -> Dict[str, Any]:
    data_text = files(__package__).joinpath("specs.json").read_text(encoding="utf-8")
    return json.loads(data_text)


_DATA = _load()


def raw() -> Dict[str, Any]:
    """Return the full raw specs.json contents as a dict."""
    return _DATA


def countries() -> List[Dict[str, Any]]:
    """Return the list of all country records.

    Each record has at minimum `id`, `name`, and `documents` keys.
    """
    return list(_DATA.get("countries", []))


def documents() -> List[Dict[str, Any]]:
    """Return a flat list of every document spec across every country.

    Each document inherits a `countryId` reference back to its country.
    """
    out: List[Dict[str, Any]] = []
    for country in _DATA.get("countries", []):
        for doc in country.get("documents", []):
            out.append(doc)
    return out


def find_country(country_id_or_slug: str) -> Optional[Dict[str, Any]]:
    """Look up a country by its id (e.g. 'italy') or by a document slug
    that belongs to it. Returns None if not found.
    """
    needle = country_id_or_slug.lower()
    for country in _DATA.get("countries", []):
        if country.get("id", "").lower() == needle:
            return country
        for doc in country.get("documents", []):
            if doc.get("slug", "").lower() == needle:
                return country
    return None


def find_document(slug: str) -> Optional[Dict[str, Any]]:
    """Look up a document spec by its slug (e.g. 'italy-visa-photo').

    Returns None if not found.
    """
    needle = slug.lower()
    for country in _DATA.get("countries", []):
        for doc in country.get("documents", []):
            if doc.get("slug", "").lower() == needle:
                return doc
    return None
