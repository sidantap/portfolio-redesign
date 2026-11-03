---
layout: ../../layouts/Project.astro
title: Cargo After COVID
kind: Data analysis
org: Personal · live app
date: '2025-12'
period: Jul – Dec 2025
summary: An interactive R Shiny app on Bureau of Transportation Statistics data that tracks U.S. air cargo performance from 2003 to 2025, before, during and after the pandemic.
img: fig/cargo-flow.svg
tags: [exploratory data analysis, time series, kpi design, data transformation, federal open data, r shiny, shinyapps.io]
links:
  - { t: Open the app, href: 'https://sidantap.shinyapps.io/CargoAfterCOVID/' }
---

## The question

COVID upended air travel. What happened to cargo? How did U.S. air cargo actually perform before, during and after 2020, and has it settled into a new normal? The Bureau of Transportation Statistics publishes the data, but as large federal tables that are hard to read.

<figure><img src="../../fig/cargo-flow.svg" alt="Flow: BTS tables are cleaned and reshaped in R, KPIs are computed, then filters and trend views make them explorable in an R Shiny app on shinyapps.io" /><figcaption>Fig. 1 · From federal tables to an app</figcaption></figure>

## What I built

- **Transformations** that turn two decades of BTS tables, 2003 to 2025, into tidy data ready to compare across years.
- **KPIs** that summarize cargo performance, computed in R.
- **Filters and trend views** so anyone can pick what to compare and see the long-run trend, pre- and post-COVID, in a few clicks.

## Publishing it

The app runs on shinyapps.io, so anyone can open it in a browser without installing anything.
