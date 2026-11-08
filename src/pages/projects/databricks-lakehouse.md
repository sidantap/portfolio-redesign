---
layout: ../../layouts/Project.astro
title: Medallion lakehouse on Azure Databricks
kind: Data engineering
org: NKWD
date: '2026-03'
period: Feb 2026 – now
summary: Bronze, silver and gold pipelines on Azure Databricks that bring a public utility's operational databases and SaaS tools into one tested, modeled lakehouse, with history kept through slowly changing dimensions.
img: fig/lakehouse-config.svg
tags: [medallion architecture, lakehouse, pyspark, delta lake, acid transactions, metadata-driven ingestion, incremental loads, watermarking, idempotent pipelines, upserts, scd type 1, scd type 2, dimensional modeling, rest api pagination, azure data factory, adls gen2, key vault, azure devops ci/cd, pytest, data reconciliation]
links: []
---

A utility runs on many systems that were never built to talk to each other: operational databases on SQL Server and a handful of SaaS tools with their own APIs. Reporting used to start from a different export for every question. This lakehouse gives every report one tested starting point. Below are the engineering ideas it rests on, without the internal details.

## Configuration, not code

Most sources are relational tables, and relational tables all look alike to a pipeline. So they share one: each table is described once in metadata (where it lives, its keys, how to detect what changed, what history to keep), and a single generic pipeline loads whatever it's pointed at.

<figure><img src="../../fig/lakehouse-config.svg" alt="A JSON config for a table, and the four steps it drives: the orchestrator reads it, loads bronze incrementally, builds silver deduplicated on the key, and a gold SCD 2 dimension" /><figcaption>Fig. 1 · One config entry drives a table through every layer (illustrative names)</figcaption></figure>

The payoff is consistency. A new table is a reviewed config change, not a new pipeline, and every table gets the same incremental logic, typing, deduplication and logging for free.

APIs are the exception: each one authenticates and paginates differently, so they get purpose-built notebooks that handle tokens and walk every page until the result is complete.

## Loading only what changed

Full reloads don't scale and hide mistakes. Each source keeps a **watermark**, the latest change already loaded, and each run asks only for what's newer. The loads are **idempotent**: re-running a window produces the same result instead of duplicates, because silver applies changes as **upserts** on the business key rather than blind appends. That makes failures cheap: fix the cause, re-run, done.

## Bronze, silver, gold

| Layer | Job | Rule |
|---|---|---|
| **Bronze** | Land data exactly as the source sent it | Never edited, so any number can be traced back |
| **Silver** | Type, clean, deduplicate and conform | One current, trustworthy row per entity |
| **Gold** | Facts and dimensions shaped for questions | History kept where it matters (SCD) |

Everything is stored as **Delta Lake** tables, which gives each write an ACID transaction: a failed run never leaves a table half-written, and readers always see a consistent version.

## Keeping history

<figure><img src="../../fig/lakehouse-scd2.svg" alt="Timeline: an asset's old version ends and a new version begins; a reading from before the change joins to the old version, one after it to the new" /><figcaption>Fig. 2 · SCD Type 2 on a timeline (made-up rows)</figcaption></figure>

With **Type 2**, a change closes the old row and adds a new one, so a report about last year still sees last year's version of the record. **Type 1** overwrites in place, for corrections where the old value was simply wrong. Choosing per attribute keeps history where it matters without bloating the tables.

## Trust, and how it's checked

- **Reconciliation.** Counts and keys are compared between source systems and the lakehouse, so missing or duplicated records surface before they reach a report.
- **Secrets** live in a key vault, never in code or config.
- **CI/CD.** Every change ships through a pipeline that runs unit tests and code-quality checks first; nothing is edited by hand in production.
- **Observability.** When a run fails, the orchestrator's logs point to the exact step and table, so the fix starts from evidence rather than guesswork.

## On top of it

The same role covers the SQL Server side (stored procedures, SSIS and scheduled jobs) and the Power BI layer people actually open: 10 to 20 reports for seven departments, plus 40 to 50 legacy Crystal Reports migrated, saving 20 to 40 staff hours a week.
