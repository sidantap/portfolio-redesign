---
layout: ../../layouts/Project.astro
title: Freight dashboards for profit, customers and emissions
kind: Business analytics
org: Motus Freight
date: '2024-06'
period: Jan – Aug 2024
summary: "Four Tableau dashboards for a freight brokerage, built on data from Turvo, its transportation platform: where the loads are, which customers and regions make money, and how much CO2 each carrier puts out."
impact: Contributed to 12.4% lower emissions and 15% higher profitability
img: img/motus-regional.webp
tags: [kpi design, kpi trees, profitability analysis, customer segmentation, geospatial analysis, rolling averages, conditional formatting, forecasting, trend analysis, emissions analytics, sustainability reporting, tableau, turvo]
links: []
---

A freight brokerage moves loads through many carriers across the country. I built four dashboards that answer the questions the business kept asking. Figures in the screenshots are blurred or marked confidential.

## 1 · Where do we make money?

"Profitable" is too vague to act on, so the first step was breaking it into numbers someone can move.

<figure><img src="../../fig/motus-tree.svg" alt="KPI tree: gross profit splits into revenue, margin and carrier cost, which feed views by customer, by region, by carrier and a revenue forecast" /><figcaption>Fig. 1 · The KPI tree behind the profitability views</figcaption></figure>

The **Regional Performance** dashboard follows that tree. It opens on gross profit year to date by month, maps every state shaded by gross profit, and breaks the country into West, Mid-West, South and North, each with its leading carriers, customers and market areas. Select a region or state and everything filters to it.

<figure><img src="../../img/motus-regional.webp" alt="Regional Performance dashboard: monthly gross profit bars for 2024, a U.S. map shaded by gross profit, and four region cards with their own maps" /><figcaption>Fig. 2 · Regional Performance: 4 regions, 49 states (values blurred)</figcaption></figure>

It contributed to a **15% rise in overall profitability**.

## 2 · Which customers are slipping?

The **Customer Scorecard** tracks each account's average gross profit, total shipments and 4-, 8- and 12-week averages, with **conditional formatting** that flags accounts above or below set thresholds. Pick an account and a weekly trend line of average net revenue shows where it's heading, compared with the others.

<figure><img src="../../img/motus-scorecard.webp" alt="Customer Scorecard: a table of accounts with rolling averages and flags, above a weekly net revenue trend line per account" /><figcaption>Fig. 3 · Customer Scorecard (values marked confidential)</figcaption></figure>

## 3 · Where are the loads?

**City Ranking Insights** ranks the top origin and destination states by reefer loads, shows total shipments and the monthly average, and shades the heaviest operating regions on a map, for routing and resource decisions.

<figure><img src="../../img/motus-city-ranking.webp" alt="City Ranking Insights: ranked lists of origin and destination states either side of a U.S. map shaded by shipment volume" /><figcaption>Fig. 4 · City Ranking Insights</figcaption></figure>

## 4 · How much CO2, and from whom?

The **CO2 Emissions** dashboard brings together miles traveled, fuel used, fuel cost and CO2 for each carrier, with trends over time, bar charts by carrier and a scatter plot of miles against emissions, so outliers stand out. It contributed to a **12.4% overall drop in emissions**.

<figure><img src="../../img/motus-co2.webp" alt="CO2 Emissions dashboard: a carrier table with miles, fuel and CO2, and a scatter plot of miles against emissions" /><figcaption>Fig. 5 · CO2 Emissions Tracking (values marked confidential)</figcaption></figure>
