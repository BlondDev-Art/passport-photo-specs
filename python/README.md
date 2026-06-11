# passport-photo-specs (Python)

[![PyPI version](https://img.shields.io/pypi/v/passport-photo-specs.svg)](https://pypi.org/project/passport-photo-specs/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20409880.svg)](https://doi.org/10.5281/zenodo.20409880)

Canonical passport, visa, and ID document photo specifications validated against 15+ official government sources. **100+ countries, 248 document formats.** Python distribution of the [`passport-photo-specs`](https://github.com/BlondDev-Art/passport-photo-specs) dataset.

Useful for:

- Building passport / visa photo tools without re-researching per-country specs
- Validating photo uploads before submitting to a government portal (DS-160, COVA, Sarathi, voters.eci.gov.in, etc.)
- Immigration / visa software that needs correct dimensions and background colors
- ML training corpora for biometric photo compliance
- Research on ICAO 9303 / biometric photo standards across jurisdictions

## Install

```bash
pip install passport-photo-specs
```

## Quick start

```python
from passport_photo_specs import find_document, find_country, countries, documents

# Look up a specific document
italy_visa = find_document("italy-visa-photo")
print(italy_visa["widthMm"], italy_visa["heightMm"], italy_visa["dpi"])
# 35 45 300

# Look up a country (by id or by any of its document slugs)
italy = find_country("italy")
print(italy["name"], len(italy["documents"]))
# Italy 3

# Iterate everything
print(f"Total countries: {len(countries())}")
print(f"Total document formats: {len(documents())}")

# Get the raw dict if you want to walk it yourself
from passport_photo_specs import raw
all_data = raw()
```

## What's in each document spec

```python
{
    "id": "italy-visa",
    "countryId": "italy",
    "name": "Italian Visa",
    "slug": "italy-visa-photo",
    "widthMm": 35,
    "heightMm": 45,
    "widthPx": 413,
    "heightPx": 531,
    "dpi": 300,
    "background": "Plain light grey",
    "bgColor": "#eeeeee",
    "bgColorLabel": "Light grey",
    "requirements": ["Size: 35×45 mm", ...],
    "seoTitle": "...",
    "h1": "...",
    "faq": [{"q": "...", "a": "..."}, ...],
}
```

Source-of-truth: validated against the issuing-authority's published guidance. The full source list is in the parent repository's [README](https://github.com/BlondDev-Art/passport-photo-specs#readme).

## Citation

This dataset is archived on Zenodo with a citable DOI. Use the concept DOI to always resolve to the latest version:

> Elena. (2026). *passport-photo-specs: Open Dataset of Passport, Visa, and ID Photo Specifications for 100+ Countries*. Zenodo. https://doi.org/10.5281/zenodo.20409880

## See also

- npm: [`passport-photo-specs`](https://www.npmjs.com/package/passport-photo-specs) — TypeScript / JavaScript
- GitHub (canonical): [`BlondDev-Art/passport-photo-specs`](https://github.com/BlondDev-Art/passport-photo-specs)
- Zenodo dataset record: [`zenodo.org/records/20409881`](https://zenodo.org/records/20409881)
- Reference implementation: [idphotosnap.com](https://idphotosnap.com) — browser-only passport photo tool that consumes this dataset

## License

MIT. See [LICENSE](https://github.com/BlondDev-Art/passport-photo-specs/blob/main/LICENSE).
