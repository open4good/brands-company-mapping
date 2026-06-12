# brands-company-mapping

This repository hosts the **brand / company referential** used by
[nudger](https://nudger.fr): it resolves raw brand names to the companies that
own them, and enriches those companies with **sourced** intelligence
(manufacturing places, ESG / ethics scores, certifications, controversies, facts).

## Purpose

The original goal was to resolve company names from brands so nudger could
integrate external ESG ratings into its ImpactScore. The referential now goes
further: it is the curated, auditable source of truth for brand intelligence,
maintained batch-by-batch by an AI agent (the `brands-maintenance` playbook),
with every fact carrying its source URL and retrieval date.

## Layout

- `brands-company-mapping.json` — versioned referential (`version: 3`). The
  `brands` array maps canonical brand names (and their synonyms / official
  domains) to a `company-id`.
- `company/<id>.json` — one file per company, holding the enriched v3 record.
- `schema/*.json` — JSON Schema (draft 2020-12) for both files. CI validates
  every file against them (`scripts/validate.py`).
- `scripts/migrate_v2_to_v3.py` — one-shot v2 → v3 migration (already applied).

## Company schema (v3)

```json
{
  "schemaVersion": 3,
  "id": "apple-inc",
  "name": "Apple, Inc.",
  "aliases": [],
  "parentCompanyId": null,
  "identifiers": { "wikidata": "Q312" },
  "hq": { "country": "US", "city": "Cupertino", "lat": 37.33, "lon": -122.01, "sources": [] },
  "manufacturing": [
    { "categories": ["tv"], "country": "CN", "city": "Zhengzhou",
      "lat": 34.74, "lon": 113.62, "type": "factory", "operator": "Foxconn",
      "sources": [{ "url": "https://opensupplyhub.org/...", "label": "Open Supply Hub", "retrievedAt": "2026-06-01" }] }
  ],
  "scores": {
    "cdp": { "value": 7, "rating": "A-", "scale": { "min": 0, "max": 8, "higherIsBetter": true },
             "url": "https://...", "retrievedAt": "2026-06-01" }
  },
  "xmetas": [
    { "key": "certification.bcorp", "type": "certification", "value": "Certified since 2022",
      "url": "https://...", "retrievedAt": "2026-06-01" }
  ],
  "provenance": { "maintainedBy": "brands-maintenance", "batch": "001", "updatedAt": "2026-06-12" }
}
```

Key rules enforced by the schema:

- **Manufacturing is category-aware**: `categories` holds open4goods vertical ids;
  an empty list means the site applies to all categories. A company can build TVs
  in one country and fridges in another.
- **Coordinates are mandatory** on each manufacturing site — the runtime never
  geocodes; the agent resolves coordinates at enrichment time.
- **Everything is sourced**: manufacturing sites, scores and x-metas all require a
  source URL. The `Sustainalytics` score is *not* curated here — it is scraped
  live by the crawler into Elasticsearch and merged at read time.

## Brand sanitization

Brand keys are upper-cased, trimmed and accent-stripped:

```java
public String sanitizeBrand(String name) {
  if (StringUtils.isEmpty(name)) return "";
  return StringUtils.stripAccents(StringUtils.normalizeSpace(name).toUpperCase()).trim();
}
```

## Contributing

Most enrichment is performed by the `brands-maintenance` agent. Manual PRs are
welcome: edit the relevant `company/<id>.json`, keep every new fact sourced, and
make sure `python3 scripts/validate.py` passes before opening the PR.
