# Brands maintenance batch 001

- Date: 2026-06-12
- Mode: enrich
- Batch size: 5
- Index range: 0-4
- Company ids: `acer-inc`, `apple-inc`, `arcelik-as`, `asbisc-enterprises-plc`, `asustek-computer-inc`

## Summary

| Company | Identity | Manufacturing sites | Scores | X-metas |
| --- | ---: | ---: | ---: | ---: |
| acer-inc | 1 HQ, 2 identifiers | 0 | 1 | 2 |
| apple-inc | 1 HQ, 2 identifiers | 0 | 0 | 2 |
| arcelik-as | 1 HQ, 2 identifiers | 0 | 1 | 2 |
| asbisc-enterprises-plc | 1 HQ, 1 identifier | 0 | 0 | 2 |
| asustek-computer-inc | 1 HQ, 2 identifiers | 0 | 1 | 2 |

## Added data

- `acer-inc`: Wikidata identity and HQ, LEI, MSCI AAA rating from Acer news, renewable electricity commitment, EcoVadis Platinum fact.
- `apple-inc`: Wikidata identity and HQ, LEI, 2030 carbon-neutral value-chain commitment, fiscal year 2024 emissions-reduction fact from Apple's 2025 CDP questionnaire.
- `arcelik-as`: Wikidata identity and HQ, LEI, S&P Global CSA score, Global 100 fact, CDP reporting fact.
- `asbisc-enterprises-plc`: Wikidata identity and HQ, 2024 sustainability-reporting fact, business-profile fact.
- `asustek-computer-inc`: Wikidata identity and HQ, LEI, CDP Climate Change A rating for 2024, CDP leadership fact, Clean200 fact.

## Skipped providers

- Open Supply Hub: unauthenticated API requests returned HTTP 401, and no token was available in the environment. No manufacturing records were written because every manufacturing entry requires sourced coordinates.
- Local geocoder: `http://localhost:8080/v1/geocode` was unreachable. HQ coordinates were only written where Wikidata provided coordinates.
- B Corp: no certified B Corp coverage was found for the five companies during this pass.
- MSCI: public provider pages were not reliably accessible for all companies; only Acer was written because Acer directly reported its MSCI AAA rating.
- LSEG: skipped because public score pages are anti-bot/paywalled in this environment.
- Ethical Consumer / Good Shopping Guide: skipped for this batch because no free, provider-grade score suitable for direct JSON ingestion was verified.
- Sustainalytics: intentionally not written to `scores` per playbook runtime-ownership rule.

## Data-quality notes

- Manufacturing remains empty for all five companies. This is preferable to adding ungeocoded or unsourced factory claims; follow-up needs OSH credentials or the local geocode service restored.
- ASBIS has no LEI in the Wikidata result used for this batch, so only the Wikidata identifier was written.
- Provider score coverage is intentionally sparse: when sources disclosed commitments or reporting but not a provider score, the datum was recorded as an `xmeta` fact instead of a synthetic score.
