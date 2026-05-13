# Examples

Code examples for using the passport-photo-specs dataset.

All examples fetch from the public API at `https://idphotosnap.com/api/specs` (no auth, MIT licensed). The same data is also available in this repository at `specs/specs.json` if you prefer to bundle it.

## Available examples

| Language | File | Notes |
|---|---|---|
| Python | [python/example.py](python/example.py) | Standard library only (`urllib`, `json`). No deps. |
| Go | [go/main.go](go/main.go) | Standard library only (`net/http`, `encoding/json`). No deps. |
| Rust | [rust/main.rs](rust/main.rs) | Uses `reqwest` + `serde`. |
| TypeScript | [../specs/index.ts](../specs/index.ts) | Module exports + lookup helpers. |

## Quick test (no clone needed)

```bash
# Get all China document specs
curl -s "https://idphotosnap.com/api/specs?country=china&format=raw" | python3 -m json.tool

# Get just the dataset metadata
curl -s "https://idphotosnap.com/api/specs?format=raw" | python3 -c "import sys, json; d=json.load(sys.stdin); print(f'{d[\"meta\"][\"countries\"]} countries, {d[\"meta\"][\"documents\"]} documents')"

# Get full Schema.org Dataset JSON-LD (default)
curl -s https://idphotosnap.com/api/specs | head -50
```

## API endpoint

`GET https://idphotosnap.com/api/specs`

Query parameters:
- `country=<id>` - filter to one country (e.g. `italy`, `germany`, `china`)
- `format=raw` - return plain JSON without Schema.org Dataset wrapper

No authentication. CORS open. Cached at edge for 1 hour.

## Schema

```ts
interface Document {
  id: string             // 'italy-visa'
  name: string           // 'Visa'
  slug: string           // 'italy-visa-photo'
  widthMm: number        // 35
  heightMm: number       // 45
  widthPx: number        // 413 (at given DPI)
  heightPx: number       // 531
  dpi: number            // 300
  background: string     // 'Plain light grey'
  bgColor: string        // '#eeeeee' (hex)
  bgColorLabel: string   // 'Light grey'
  requirements: string[] // bullet list
}

interface Country {
  id: string
  name: string
  flag: string
  documents: Document[]
}
```

## Contributing

PRs for additional language examples welcome. Keep dependencies minimal (standard library preferred). One file per language under `examples/<lang>/`.
