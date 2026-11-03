---
layout: ../../layouts/Project.astro
title: Clinical study experience map
kind: Data integration
org: Medpace
date: '2024-11'
period: Aug – Dec 2024
summary: An interactive R Shiny map of where clinical studies run worldwide, combining several sources into one view for research and proposal work.
impact: Replaced repeated manual assembly of study experience
img: fig/clinical-world.svg
tags: [geospatial visualization, data integration, data validation, clinical trial data, snowflake, dbt, sql, medidata, python, r, r shiny]
links: []
---

<figure><img src="../../fig/clinical-world.svg" alt="World map with circles sized by number of studies per country, largest in the United States and Europe" /><figcaption>Fig. 1 · What the map shows (illustrative sites and counts, not Medpace data)</figcaption></figure>

When a clinical research organization bids on a new trial, the proposal has to show where it has run similar studies before. That experience was spread across several sources and pulled together by hand for every request.

## Before and after

| | Before | After |
|---|---|---|
| **Where the answer lived** | Several separate sources | One map |
| **How it was assembled** | By hand, again for each proposal | Once, in the data layer |

## What made it work

The hard part wasn't the map, it was getting several sources into one consistent view. The data behind it came from Medidata and other clinical systems, with the transformation work in SQL on Snowflake and cleaning and validation in Python, SQL and R.

## The rest of the role

The map sat on the same foundation as the rest of my Medpace work: dbt and SQL transformations on Snowflake, millions of clinical trial records cleaned and validated, Power BI dashboards for analysts and leadership, and monthly dashboard design sessions I led for 10+ analysts in the US and UK.
