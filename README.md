# China Hukou Reform Observatory

**Edition 0.3 — research snapshot 12 November 2026.** A static, mobile-responsive, source-led research platform for tracking how hukou reforms are articulated and administered in the 31 mainland provincial-level jurisdictions.

## Deliverables and coverage

- **31 jurisdiction profiles** (22 provinces, 5 autonomous regions, 4 provincial-level municipalities).
- **31/31 jurisdictions** have at least one geographically scoped government source anchor.
- **124 source triage assessments**, one for each jurisdiction × settlement, education, public rental housing, and social protection.
- **46 policy source records**, including **4 national** and **42 jurisdiction-level** records, plus a proposed roster of **63 municipality/district research locations**.
- Interactive map with mouse/keyboard province selection, source-coverage colour, province detail panel, year and policy filters, map zoom, full jurisdiction directory, 31-province table, 124-entry audit explorer, three-jurisdiction compare panel, and searchable document library.
- Exportable CSV files and a separate Excel research workbook (distributed alongside the ZIP).

**Current evidence breakdown:** 8 rule documented, 38 unverified, 60 direction documented, 18 related document. This is an evidence *coverage* review, **not 124 completed and currently enforceable applicant-level legal determinations**. For many service areas a provincial policy sets only a direction. The website documents this distinction and shows open research questions.

## Publish with GitHub Pages

1. Create a **public** GitHub repository named `china-hukou-reform-observatory`.
2. Upload the **contents** of this folder (`index.html` at repository root), including the complete `data/` folder and `.nojekyll`.
3. Commit on `main`; navigate to **Settings → Pages → Build and deployment → Deploy from a branch → main → /(root)**.
4. Visit `https://YOUR-USERNAME.github.io/china-hukou-reform-observatory/` after the deployment completes.

GitHub Pages requires no paid hosting. This package has not been pushed or published to a GitHub account.

## Preview locally

In this directory run `python -m http.server 8000`, then navigate to `http://localhost:8000`. Opening `index.html` as a file will not work because browser JavaScript cannot reliably load local JSON files from `file://` URLs.

**Map limitation:** Province boundary GeoJSON is loaded from third-party `cn-atlas` 0.1.2 CDNs at runtime. Internet/CDN access is needed for the map, but the jurisdiction directory, audit table, record library and comparison remain available if map loading fails. Map geometry is a general-purpose locator, not an authoritative legal boundary determination. See `ATTRIBUTION.md`.

## Data structure

| File | Purpose |
|---|---|
| `data/provinces.json` | All 31 provincial-level units |
| `data/cities.json` | 63 candidate municipal/district research case locations |
| `data/policies.json` | 46 links to original government documentation, national and local |
| `data/audits.json` | 124 evidence classifications, findings, links and outstanding questions |
| `data/policy_audits_124.csv` | Portable complete evidence assessment table |
| `data/source_register.csv` | Searchable primary-source bibliography for all 46 records |
| `data/research_matrix.csv` | Extended province × policy-area research matrix |
| `PROVINCIAL_COVERAGE.md` | Human-readable complete 31-jurisdiction inventory |
| `METHODOLOGY.md` | Coding rules, limitation statements, source hierarchy |

After adding/editing `data/policies.json` **also update the corresponding `data/audits.json` entries manually** (checking accurate source identifiers, findings and evidence class). Then run `python tools/refresh_matrix.py` to sync CSV outputs and `python tools/validate_data.py` to check references and structural integrity. A new policy source does **not** automatically prove applicant eligibility or current legal force.

## Interpretive rules

1. **Rule documented** = a source addresses a concrete applicant-level rule in that jurisdiction or an explicitly scoped municipal example, not necessarily the complete 2026 law.
2. **Policy direction** = an official plan/guideline articulates goals but does not independently establish individual entitlement.
3. **Related document** = registration administration, secondary implementation report, or background policy but no complete domain eligibility rule established.
4. **Unverified** = no adequate source in the indexed corpus, not evidence that access is restrictive or reform absent.

Only one city may be evidenced under a province. Most sources have **not** been cross-checked for amendments, repeals or court challenges, and no audited service delivery outcomes are included. The year selector means documents published up to a year, not necessarily valid in that year. Do **not** rank provincial policy openness or compare real service access from this dataset.

## Licensing

Original website is MIT-licensed. Third-party map boundary data and original government policy content remain under their respective terms. See `LICENSE` and `ATTRIBUTION.md`.
