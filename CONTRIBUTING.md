# Contributing

Two ways to contribute, both welcome.

## 1. Spec correction

If you have evidence that a spec in this dataset is wrong, open an issue with:

- Country and document type (e.g. "Italy passport")
- Current value in our data (`grep "italy-passport" specs/specs.json`)
- Correct value with a link to the official government source
- (Optional) Screenshot of the official requirement page

We will verify the source and update the spec.

## 2. Adding a country

If a country is missing, open a PR with:

- A new `CountrySpec` entry in `specs/specs.json` following the existing schema
- A link to the official government source for each document type added
- Validated via `node scripts/validate.js` (no errors)

## What we don't accept

- Specs copied from other photo tool websites or aggregators - we cite primary government sources only
- Inflated country counts via ICAO 9303 default fallback - if a country's spec is identical to the ICAO default, that's already covered
- AI-generated specs without source verification
- Specs based on personal experience without official documentation

## Schema reference

See `specs/index.ts` for the TypeScript types or load `specs/specs.json` and inspect.

## Validation

```bash
node scripts/validate.js
```

This checks for duplicate ids, dimension consistency (mm vs px at given DPI), and meta counts.

## License

By contributing you agree your contribution will be licensed under MIT (see LICENSE).
