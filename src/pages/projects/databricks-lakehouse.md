---
layout: ../../layouts/Project.astro
title: Medallion lakehouse on Azure Databricks
kind: Data engineering
org: NKWD
date: '2026-03'
period: Feb 2026 – now
summary: Bronze, silver and gold pipelines on Azure Databricks that bring a public water utility's operational systems and SaaS tools into one modeled lakehouse, with history kept through slowly changing dimensions.
img: fig/lakehouse-config.svg
tags: [medallion architecture, lakehouse, pyspark, delta lake, metadata-driven ingestion, incremental loads, scd type 1, scd type 2, dimensional modeling, rest api pagination, azure data factory, adls gen2, key vault, azure devops ci/cd, pytest, black, pylint, data reconciliation, sql server, ssis]
links: []
---

A water utility runs on many systems that were never built to talk to each other: customer information, work orders and assets, lab results, HR, security training, the website and the help desk. Reporting used to start from a different export for every question. This project gives it one tested starting point.

## Two kinds of sources, two patterns

**SQL Server systems** (CIS, Lucity, LIMS, Antero) all look alike to a pipeline, so they share one. Each table is described once in JSON metadata, and a single generic Data Factory pipeline loads any table it's pointed at.

<figure><img src="../../fig/lakehouse-config.svg" alt="A JSON config for a work orders table, and the four steps it drives: Data Factory reads it, loads bronze incrementally, builds silver deduplicated on the key, and a gold SCD 2 dimension" /><figcaption>Fig. 1 · One config entry drives a table through every layer (illustrative names)</figcaption></figure>

**REST APIs** (Paycor, KnowBe4, CivicPlus, ServiceDesk Plus) don't fit one template: each authenticates and pages differently. They get custom notebooks that handle the auth and walk every page until the data is complete.

## Bronze, silver, gold

| Layer | What happens |
|---|---|
| **Bronze** | Raw Delta tables, loaded incrementally rather than in full |
| **Silver** | Cleaned and conformed with PySpark; records reconciled across SAP and Lucity with SQL validation |
| **Gold** | Dimensions and facts for reporting, with SCD Type 1 or Type 2 per attribute |

## Keeping history

<figure><img src="../../fig/lakehouse-scd2.svg" alt="Timeline: a meter's 5/8 inch version ends in April 2026 and a 1 inch version begins; a reading from August 2025 joins to the old version, one from September 2026 to the new" /><figcaption>Fig. 2 · SCD Type 2 on a timeline (made-up rows)</figcaption></figure>

With **Type 2**, a change adds a new row and closes the old one, so a report about last year still sees last year's version of the record. **Type 1** overwrites in place, for corrections where the old value was simply wrong. Choosing per attribute keeps history where it matters without bloating the tables.

## Guardrails

- **Secrets** live in Key Vault, not in code; storage is ADLS Gen2.
- **Every change** ships through Azure DevOps CI/CD, with pytest, black and pylint run automatically first.
- **When a run fails**, I trace it through Data Factory and Databricks back to the step that broke.
- **Around the lakehouse**, I write SQL Server stored procedures, SSIS transformations and SQL Agent jobs, and build the Power BI reports on top: 10 to 20 for seven departments, plus 40 to 50 legacy Crystal Reports migrated, saving 20 to 40 staff hours a week.
