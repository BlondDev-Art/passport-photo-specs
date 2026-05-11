#!/usr/bin/env node
/**
 * Validate the specs.json data integrity.
 * Run: node scripts/validate.js
 */

const fs = require('fs')
const path = require('path')

const specs = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'specs', 'specs.json'), 'utf8'))

let errors = 0
let warnings = 0

function err(msg) { console.error('ERROR:', msg); errors++ }
function warn(msg) { console.warn('WARN:', msg); warnings++ }

// Check meta
if (!specs.meta) err('Missing meta block')
if (!specs.countries || !Array.isArray(specs.countries)) err('countries must be an array')

// Validate per country
const countryIds = new Set()
const docSlugs = new Set()
let totalDocs = 0

for (const country of specs.countries) {
  if (!country.id) err(`Country missing id: ${JSON.stringify(country).slice(0, 80)}`)
  if (!country.name) err(`Country ${country.id} missing name`)
  if (!country.flag) warn(`Country ${country.id} missing flag emoji`)
  if (countryIds.has(country.id)) err(`Duplicate country id: ${country.id}`)
  countryIds.add(country.id)

  if (!country.documents || !Array.isArray(country.documents)) {
    err(`Country ${country.id} missing documents array`)
    continue
  }

  for (const doc of country.documents) {
    totalDocs++
    if (!doc.id) err(`${country.id}: doc missing id`)
    if (!doc.slug) err(`${country.id}/${doc.id}: missing slug`)
    if (docSlugs.has(doc.slug)) err(`Duplicate slug: ${doc.slug}`)
    docSlugs.add(doc.slug)

    if (!doc.widthMm || !doc.heightMm) err(`${doc.slug}: missing dimensions`)
    if (doc.widthMm < 20 || doc.widthMm > 80) warn(`${doc.slug}: unusual width ${doc.widthMm}mm`)
    if (doc.heightMm < 25 || doc.heightMm > 80) warn(`${doc.slug}: unusual height ${doc.heightMm}mm`)

    if (!doc.widthPx || !doc.heightPx) err(`${doc.slug}: missing pixel dimensions`)
    if (!doc.dpi || doc.dpi < 100) warn(`${doc.slug}: unusual DPI ${doc.dpi}`)

    // Verify pixel/mm/DPI consistency (allow 1px tolerance from rounding)
    const expectedWidthPx = Math.round((doc.widthMm / 25.4) * doc.dpi)
    const expectedHeightPx = Math.round((doc.heightMm / 25.4) * doc.dpi)
    if (Math.abs(doc.widthPx - expectedWidthPx) > 2) {
      warn(`${doc.slug}: widthPx ${doc.widthPx} != expected ${expectedWidthPx} at ${doc.dpi} DPI`)
    }
    if (Math.abs(doc.heightPx - expectedHeightPx) > 2) {
      warn(`${doc.slug}: heightPx ${doc.heightPx} != expected ${expectedHeightPx} at ${doc.dpi} DPI`)
    }

    if (!doc.bgColor || !/^#[0-9a-f]{6}$/i.test(doc.bgColor)) warn(`${doc.slug}: invalid bgColor ${doc.bgColor}`)
    if (!doc.background) err(`${doc.slug}: missing background description`)
    if (!doc.requirements || !Array.isArray(doc.requirements)) warn(`${doc.slug}: missing requirements array`)
  }
}

console.log('---')
console.log(`Countries: ${specs.countries.length} (meta says ${specs.meta.countries})`)
console.log(`Documents: ${totalDocs} (meta says ${specs.meta.documents})`)
console.log(`Errors: ${errors}`)
console.log(`Warnings: ${warnings}`)

if (specs.countries.length !== specs.meta.countries) err(`Country count mismatch: data has ${specs.countries.length}, meta says ${specs.meta.countries}`)
if (totalDocs !== specs.meta.documents) err(`Document count mismatch: data has ${totalDocs}, meta says ${specs.meta.documents}`)

process.exit(errors > 0 ? 1 : 0)
