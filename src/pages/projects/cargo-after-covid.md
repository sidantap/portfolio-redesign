---
layout: ../../layouts/Project.astro
title: Cargo After COVID
kind: Data analysis
org: Personal · live app
date: '2025-12'
period: Jul – Dec 2025
summary: An interactive R Shiny app on Bureau of Transportation Statistics data that tracks U.S. air cargo from 2003 to 2025, so anyone can see what the pandemic did to it, and what came after.
impact: Two decades of federal air cargo data, explorable in a few clicks
img: fig/cargo-trend.svg
tags: [exploratory data analysis, time series, seasonality, rolling averages, kpi design, data wrangling, federal open data, bts, r, r shiny, shinyapps.io]
links:
  - { t: Open the app, href: 'https://sidantap.shinyapps.io/CargoAfterCOVID/' }
---

Passenger flights collapsed in 2020. Cargo did something very different, and the federal data shows it plainly, if you can get at it. The Bureau of Transportation Statistics publishes it as large tables that are hard to read. This app makes them explorable.

<figure><img src="../../fig/cargo-trend.svg" alt="Line chart of monthly U.S. air carrier cargo ton-miles from 2003 to 2026, international above domestic, both rising sharply through 2020 and 2021 and settling higher than before" /><figcaption>Fig. 1 · The story in one chart: published BTS monthly series, 12-month averages in bold</figcaption></figure>

## Reading the chart

Some of what the data shows, computed from the BTS series in Fig. 1:

- **Cargo didn't fall in 2020, it rose.** Total U.S. air carrier cargo grew from about 43,500 million ton-miles in 2019 to about 52,500 million in 2021, roughly **+21%** in two years.
- **Both markets moved together.** Domestic cargo rose about 23% from 2019 to 2021, international about 20%.
- **It settled higher than before.** In 2025 the total was still about **12% above 2019**, a new level rather than a spike that fully reversed.
- **The last shock looked different.** In the 2008–09 recession, international cargo fell about 21% from 2007 to 2009. COVID hit passengers, not freight.
- **Months swing a lot.** The thin monthly lines move up and down within every year, with peaks most often in the fall and late winter, so the chart uses 12-month averages to show the trend underneath.

## What the app does

- **Transforms** two decades of BTS tables, 2003 to 2025, into tidy data in R, so years and markets compare cleanly.
- **Computes KPIs** that summarize cargo performance.
- **Filters and trend views** let anyone choose what to compare and see the long run, pre- and post-COVID, without touching a spreadsheet.

## Publishing it

The app is written in R Shiny and hosted on shinyapps.io, so it opens in any browser with nothing to install.
