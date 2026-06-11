# Passport & Visa Photo Specifications (100 Countries, 248 Document Formats)

Machine-readable photo requirements for passports, visas, ID cards, residence permits, and driving licences across 100 countries: physical dimensions (mm), pixel dimensions, DPI, background color, portal file-size caps, and a citation to the issuing government source for every spec.

## Files

- `passport_photo_specs.csv` - flat table, one row per country+document (248 rows)
- `passport_photo_specs_full.json` - full nested dataset with metadata, validation rules, and source citations

## Columns (CSV)

| column | description |
|---|---|
| country / country_id | Country name and ISO-style id |
| document / document_id | Document type (passport, visa, eVisa, residence permit, etc.) |
| width_mm / height_mm | Physical print dimensions |
| width_px / height_px | Digital upload dimensions where a portal specifies them |
| dpi | Required print resolution |
| background | Required background color (verbatim from the issuing authority) |
| max_file_kb | Portal upload cap where applicable (e.g. Saudi Enjaz 200 KB, Japan MOFA eVisa 240 KB) |
| source_url | Government source the spec was validated against |

## Provenance and maintenance

- Canonical repository: https://github.com/BlondDev-Art/passport-photo-specs (MIT)
- Archived with DOI: 10.5281/zenodo.20409880
- Also available as a free JSON API: https://idphotosnap.com/api/specs
- Validated against 15+ official government sources (US State Dept, UK HMPO, German Bundesdruckerei, Indian Passport Seva, Chinese MFA COVA, Saudi MOFA/Enjaz, Japan MOFA, and others). Each spec row carries its citation.
- Maintained by Elena, founder of IDPhotoSnap (https://idphotosnap.com), a free browser-based passport photo tool built on top of this dataset.

## Example uses

- Travel apps validating user photo uploads before portal submission
- Research on biometric document standardization (ICAO 9303 adherence by country)
- Comparison of government portal upload constraints across countries

## License

MIT. Attribution appreciated: link to the GitHub repository or the Zenodo DOI.
