---
layout: ../../layouts/Project.astro
title: A lakehouse built only from open tools
kind: Data engineering
org: Personal · open source
date: '2026-11'
period: Nov 2026
summary: The medallion pattern I run on Databricks at work, rebuilt from open parts (Apache Iceberg tables, DuckDB, Dagster and a YAML data contract) and loaded with 3.4 million US flights from the Bureau of Transportation Statistics.
impact: Six months of flights (3,446,675 rows) downloaded, validated and modeled in about two minutes on a laptop; the contract caught one real error in the government data
img: img/open-lakehouse.jpg
tags: [apache iceberg, medallion architecture, data contracts, data quarantine, schema drift, schema evolution, idempotent loads, time travel, scd type 2, star schema, reconciliation, duckdb, dagster, docker, pytest, python]
links:
  - { t: Live report, href: 'https://sidantap.github.io/portfolio-redesign/lakehouse/' }
  - { t: Code and README, href: 'https://github.com/sidantap/open-lakehouse' }
---

At work the lakehouse is a vendor platform: the table format, the catalog and the scheduler come in one box. I wanted to know I understood the pattern and not just the product, so I built it again from parts anyone can install, and gave it real, public data: every scheduled US domestic flight from the Bureau of Transportation Statistics (BTS).

<figure><img src="../../fig/open-lakehouse-architecture.svg" alt="BTS monthly zips land once, then load into bronze, silver and gold Iceberg tables; DuckDB runs the SQL, a YAML data contract checks silver, and Dagster orchestrates everything by month" /><figcaption>Fig. 1 · From a monthly zip to a star schema</figcaption></figure>

## The contract is the schema

Most pipelines keep the schema in one place, the quality checks in another and the documentation in a third, and the three slowly disagree. Here a single YAML file declares every silver column: where it comes from, its type, whether it's required, its range or pattern. It also holds rules that span columns:

```yaml
- name: delay_causes_add_up
  # causes, when reported, sum to
  # the minutes the flight was late
  sql: >-
    carrier_delay_min IS NULL OR
    carrier_delay_min
      + weather_delay_min
      + nas_delay_min
      + security_delay_min
      + late_aircraft_delay_min
      = arr_delay_late_min
```

A small compiler turns the file into one DuckDB query that types each column and attaches to every row the list of checks it failed: 98 checks in all. An empty list means the row goes to silver. Anything else goes to **quarantine**, with the names of the failed checks and the raw values exactly as they arrived. Nothing is dropped and nothing is quietly "fixed".

## What it caught

Six months, 3,446,676 rows, one rejection, and it was real:

| | |
|---|---|
| Flight | PSA Airlines 5292, Charlotte → Knoxville, March 30, 2025 |
| Distance | 177 miles |
| Scheduled | 22:49 → 23:59, about 70 minutes |
| Reported scheduled duration | **1,510 minutes**, about 25 hours |
| Failed check | `max:crs_elapsed_min` |

The flight stays out of every number built on silver, and it's kept for anyone who wants to correct it. If more than 0.5% of a month ever failed, the load would stop before writing anything: that many failures means the source changed, and a person should look before a filter hides it.

## Nothing disappears without a reason

Every load has to reconcile: **bronze rows = silver rows + quarantined rows**, and the fact table must hold exactly as many flights as silver. Dagster shows both as checks next to the tables, so a broken join or a bad filter fails the run instead of shrinking a dashboard.

Bronze keeps every column as text, because typing belongs in silver under the contract. Bronze refuses only a *file*: one whose header has lost a column the contract needs (schema drift). A file with a *new* column is welcome, and Iceberg evolves the bronze table to hold it while old snapshots stay readable.

## Run it twice, get the same tables

Each month replaces exactly its own partition in one Iceberg transaction. Re-running a month, or loading months out of order, gives identical tables, which makes backfills boring, as they should be. Every load is also a **snapshot**, so the tables can be read as they were at any earlier load:

```text
$ lakehouse sql "SELECT count(*)
    FROM silver_flights" \
    --at silver.flights=<snapshot>
1,044,631   # right after February
```

## History that changes: SCD Type 2

BTS gives each airport a stable ID, but its code, city name and state can change. The airport dimension turns every sighting into versions with `valid_from` and `valid_to` dates (a gaps-and-islands query), and each flight joins to the airport as it was named on its own date. I rebuild it from history instead of merging changes in, so it stays correct when an older month arrives late. The tests check exactly that: they load three months in order and then backfilled, and expect the same versions, with a rename that reverts (A → B → A) becoming three versions, not two.

## Built to be checked

- **35 tests**, no network: they write small files in the real BTS layout from made-up flights, covering every kind of contract violation, duplicates, midnight written as `2400`, reloads, time travel, schema drift and the SCD Type 2 versions.
- **Dagster** runs the same functions as partitioned assets, one partition per month, with a schedule that loads the month BTS has just published.
- **Docker Compose** starts the Dagster UI, and GitHub Actions lints, tests and builds the image on every push.

## What production would change

The catalog is a SQLite file so the whole thing fits on a laptop. Pointing it at a REST, Glue or Nessie catalog and object storage changes one module, and then Spark, Trino or Snowflake can read the same tables. The patterns stay the same: contract-first silver, quarantine with reasons, partition-scoped idempotent loads and reconciliation on every run.
