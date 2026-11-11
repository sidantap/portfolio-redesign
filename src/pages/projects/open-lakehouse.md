---
layout: ../../layouts/Project.astro
title: An open-source lakehouse for US flight data
kind: Data engineering
org: Personal · open source
date: '2026-11'
period: Nov 2026
summary: My work lakehouse runs on Databricks. I rebuilt the same bronze, silver and gold pattern with open-source tools (Apache Iceberg, DuckDB and Dagster), loaded six months of US flight data into it, and built a five-page operations report on top.
impact: 3,446,676 flights downloaded, loaded and checked in 2 minutes 16 seconds; one bad row caught and quarantined, and every load reconciled
img: img/open-lakehouse.jpg
tags: [apache iceberg, duckdb, dagster, data contracts, medallion architecture, data quarantine, schema evolution, scd type 2, star schema, audit logging, echarts, python, sql, docker, pytest]
links:
  - { t: Live report, href: 'https://sidantap.github.io/portfolio-redesign/lakehouse/' }
  - { t: Code and README, href: 'https://github.com/sidantap/open-lakehouse' }
---

At work our lakehouse runs on Databricks, which handles the table format, the catalog and the scheduler for you. I wanted to check that I understood the pattern itself and not just the product, so I rebuilt it from open-source parts and fed it public data: every scheduled domestic flight that US airlines report to the Bureau of Transportation Statistics (BTS). Six months of 2025 comes to 3.45 million rows.

## How it's built

<figure><img src="../../fig/open-lakehouse-architecture.svg" alt="Data flow: BTS zip files land once, load to a bronze Iceberg table, are checked against a data contract into silver with a quarantine table, then modeled into a gold star schema, marts and report tables" /><figcaption>Fig. 1 · Data flow, one partition per month</figcaption></figure>

| Layer | What it holds | How it loads |
|---|---|---|
| Landing | The monthly zip from BTS and a manifest (URL, size, SHA-256, download time) | Downloaded once, never changed |
| Bronze | All 110 columns as text, plus the source month, row number and batch id | Overwrites its own month only |
| Silver | The 38 contract columns, typed, plus a few derived ones (47 in all); a quarantine table for rows that failed | Same: one month at a time |
| Gold | Fact and dimension tables, marts, and three summary tables for the report | Rebuilt from silver each run (about 4 s) |
| Ops | `ops.load_audit`: one row per stage, per month, per run | Appended, including failures |

The tables are Apache Iceberg (Parquet files plus metadata), so every load is a snapshot I can query later. DuckDB runs all the SQL, and Dagster schedules the loads with one partition per month.

## The data contract

The silver table is defined in one YAML file. For each column it lists the source column, the type and any limits; then come a few rules that span columns, such as "a cancelled flight has a cancellation reason" and "when BTS reports delay causes, they add up to the minutes the flight was late". A small compiler turns the file into one DuckDB query with 98 named checks, plus a duplicate-key check.

A row that fails any check isn't dropped or fixed. It goes to a quarantine table with the names of the checks it failed and its raw values. Every month has to reconcile (bronze rows = silver rows + quarantined rows), and if more than 0.5% of a month fails, nothing is written and the run stops.

Real BTS data turned out to be very clean. In six months the contract rejected one row:

| | |
|---|---|
| Flight | PSA Airlines 5292, Charlotte → Knoxville, 30 March 2025 |
| Distance | 177 miles |
| Scheduled | 22:49 → 23:59 |
| Scheduled duration in the file | 1,510 minutes (about 25 hours) |
| Failed check | `max:crs_elapsed_min` |

It's almost certainly meant to be 70 minutes, but deciding that isn't the pipeline's job. To check the rules that real data never triggers, the tests feed in 16 kinds of invented bad rows.

## The report

The report is the part a business user would see. It has five pages: an executive summary with month-on-month changes, carrier performance, airports and routes, delay analysis, and a data operations page. Slicers for month range, carrier, state and airport filter every visual.

To make filtering work in a static page, gold includes three summary tables that hold only counts and sums, never rates: for example flights, on-time arrivals and delay minutes per month, carrier and airport. The browser adds up whatever the filters select and only then divides. Averaging rates that were already averaged would give the wrong answer; summing counts can't.

The data operations page is built from the pipeline's own metadata: the audit table, each Iceberg table's snapshot log, file counts and sizes, and the result of every contract check.

## Numbers

<figure><img src="../../fig/open-lakehouse-load-times.svg" alt="Stacked bars of seconds per month: download from BTS between 11 and 19 seconds, bronze and silver about 3 seconds each" /><figcaption>Fig. 2 · Time to land and load each month</figcaption></figure>

The download from BTS is most of the time, and it varies: 11 to 19 seconds a month in this run, up to 38 in an earlier one. Bronze and silver each take about 3 seconds for some 600,000 rows. The timings come from the audit table.

<figure><img src="../../fig/open-lakehouse-storage.svg" alt="Horizontal bars: 1,559 MB of CSV, 174 MB zipped, 104 MB bronze, 145 MB silver, 94 MB fact table" /><figcaption>Fig. 3 · The same six months at each stage</figcaption></figure>

I expected silver to be smaller than bronze, and it isn't. When I looked at the Parquet column sizes, a 16-character hash key I'd added to silver took 32 MB on its own, 22% of the table, because random hex doesn't compress. The natural key columns are already in the table, so next time I'd leave the hash out.

## What the data showed

<figure><img src="../../fig/open-lakehouse-otp.svg" alt="Line chart of monthly on-time arrival rate for Southwest, Delta, American and SkyWest and all carriers, January to June 2025, all falling in May and June" /><figcaption>Fig. 4 · On-time arrival rate, four largest carriers</figcaption></figure>

Across all 14 carriers, 78.1% of completed flights arrived less than 15 minutes late. That held around 80% from January to April, then dropped to 76.4% in May and 71.7% in June, with every large carrier falling. The carriers ranged from Hawaiian at 84.0% to PSA at 70.1%.

<figure><img src="../../fig/open-lakehouse-delays.svg" alt="Histogram of arrival delay in five-minute bins, peaking just before scheduled time, with a long tail past four hours" /><figcaption>Fig. 5 · Arrival delay of 3.4 million completed flights</figcaption></figure>

Most flights arrive early: schedules are padded. The tail is long, though: 8% of completed flights were an hour or more late. The single biggest cause of delay minutes was a late-arriving aircraft (38%), meaning the delay came from an earlier flight. The report's hour-by-weekday heatmap shows the same knock-on effect: delays build through the day and peak in the evening.

## Problems I hit

- **DuckDB 2.0 broke two things.** The old lambda syntax was deprecated and a function I used was renamed. I pinned the version.
- **Partitioning by month needed an extra package** (`pyiceberg-core`) before PyIceberg would write.
- **A replace is two snapshots in PyIceberg**: a delete and then an append, committed together. Readers never see the gap, but it shows up in the history.
- **0/0 gives NaN in DuckDB, not NULL.** A test with a carrier whose flights were all cancelled caught it.
- **The airport reference data was ahead of BTS.** OurAirports already lists Palm Beach under its new code (DJT); BTS still reports PBI.
- **My first timings were wrong.** I recorded durations in snapshot properties, which are set before the write happens, so the write was left out. That's why the audit table exists.

## What I'd change

The SQLite catalog allows one writer at a time; a shared setup would use a REST or Glue catalog with object storage, and only one module would change. Gold is rebuilt in full every run, which takes seconds now but wouldn't with years of data, so the fact table would need to load incrementally. Flight times are local to each airport with no time zones, which is fine for "hour of day" but not for anything that crosses time zones.
