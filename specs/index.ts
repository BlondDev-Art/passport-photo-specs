/**
 * passport-photo-specs - canonical passport photo specifications
 *
 * MIT licensed. Validated against 15+ official government sources.
 * 89 countries, 226 document formats.
 *
 * Upstream: https://idphotosnap.com
 * Repository: https://github.com/BlondDev-Art/passport-photo-specs
 */

import specsData from './specs.json'

export interface DocumentSpec {
  /** Stable identifier, e.g. "italy-visa" */
  id: string
  /** Display name within country context, e.g. "Visa" or "Passport" */
  name: string
  /** URL-safe slug, e.g. "italy-visa-photo" */
  slug: string
  /** Photo width in millimeters */
  widthMm: number
  /** Photo height in millimeters */
  heightMm: number
  /** Photo width in pixels at the given DPI */
  widthPx: number
  /** Photo height in pixels at the given DPI */
  heightPx: number
  /** Dots-per-inch resolution (typically 300) */
  dpi: number
  /** Human-readable background description */
  background: string
  /** Background color as hex code, e.g. "#ffffff" */
  bgColor: string
  /** Background color label, e.g. "White" or "Light grey" */
  bgColorLabel: string
  /** Detailed requirements as bullet points */
  requirements: string[]
}

export interface CountrySpec {
  /** ISO-style country identifier, e.g. "italy" */
  id: string
  /** Display name, e.g. "Italy" */
  name: string
  /** Emoji flag */
  flag: string
  /** All document types supported for this country */
  documents: DocumentSpec[]
}

export interface SpecsMeta {
  name: string
  version: string
  description: string
  countries: number
  documents: number
  license: string
  repository: string
  upstream: string
  lastUpdated: string
  governmentSources: string[]
}

export interface Specs {
  meta: SpecsMeta
  countries: CountrySpec[]
}

const specs = specsData as Specs

export const meta: SpecsMeta = specs.meta
export const countries: CountrySpec[] = specs.countries

export const allDocuments: DocumentSpec[] = countries.flatMap((c) => c.documents)
export const countriesById: Record<string, CountrySpec> = Object.fromEntries(countries.map((c) => [c.id, c]))
export const documentsBySlug: Record<string, DocumentSpec> = Object.fromEntries(allDocuments.map((d) => [d.slug, d]))

/**
 * Find a country by id, e.g. findCountry("italy")
 */
export function findCountry(id: string): CountrySpec | undefined {
  return countriesById[id]
}

/**
 * Find a document by slug, e.g. findDocument("italy-visa-photo")
 */
export function findDocument(slug: string): DocumentSpec | undefined {
  return documentsBySlug[slug]
}

/**
 * Get all documents for a country
 */
export function documentsForCountry(countryId: string): DocumentSpec[] {
  return countriesById[countryId]?.documents ?? []
}

export default specs
