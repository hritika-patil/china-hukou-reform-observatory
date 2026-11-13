# Methodology and limitations

**Edition 0.3 · evidence snapshot 12 November 2026 · mainland China: 31 provincial-level jurisdictions.** Hong Kong, Macau and Taiwan are not coded within the same mainland hukou framework.

## Research question

How do different provincial and municipal authorities translate national hukou-reform priorities into concrete rules for acquiring local registration and accessing education, housing and social protection without a local hukou?

## Comparative units

The 31 province-level jurisdictions are the **national coverage frame**. Laws can be issued by a central ministry, province/autonomous region/municipality, prefecture-level city, district, or service agency. A municipal example (e.g. Dongguan, Jiaxing, Chengdu or Yantai) **never justifies the claim that its rule applies throughout the province**. The city's scope is recorded separately in `data/policies.json`. The 63 research locations are proposed subsequent research cases, not a verified municipal dataset.

Each jurisdiction has four evidence records:
1. **Settlement** — local hukou acquisition, points, duration/permit/insurance, work or housing conditions, family routes.
2. **Education** — migrant-child compulsory school admission, permit/insurance tests, school choice and entrance examinations.
3. **Housing** — non-local-hukou public rental housing, income/insurance/document thresholds, allocation and waiting rules.
4. **Protection** — access to insurance, pensions, employment benefits, social assistance and portability.

## Evidence classification (not a hukou openness scale)

| Classification | Meaning | Does NOT mean |
|---|---|---|
| `rule-documented` | A domain-specific operative rule or narrowly scoped municipal case located | All related eligibility routes, amendments or enforcement are verified |
| `direction-documented` | Government plan, directive or programme relevant to the domain | Individual right to obtain the named service |
| `related-document` | A relevant published source without the operative conditions sought | Reforms were implemented or eligibility confirmed |
| `unverified` | Source corpus does not yet establish the specific rule for that domain | Restrictive policy or no reform |

**Evidence snapshot:** 31 jurisdictions, 124 audit cells, 46 documents (4 national, 42 local). Rule-documentation: 8 cells; policy direction: 60; related-only: 18; unverified: 38. None is a comprehensive city-by-city legal audit or verified implementation outcome.

## Source hierarchy and cautions

1. Government original normative text/gazette, noting dates and issue numbers.
2. Department and municipal implementing instructions, application rules and current notices.
3. Government monitoring/statistics to evaluate delivery, not to infer from legislation.
4. Peer-reviewed literature and independent reporting to contextualise claims, not as substitutes for current eligibility regulations.

A source URL may be an **official government reprint**, not the first publication. The `date` can be the *published/indexed* date and `effective_date` can be `null`. A dated earlier rule may have since been amended or repealed. Every entry includes a provenance URL and caveat. The site does not purport to authenticate its continuing legal effect in November 2026.

The `dimension` field in the source library means a text *touches* a policy issue, not that it codifies applicant-level eligibility. The `rule-documented` class was intentionally restricted to narrower settlement instruments and a Shanghai-specific school-admission notice.

## Current national baseline

The 2014 State Council household-registration reform opinion, the July 2024 new-type urbanisation plan, and the May 2026 State Council residence-based public-service guidance form national background. They should **never** be counted as evidence of implementation within a particular province. Visit `data/policies.json` for original Chinese government URLs and document dates.

## Future requirement before a fully verified legal audit

For each of the 31 regions and all four policy areas: establish an operative **province-level framework and municipal/district eligibility rules** for at least two contrasting cities, check the issuing agency's current validity/repeals, record beneficiary categories, thresholds, documentation requirements, effective periods and exceptions, and then separately obtain administrative implementation evidence. That would entail more than 124 province-level desk assessments. Do not add a provincial composite rating until comparable units and missing-data handling are settled.

## Map / interface limitations

The choropleth shows indexed source coverage, **not settlement ease or service access**. It uses third-party GeoJSON as a geographic locator, with boundaries that should not be treated as a legal position on territorial claims. The year filter is retrospective by document date (cumulative issued-through-year) and is not a 'valid in that year' filter. All unknowns remain visible.

## Reproducibility

Each record contains source ID, date, document title, administrative level, agency, original URL, geographic scope, evidence type, concise finding and caveat; each audit record includes province × dimension, source IDs, source URLs, evidence class and unresolved check. Run `python tools/refresh_matrix.py` after updating both JSON inputs, followed by `python tools/validate_data.py`.
