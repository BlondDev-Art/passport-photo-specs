# Changelog

All notable changes to `passport-photo-specs` are documented here.
This project follows [Semantic Versioning](https://semver.org/).

## [1.4.0] - 2026-09-09

### Fixed
Synced from the live upstream dataset after several real spec corrections found and fixed on idphotosnap.com since the last release. This repo had not been updated since 2026-06-15 and was carrying the pre-fix values.

- Philippine passport photo background: was blue, current DFA ePassport requirement is white (blue was for the older machine-readable passport).
- Malaysia head-crop ratio: was 70-80% (common band), JIM's actual spec is 50-60%.
- UAE visa photo size: was incorrectly duplicating the passport's 40x60mm, actual visa spec is 43x55mm.
- India passport head-crop: was 70-80%, ICAO enforcement tightened to 80-85% in September 2025.
- Head-ratio overrides added for Canada, Turkey, and Hong Kong (previously using the generic default).

### Changed
- Data now includes the June 2026 addition of Venezuela, Afghanistan, and Dominican Republic (previously landed without a proper version bump).
- Total unchanged at 103 countries, 276 document formats (corrections, not additions).

## [1.3.0] - 2026-05-27

### Added
- `.zenodo.json` metadata file so new GitHub releases mint a versioned
  DOI via the Zenodo - GitHub integration. The dataset is now formally
  citable (e.g. for academic work, biometric-tooling research, or
  AI-search engines that prefer DOI-backed sources).
- Aligned `package.json` version with the CHANGELOG history.

## [1.2.1] - 2026-05-13

### Changed
- Description normalized to "100+ countries / 248 document formats" so
  the framing stays accurate as new countries are added.

## [1.2.0] - 2026-05-13

### Added
- Python, Go, and Rust code examples under `examples/`.
- Live API usage notes in `README.md`.

## [1.1.0] - 2026-05-12

### Added
- Expanded coverage to 100 countries and 248 document formats
  (+11 ICP-aligned destinations: emerging-market visa applicants
  applying for developed-country visas).

### Changed
- All new entries validated against the same official-government-source
  rule as the v1.0 release. Inline `source` URL on every document.

## [1.0.0] - 2026-05-11

### Added
- Initial public release: 89 countries, 226 document formats.
- All specs validated against 15+ official government sources
  (US State Department, UK Home Office, Schengen ICAO, etc.).
- TypeScript type definitions (`specs/index.ts`).
- `validate.js` script for downstream consumers.
- MIT License.

[1.2.1]: https://github.com/BlondDev-Art/passport-photo-specs/releases/tag/v1.2.1
[1.2.0]: https://github.com/BlondDev-Art/passport-photo-specs/releases/tag/v1.2.0
[1.1.0]: https://github.com/BlondDev-Art/passport-photo-specs/releases/tag/v1.1.0
[1.0.0]: https://github.com/BlondDev-Art/passport-photo-specs/releases/tag/v1.0.0
