#!/usr/bin/env python3
"""
Publish the current specs/specs.json as a new Zenodo version, so the
concept DOI (10.5281/zenodo.20705585) keeps resolving to the latest data.

Run this after bumping the version in specs/specs.json + CHANGELOG.md
and pushing a GitHub release - Zenodo does NOT auto-sync from GitHub for
this repo (the GitHub-app webhook was never actually wired up, confirmed
2026-09-09), so this script is the real mechanism, not the badge in the
README claiming automatic sync.

Requires ZENODO_TOKEN in ~/.idphotosnap_env (a Zenodo personal access
token with deposit:write and deposit:actions scopes).

Usage:
  python3 scripts/publish_zenodo_version.py
"""
import json
import os
import sys
import urllib.request
import urllib.error

LATEST_RECORD_ID = "22672168"  # bump this to whatever this script last published
ENV_FILE = os.path.expanduser("~/.idphotosnap_env")
SPECS_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "specs", "specs.json")


def _token():
    for line in open(ENV_FILE):
        if line.startswith("ZENODO_TOKEN="):
            return line.strip().split("=", 1)[1]
    raise RuntimeError(f"ZENODO_TOKEN not found in {ENV_FILE}")


def _req(url, token, method="GET", data=None, content_type="application/json"):
    sep = "&" if "?" in url else "?"
    req = urllib.request.Request(f"{url}{sep}access_token={token}", data=data, method=method)
    if data is not None:
        req.add_header("Content-Type", content_type)
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"{method} {url} -> {e.code}: {e.read().decode()[:300]}")


def main():
    token = _token()
    specs = json.load(open(SPECS_FILE))
    meta = specs["meta"]

    print(f"Publishing specs.json v{meta['version']} ({meta['countries']} countries, {meta['documents']} documents)")

    draft = _req(
        f"https://zenodo.org/api/deposit/depositions/{LATEST_RECORD_ID}/actions/newversion",
        token, method="POST",
    )
    draft_url = draft["links"]["latest_draft"]
    draft_id = draft_url.rsplit("/", 1)[-1]
    print(f"New draft: {draft_id}")

    draft_detail = _req(f"https://zenodo.org/api/deposit/depositions/{draft_id}", token)
    for f in draft_detail.get("files", []):
        _req(f"https://zenodo.org/api/deposit/depositions/{draft_id}/files/{f['id']}", token, method="DELETE")
        print(f"Deleted old file: {f['filename']}")

    bucket = draft_detail["links"]["bucket"]
    with open(SPECS_FILE, "rb") as f:
        _req(f"{bucket}/specs.json", token, method="PUT", data=f.read(), content_type="application/octet-stream")
    print("Uploaded new specs.json")

    changelog_note = (
        f"<p><strong>v{meta['version']} ({meta['lastUpdated']}):</strong> see "
        f"https://github.com/BlondDev-Art/passport-photo-specs/blob/main/CHANGELOG.md "
        f"for what changed in this version.</p>"
    )
    metadata_update = {
        "metadata": {
            "title": f"Passport, Visa & ID Photo Specifications ({meta['countries']} Countries, {meta['documents']} Documents)",
            "upload_type": "dataset",
            "description": (
                "<p>Canonical, machine-readable dataset of passport, visa, and identity document "
                "photo specifications, validated against official government sources. Covers "
                f"{meta['countries']} countries and {meta['documents']} distinct document formats.</p>"
                + changelog_note +
                "<p>The dataset is the underlying reference used by the browser-only passport photo "
                "tool at <a href='https://idphotosnap.com'>idphotosnap.com</a>.</p>"
            ),
            "access_right": "open",
            "license": "CC-BY-4.0",
            "creators": [{"name": "Elena Dev", "affiliation": "IDPhotoSnap"}],
            "keywords": [
                "passport photo", "visa photo", "biometric photo", "ICAO 9303", "identity document",
                "passport specifications", "visa requirements", "government compliance", "open dataset",
                "travel documents", "machine readable", "face detection", "biometric standards",
                "open data", "FAIR data",
            ],
            "related_identifiers": [
                {"identifier": "https://github.com/BlondDev-Art/passport-photo-specs", "relation": "isSupplementTo", "resource_type": "software"},
                {"identifier": "https://idphotosnap.com", "relation": "isReferencedBy", "resource_type": "other"},
                {"identifier": "https://www.npmjs.com/package/passport-photo-specs", "relation": "isIdenticalTo", "resource_type": "software"},
            ],
        }
    }
    _req(
        f"https://zenodo.org/api/deposit/depositions/{draft_id}",
        token, method="PUT", data=json.dumps(metadata_update).encode(),
    )
    print("Updated metadata")

    published = _req(f"https://zenodo.org/api/deposit/depositions/{draft_id}/actions/publish", token, method="POST")
    print(f"PUBLISHED: {published['doi']}")
    print(f"Concept DOI (unchanged, always latest): {published['conceptdoi']}")
    print()
    print(f"!! Update LATEST_RECORD_ID in this script to {published['id']} for the next run.")


if __name__ == "__main__":
    main()
