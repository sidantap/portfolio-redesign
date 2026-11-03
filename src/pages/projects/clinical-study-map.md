---
layout: ../../layouts/Project.astro
title: Clinical study experience map
kind: Data integration
org: Medpace
date: '2024-11'
period: Aug – Dec 2024
summary: An interactive R Shiny map of where clinical studies run worldwide, combining several sources into one view for research and proposal work.
impact: Replaced repeated manual assembly of study experience
img: fig/clinical-map.svg
tags: [geospatial visualization, data integration, data validation, snowflake, sql, medidata, python, r shiny]
links: []
---

## The problem

When a clinical research organization bids on a new trial, the proposal has to show where it has run similar studies before. That experience was spread across several sources and pulled together by hand for each request.

<figure><img src="../../fig/clinical-map.svg" alt="Flow: Medidata and other study sources are integrated with SQL and Snowflake, cleaned and validated, and shown in an R Shiny map used by research and proposal teams" /><figcaption>Fig. 1 · Several sources, one map</figcaption></figure>

## What I built

An interactive R Shiny map of where clinical studies run around the world. It combines the sources into one standardized view, so the research and proposal teams can answer "where have we done this before?" without assembling it again by hand.

## The data work behind it

The map sits on the same foundation as the rest of my Medpace work: dbt and SQL transformations on Snowflake, data pulled from Medidata, and millions of clinical trial records cleaned and validated with Python, SQL and R. I also built Power BI dashboards on Snowflake and led monthly dashboard design sessions for 10+ analysts in the US and UK.
