---
layout: ../../layouts/Project.astro
title: Emissions and regional profitability dashboards
kind: Business analytics
org: Motus Freight
date: '2024-06'
period: Jan – Aug 2024
summary: "Tableau Cloud dashboards on data from Turvo, the company's transportation platform, for two questions every freight broker has: where do our emissions come from, and where do we actually make money?"
impact: Contributed to 12.4% lower emissions and 15% higher profitability
img: fig/motus-tree.svg
tags: [kpi design, kpi trees, profitability analysis, unit economics, forecasting, trend analysis, emissions analytics, sustainability reporting, data visualization, tableau cloud, turvo]
links: []
---

A freight brokerage moves loads through many carriers across the country. I built the dashboards that answer two questions.

## Question 1: where do we make money?

"Profitable" is too vague to act on, so the first step was breaking it down into numbers someone can move.

<figure><img src="../../fig/motus-tree.svg" alt="KPI tree: gross profit splits into revenue, margin and carrier cost, which feed views by customer, by region, by carrier and a revenue forecast" /><figcaption>Fig. 1 · The KPI tree behind the profitability views</figcaption></figure>

Each leaf became a view:

- **By customer:** profitability scorecards built from P&L data.
- **By region:** a dashboard comparing gross profit across **4 regions and 49 states**.
- **By carrier:** revenue forecasting for top and lower-ranked carriers.

The regional dashboard contributed to a **15% rise in overall profitability**.

## Question 2: where are emissions heading?

<figure><img src="../../fig/motus-forecast.svg" alt="Line chart of an emissions index with history in black and a dashed forecast with a widening range" /><figcaption>Fig. 2 · The shape of the trend and forecast view (illustrative values)</figcaption></figure>

A Tableau Cloud CO2 dashboard built on carrier and transportation data from Turvo, with trend analysis and forecasting, so the team could see where emissions were heading, not just where they'd been. It contributed to a **12.4% overall drop in emissions**.
