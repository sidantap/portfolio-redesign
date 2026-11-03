---
layout: ../../layouts/Project.astro
title: Crystal Reports to Power BI modernization
kind: Analytics engineering
org: NKWD
date: '2026-02'
period: Feb 2026 – now
summary: 40 to 50 legacy Crystal Reports rebuilt on validated SQL Server views and Power BI semantic models, plus 10 to 20 new reports built for seven departments.
impact: With the new dashboards, 20 to 40 staff hours of manual reporting removed each week
img: fig/powerbi-migration.svg
tags: [semantic modeling, star schema, dax, power query, sql server views, on-premises gateway, kpi frameworks, source-to-target mapping, power bi, crystal reports]
links: []
---

The utility's reporting lived in Crystal Reports, with the business logic buried inside each report. Each report was its own island, hard to check and hard to reuse.

## The migration pattern

Each report follows the same path, so the 40 to 50 migrations stay consistent.

<figure><img src="../../fig/powerbi-migration.svg" alt="Flow: a Crystal report's logic moves into a SQL Server view, is validated against the legacy output, modeled as a Power BI semantic model, refreshed through an on-premises gateway and shared per department" /><figcaption>Fig. 1 · One report's path from Crystal to Power BI</figcaption></figure>

1. **Move the logic into SQL.** The calculation that lived inside the Crystal report becomes a SQL Server view, where it can be read, tested and reused.
2. **Validate it.** The new view is checked against what the legacy report produced before anyone relies on it.
3. **Model it.** The view feeds a Power BI semantic model with DAX measures.
4. **Keep it fresh.** On-premises gateways and scheduled refresh keep the data current.
5. **Share it.** Workspace access and distribution are set per department.

Along the way I fixed reports that ran in the designer but failed inside Lucity Web.

<figure><img src="../../fig/powerbi-star.svg" alt="Illustrative star schema: a fact table in the middle with date, department, asset, customer and status dimensions around it" /><figcaption>Fig. 2 · The model shape the reports are rebuilt on (illustrative)</figcaption></figure>

## New reports

On top of the migration, I built 10 to 20 new Power BI reports and data models on my own for HR, Legal, Engineering, IT, Customer Service, Finance and Operations. The work included KPI frameworks, dimensional models and source-to-target mappings across SAP, HR, Finance and Engineering data, so a number on a page can be traced back to where it came from.

## Impact

Together, the migration and the new dashboards remove 20 to 40 hours of manual reporting a week across departments.
