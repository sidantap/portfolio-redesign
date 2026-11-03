---
layout: ../../layouts/Project.astro
title: Medallion lakehouse on Azure Databricks
kind: Pipeline
org: NKWD
date: '2026-03'
period: Feb 2026 – now
summary: Bronze, silver and gold pipelines on Azure Databricks for a public water utility, loading its operational systems and SaaS tools incrementally into one modeled lakehouse.
tags: [azure databricks, pyspark, delta lake, azure data factory, ci/cd, data quality, python, sql server]
links: []
---

## What it does

Medallion (bronze, silver, gold) pipelines on Azure Databricks with PySpark and Delta Lake. Raw data loads incrementally, and the gold layer models dimensions and facts with SCD Type 1 and 2 logic.

## Getting data in

SQL Server sources (CIS, Lucity, LIMS, Antero) come in through config-driven JSON pipelines, so a new table is a config entry rather than new code. REST APIs (Paycor, KnowBe4, CivicPlus, ServiceDesk Plus) come in through custom notebooks that handle auth and pagination.

## Running it

Ingestion is orchestrated with Azure Data Factory, ADLS Gen2 and Key Vault, and deployed through Azure DevOps CI/CD with automated pytest and code-quality checks (black, pylint). When a run fails, I trace it in Data Factory and Databricks, and reconcile missing or duplicate records across SAP and Lucity with SQL validation.

## Stack

Azure Databricks, PySpark, Delta Lake, Azure Data Factory, ADLS Gen2, Key Vault, SQL Server, Azure DevOps, pytest.
