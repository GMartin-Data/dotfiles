# Tech Watch — Apache Iceberg row lineage
**Date**: 2026-10-10 | **Window**: 60 days (niche topic) | **Sources**: 8 (5 at or above 60/100, 3 kept below threshold)
**Filter counts**: 94 raw results | 11 on-topic (7 unique after deduplication) | 47 adjacent | 36 off-topic or dropped
**Tiers run**: Tier 1 (arXiv 0, GitHub 1, YouTube 8) · Tier 2 (3 searches) · Tier 3 (all 6 entries, exhausted without reaching 12 on-topic)

> **Coverage note**: the target of 15-20 sources was not reached. Only 7 unique on-topic results exist across all tiers, and only one of them was published inside the 60-day window. The web searches are not date-filtered, so most on-topic sources are older than the window and score 0 on freshness. Tier 3 domains are AI-oriented and returned no on-topic result for this data-engineering topic.

---

## Executive Summary
Row lineage is treated as a settled part of the Iceberg v3 spec: every source describes the same two implicit per-row fields (`_row_id`, `_last_updated_sequence_number`) and the same headline use case, change detection and CDC by filtering on the sequence number instead of running a separate changelog pipeline. Recent activity has moved from explaining the feature to checking engine conformance (which engines read and preserve the lineage columns correctly) and to documenting caveats such as null identifiers on rows upgraded from v2. Unexpected finding: almost nothing new was published in the last 60 days, there are no arXiv papers and no dedicated videos, and the available material is overwhelmingly vendor-authored.

---

## Sources ranked by score

---

### 🔴 Essential (score 85–100)

No source reached this band.

---

### 🟠 High value (score 70–84)

**[1] gunjankaphle/iceberg-v3-duckdb-bench**
🔗 https://github.com/gunjankaphle/iceberg-v3-duckdb-bench
📅 2026-09-16 (created; last push 2026-10-08) | ⭐ Authority: High | 📊 Score: 75/100
**Summary**: Reproducible benchmark checking whether DuckDB reads Iceberg v3 tables correctly. For row lineage it compares each row's `_row_id` and `_last_updated_sequence_number` as read by DuckDB against Spark's values. The repository reports 24 passing checks and zero failures overall (also covering deletion vectors, variant and time travel), and lists six observed gaps and eight untested cases; it gives no lineage-specific verdict.
**Score reason**: Only on-topic result inside the window, from a Tier 1 source; 0 stars, so no engagement signal (freshness scored on creation date, 24 days).
**Tags**: `duckdb`, `iceberg-v3`, `conformance-testing`

---

### 🟡 Worth including (score 60–69)

**[2] Iceberg Row Lineage: The Feature AI and CDC Workloads Will Eventually Depend On**
🔗 https://datalakehousehub.com/blog/iceberg-row-lineage
📅 2026-08-24 | ⭐ Authority: Medium | 📊 Score: 65/100
**Summary**: Long-form article (about 5,000 words) by Alex Merced, who works at Dremio. Explains that engines leave the lineage values null for new rows and derive them from metadata at read time, writing them physically only when a row moves (update, compaction). Covers changelogs between snapshots, CDC and incremental computation, and stresses that identity starts at the v3 upgrade and tracks physical continuity, not business keys.
**Score reason**: Exact match on the topic with the deepest treatment found; 47 days old, so no freshness points.
**Tags**: `row-lineage`, `cdc`, `spec-internals`

**[3] CDC Without Complexity Using Iceberg v3 Row Lineage**
🔗 https://datalakehousehub.com/blog/iceberg-v3-row-lineage-cdc
📅 2026-06-08 | ⭐ Authority: Medium | 📊 Score: 65/100
**Summary**: About 2,300 words by Alex Merced on the CDC recipe: a consumer detects changes by querying rows whose sequence number exceeds its last checkpoint. States the limits clearly: intermediate row states are not tracked, sub-second latency is out of reach, the approach depends on snapshot retention, and replication from operational databases still needs a CDC pipeline. The same post is mirrored on iceberglakehouse.com.
**Score reason**: Exact match with a full practical walkthrough; outside the window.
**Tags**: `cdc`, `incremental-processing`, `row-lineage`

**[4] Accelerate data lake operations with Apache Iceberg V3 deletion vectors and row lineage**
🔗 https://aws.amazon.com/blogs/big-data/accelerate-data-lake-operations-with-apache-iceberg-v3-deletion-vectors-and-row-lineage
📅 2025-11-26 | ⭐ Authority: Medium | 📊 Score: 65/100
**Summary**: AWS Big Data Blog post (about 1,800 words) by Ron Ortloff, Principal Product Manager at AWS. Presents row lineage as per-row metadata recording creation and last change, and contrasts it with the v2 changelog, which according to the post can miss a row inserted and deleted between snapshots. Argues that being part of the v3 spec makes the feature engine-agnostic, so downstream pipelines can process only changed records.
**Score reason**: Exact match in the title, first-party vendor engineering blog; almost a year old.
**Tags**: `aws`, `deletion-vectors`, `iceberg-v3`

**[5] Apache Iceberg Explained: Open Tables, Time Travel, Zero Lock-In | Tech, Decoded Ep 50**
🔗 https://www.youtube.com/watch?v=BtMlYcsht-c
📅 2026-09-22 | ⭐ Authority: High | 📊 Score: 60/100
**Summary**: Adjacent source, not on-topic: a 9-minute general introduction to Iceberg (open tables, time travel). Nothing in its title or description indicates that row lineage is covered. Included only because it clears the threshold on freshness and source tier; useful as background at most.
**Score reason**: Adjacent topic (20/40) offset by Tier 1 source and 18-day freshness; 28 views.
**Tags**: `iceberg-intro`, `video`, `adjacent`

---

### Below threshold, kept (score < 60)

Kept under the scoring rule "drop unless Tier 3 run returns nothing better": Tier 3 returned no on-topic result. All three are exact matches on the topic.

**[6] Dremio and Iceberg v3 row lineage (Dremio blog)**
🔗 https://www.dremio.com/blog/dremio-iceberg-v3-row-lineage/
📅 2026-04-20 | ⭐ Authority: Medium | 📊 Score: 59/100
**Summary**: Short post (about 800 words) by Will Martin, Technical Evangelist at Dremio. States that row lineage is on by default for v3 tables in Dremio Cloud, that `_row_id` persists through updates and that `OPTIMIZE TABLE` preserves both columns. Lists audits, reconciliation, GDPR erasure verification and data quality debugging as use cases, with a short create, update and query exercise.
**Score reason**: Exact match but short and outside the window.
**Tags**: `dremio`, `row-lineage`, `hands-on`

**[7] Iceberg v3 row lineage inheritance (youngju.dev)**
🔗 https://www.youngju.dev/blog/2026-07-16-iceberg-v3-row-lineage-inheritance
📅 2026-07-16 (from the URL) | ⭐ Authority: Medium | 📊 Score: 59/100
**Summary**: Content not verified: the page returned an empty body when fetched. According to the search snippet only, this is a Korean-language post stating that row lineage cannot be turned off on v3 tables (format version 3 or higher implies lineage) and warning that lineage can break in ways that silently damage pipelines.
**Score reason**: Exact match in the title; depth scored at the low anchor because the content could not be read.
**Tags**: `row-lineage`, `inheritance`, `unverified-content`

**[8] Introducing Apache Iceberg 1.9.0: Native Geospatial Support, Enhanced Row Lineage, and More**
🔗 https://medium.com/data-engineering-with-dremio/introducing-apache-iceberg-1-9-0-native-geospatial-support-enhanced-row-lineage-and-more-dead8950d391
📅 Date not retrieved (page returned HTTP 403; tied to the Iceberg 1.9.0 release, well outside the window) | ⭐ Authority: Medium | 📊 Score: 59/100
**Summary**: Content not verified beyond the search snippet. The snippet says that before 1.9.0 row lineage and equality deletes could not coexist and that 1.9.0 removes the limitation, with new row IDs assigned to rows inserted or updated when equality deletes are applied.
**Score reason**: Exact match in the title; depth scored at the low anchor because the content could not be read.
**Tags**: `iceberg-1.9`, `equality-deletes`, `unverified-content`

---

## Trends identified

- **Consensus on the mechanism and the use case**: every source read describes the same two implicit fields and positions row lineage primarily as a way to do change detection and CDC with a plain filter on the sequence number.
- **Focus is shifting to engine conformance**: the only in-window on-topic result is a conformance benchmark (DuckDB against Spark), and adjacent results point to uneven engine support. These engine claims come from search snippets and one adjacent article, not from release notes, and should be checked before use.
- **Migration and limits are the recurring caveats**: rows upgraded from v2 have no identifier until rewritten, identity is physical rather than tied to business keys, intermediate states between snapshots are not captured, and the CDC recipe depends on snapshot retention.
- **Unresolved contradiction on identifier stability**: several sources state that `_row_id` survives updates, while the snippet for the 1.9.0 article says new row IDs are assigned when equality deletes are applied. The search did not settle this; the Iceberg v3 specification is the reference and was not among the results.
- **Vendor-driven, thin recent coverage**: the material comes almost entirely from Dremio-affiliated authors and AWS, with no arXiv paper, no dedicated video and no Hacker News thread on row lineage itself. One article notes that the feature needs no configuration, which may explain the lack of tutorials.

---

## Excluded but notable (adjacent, below threshold)

- Apache Iceberg v3 Is GA. Here Is What Data Engineers Get (dev.to, Sep 15, year not shown): v3 overview with a row lineage section, including the v2 upgrade caveat. https://dev.to/datadriven/apache-iceberg-v3-is-ga-here-is-what-data-engineers-get-51ol
- Apache Iceberg v3: What Snowflake Data Teams Need to Know (Atlan, 2026-06-03). https://atlan.com/know/snowflake/apache-iceberg-v3/
- Working with Apache Iceberg V3 (Amazon S3 user guide). https://docs.aws.amazon.com/AmazonS3/latest/userguide/working-with-apache-iceberg-v3.md
- Delta Lake and Iceberg in 2026: Catalog Commits, Delta Kernel, and AI-Native Data Types (Databricks Events, 2026-09-09, 31 min). https://www.youtube.com/watch?v=riMwkepxTqo
- Efficient Row-Level Lineage Leveraging Predicate Pushdown (arXiv 2412.16864): row-level lineage in query pipelines, not the Iceberg feature. https://arxiv.org/pdf/2412.16864

---

*Generated by tech-watch skill | Sources: arXiv · GitHub · YouTube · Web search*
*Scoring: Relevance 40% · Freshness 20% · Authority 20% · Depth 10% · Engagement 10%*
