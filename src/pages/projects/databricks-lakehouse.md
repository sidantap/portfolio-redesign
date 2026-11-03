---
layout: ../../layouts/Project.astro
title: Medallion lakehouse on Azure Databricks
kind: Data engineering
org: NKWD
date: '2026-03'
period: Feb 2026 – now
summary: Bronze, silver and gold pipelines on Azure Databricks for a public water utility, bringing its operational systems and SaaS tools into one modeled lakehouse, with history kept through slowly changing dimensions.
img: fig/lakehouse-architecture.svg
tags: [medallion architecture, pyspark, delta lake, scd type 2, metadata-driven ingestion, rest api pagination, azure data factory, adls gen2, key vault, ci/cd, pytest, data reconciliation, python, sql server]
links: []
---

A water utility runs on many systems that were never designed to talk to each other: customer information, work orders and assets, lab results, HR, security training, the website and the help desk. This project brings them into one lakehouse so reporting starts from a single, tested copy of the data instead of a different export for every question.

<figure><img src="../../fig/lakehouse-architecture.svg" alt="Architecture: SQL Server systems and REST APIs flow through config-driven pipelines and notebooks into bronze Delta tables, then a cleaned silver layer with reconciliation checks, then gold dimensions and facts that feed Power BI" /><figcaption>Fig. 1 · Sources to Power BI, layer by layer</figcaption></figure>

## Getting data in

There are two kinds of sources, and each gets the ingestion pattern that fits it.

- **SQL Server systems** (CIS, Lucity, LIMS, Antero) come in through **config-driven pipelines**. Each table is described once in JSON metadata, so adding a table is a config entry, not new code, and every table loads the same way.
- **REST APIs** (Paycor, KnowBe4, CivicPlus, ServiceDesk Plus) come in through **custom notebooks**, because every API authenticates and pages differently. The notebooks handle the auth and walk the pages until the data is complete.

Raw data lands in **bronze** as Delta tables, loaded incrementally rather than reloaded in full.

## Silver and gold

**Silver** cleans and conforms the data with PySpark and Delta Lake. This is also where reconciliation happens: when records go missing or appear twice between SAP and Lucity, SQL validation finds where the two disagree.

**Gold** models dimensions and facts for reporting. Dimensions use SCD Type 1 or Type 2 logic depending on whether history matters.

<figure><img src="../../fig/lakehouse-scd2.svg" alt="Illustration of SCD Type 2: when a meter changes size, the old row is closed with a valid_to date and a new current row is added" /><figcaption>Fig. 2 · SCD Type 2 in one picture (made-up rows)</figcaption></figure>

With Type 2, a change creates a new row instead of overwriting the old one, so a report about last year still sees last year's version of the record. Type 1 is for corrections, where the old value was simply wrong.

## Running it safely

Ingestion is orchestrated with **Azure Data Factory**, with storage in **ADLS Gen2** and credentials in **Key Vault** rather than in code. Changes ship through **Azure DevOps CI/CD**: pytest, black and pylint run automatically before anything deploys. When a run fails, I trace it through Data Factory and Databricks back to the step that broke.

## Around it

The same role includes SQL Server stored procedures, SSIS transformations and SQL Agent jobs for the systems that aren't in the lakehouse yet, and the Power BI work in the [Crystal Reports migration](../power-bi-modernization/).
