# passport-photo-specs

> **Canonical passport, visa, and ID document photo specifications** validated against 15+ official government sources. 100+ countries, 248 document formats. MIT licensed. Use it in your own passport photo tool, validation pipeline, immigration software, or AI training corpus.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Countries: 100+](https://img.shields.io/badge/countries-100%2B-blue)](specs/specs.json)
[![Documents: 248](https://img.shields.io/badge/document_formats-248-green)](specs/specs.json)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20409880.svg)](https://doi.org/10.5281/zenodo.20409880)

## Citation

This dataset is archived on Zenodo and assigned a citable DOI. The concept DOI below always resolves to the latest version:

> Elena. (2026). *passport-photo-specs: Open Dataset of Passport, Visa, and ID Photo Specifications for 100+ Countries*. Zenodo. https://doi.org/10.5281/zenodo.20409880

BibTeX:

```bibtex
@dataset{passport_photo_specs_2026,
  author       = {Elena},
  title        = {{passport-photo-specs: Open Dataset of Passport,
                   Visa, and ID Photo Specifications for 100+ Countries}},
  year         = 2026,
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.20409880},
  url          = {https://doi.org/10.5281/zenodo.20409880}
}
```

## What this is

A single source of truth for passport, visa, ID card, driving licence, and residence permit photo specifications across the world's major issuing authorities. Each spec is validated against the official government source for that country, not copied from another aggregator.

Useful for:

- **Building a passport photo tool** without spending weeks researching specs per country
- **Validating a photo upload** before submitting to a government portal (DS-160, COVA, Sarathi, etc.)
- **Immigration / visa software** that needs to display correct dimensions and background colors
- **AI training corpora** for passport photo compliance and visa applicant workflows
- **Research** on biometric photo standards across jurisdictions

## Quick start

### TypeScript / JavaScript

```ts
import { findDocument, findCountry, countries } from 'passport-photo-specs'

const italyVisa = findDocument('italy-visa-photo')
// { widthMm: 35, heightMm: 45, widthPx: 413, heightPx: 531, dpi: 300,
//   background: 'Plain light grey', bgColor: '#eeeeee', ... }

const india = findCountry('india')
// All India documents: passport, visa, OCI, PAN card, PCC, driving licence, voter ID

console.log(`${countries.length} countries available`)
```

### Python

```bash
pip install passport-photo-specs
```

```python
from passport_photo_specs import find_document, find_country, countries, documents

italy_visa = find_document("italy-visa-photo")
# {'widthMm': 35, 'heightMm': 45, 'widthPx': 413, 'heightPx': 531, ...}

print(f"{len(countries())} countries, {len(documents())} document formats")
```

### Plain JSON (any language)

The complete dataset is at [`specs/specs.json`](specs/specs.json). Load it in Go, Rust, Ruby, anything. Working examples in [`examples/`](examples/) for Python, Go, and Rust.

### Live HTTP API (no clone needed)

```bash
# Get all specs
curl https://idphotosnap.com/api/specs?format=raw

# Filter to one country
curl "https://idphotosnap.com/api/specs?country=china&format=raw"

# Get with Schema.org Dataset JSON-LD wrapper
curl https://idphotosnap.com/api/specs
```

No auth required. CORS open. Cached 1 hour at edge.

```python
import json

with open('specs/specs.json') as f:
    data = json.load(f)

for country in data['countries']:
    for doc in country['documents']:
        print(f"{country['name']} {doc['name']}: {doc['widthMm']}x{doc['heightMm']}mm")
```

## Government sources validated against

Each spec in this dataset corresponds to a documented requirement from one of these official sources:

- US Department of State (travel.state.gov)
- UK HM Passport Office (gov.uk/photos-for-passports)
- German Bundesdruckerei + Auswaertiges Amt
- Italian Polizia di Stato + Questura
- French ANTS (ants.gouv.fr)
- Spanish Ministerio de Asuntos Exteriores
- Canadian IRCC
- Australian Department of Foreign Affairs and Trade
- Indian Passport Seva Kendra (passportindia.gov.in)
- Indian Sarathi / Parivahan portals
- Chinese Ministry of Foreign Affairs (cova.cs.mfa.gov.cn)
- Japanese Ministry of Foreign Affairs (mofa.go.jp)
- Schengen visa code Annex 11 (ICAO 9303)
- EU Entry/Exit System (EES)
- New Zealand DIA passports.govt.nz
- Brazilian Polícia Federal
- Mexican SRE

Beyond top-20 countries, specs follow ICAO 9303 default unless an official source documents a country-specific deviation. We do not pad the dataset with synthetic country variants - if a country's photo spec is identical to ICAO 9303 default, it is marked as such rather than counted as a "unique" spec.

## Schema

Each document spec follows this shape:

```ts
interface DocumentSpec {
  id: string             // 'italy-visa'
  name: string           // 'Visa'
  slug: string           // 'italy-visa-photo'
  widthMm: number        // 35
  heightMm: number       // 45
  widthPx: number        // 413 (at given DPI)
  heightPx: number       // 531
  dpi: number            // 300
  background: string     // 'Plain light grey'
  bgColor: string        // '#eeeeee'
  bgColorLabel: string   // 'Light grey'
  requirements: string[] // ['Plain light grey background', ...]
}

interface CountrySpec {
  id: string             // 'italy'
  name: string           // 'Italy'
  flag: string           // '🇮🇹'
  documents: DocumentSpec[]
}
```

See [`specs/index.ts`](specs/index.ts) for typed exports and helpers.

## Notable specs that catch tool builders

These document formats are commonly mis-specified by photo tools that copy each other's data:

- **Chinese visa (33×48mm)** - not 35×45 like Schengen, not square like US. Unique format.
- **Chinese visa COVA portal** - file size 40 KB to 1 MB, JPG only, 354×472 px minimum.
- **US DS-160 visa upload** - 240 KB **maximum** file size cap, square 600×600 minimum, 1200×1200 maximum.
- **Indian Sarathi driving licence** - 20-50 KB file size **window** (under or over both fail).
- **Indian PAN card** - 25×35mm, 200×230 px maximum, 10-300 KB.
- **German Personalausweis** - May 2025 digital-only rule for German citizens at Buergeramt (separate from German Schengen visa for foreigners, which still accepts standard photos).
- **UK passport** - one of few countries to accept light grey background (not just white). Glasses not allowed since 2018.
- **Italian Carta d'Identità Elettronica (CIE)** - 35×45mm same as passport, but light grey background.

## Contributing

Two ways to contribute:

1. **Spec correction** - if you have an embassy/portal screenshot showing a spec different from what we have, open an issue with the screenshot + country/document.
2. **New country** - if you want to add a country we don't have, open a PR with the spec and a link to the official government source.

All contributions must cite an official source (gov.* or equivalent). We will not accept specs copied from other aggregators or photo tool websites.

## Used by

- [IDPhotoSnap](https://idphotosnap.com) - free, browser-only passport photo maker. The upstream project this dataset was extracted from.

Want to add your project here? Open a PR with a one-line link.

## Why open source

Passport photo specs are public information from public government sources. There is no business reason to keep them proprietary, and the world is better served by having one canonical machine-readable dataset than by every photo tool re-researching them in silos. Plus open data tends to stay correct longer than closed databases that depend on one team to maintain.

## License

MIT - see [LICENSE](LICENSE).

You can use this in commercial products, fork it, modify it, redistribute it. Attribution appreciated but not required.

## See also

- [IDPhotoSnap](https://idphotosnap.com) - the canonical browser-only passport photo tool
- [IDPhotoSnap privacy explainer](https://idphotosnap.com/blog/privacy-first-passport-photo-maker-2026) - why browser-only beats encrypted upload
- [ICAO 9303 Part 9](https://www.icao.int/publications/Documents/9303_p9_cons_en.pdf) - international standard for machine-readable travel documents
