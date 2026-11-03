---
layout: ../../layouts/Project.astro
title: FAA drug and alcohol testing randomizer
kind: Compliance application
org: Atlas Air
date: '2025-09'
period: May – Dec 2025
summary: An in-house R Shiny app that randomly selects employees for FAA-mandated drug and alcohol testing, covering every regulated employee and replacing a paid third-party process.
impact: Covers every FAA-regulated employee and meets all FAA guidelines
img: fig/faa-funnel.svg
tags: [random sampling, regulatory compliance, 14 cfr part 120, rollover logic, deduplication, eligibility rules, microsoft graph api, azure ad, oauth 2.0, audit logging, sharepoint, r shiny, excel exports]
links: []
---

FAA-regulated employers must randomly test a set share of their safety-sensitive employees every year, from pilots to ground crew. The draw has to be genuinely random, every eligible person has to be in the pool, and the employer has to be able to show an inspector exactly what happened. I built an app that does this in-house, and owned it end to end: requirements, architecture, build, validation, deployment, documentation and training.

<figure><img src="../../fig/faa-funnel.svg" alt="Funnel from all employees to safety-sensitive to active this quarter, beside quarterly bars of drug tests where later quarters carry a small rollover on top" /><figcaption>Fig. 1 · Who can be selected, and how many each quarter (illustrative numbers)</figcaption></figure>

## The rules, and how the app enforces them

| Rule | What the app does |
|---|---|
| Only eligible people can be drawn | Builds the quarter's eligible pool from the master employee list |
| Annual targets must be met | Turns the yearly testing rates into annual and quarterly targets and tracks completed tests against them |
| Missed tests still count against the target | **Rollover:** tests selected but not completed carry into the next quarter |
| Drug and alcohol testing differ | Draws the drug-and-alcohol and drug-only categories separately |
| No double-counting | **Deduplicates** each draw against prior selections and prior-quarter history |
| Everything must be provable | Writes results, history and an audit log for every run |

## Wiring it to SharePoint

The company's master data lived in SharePoint, so the app reads and writes there through the **Microsoft Graph API**, authenticated with **Azure AD and OAuth 2.0**: master data, results, history, audit logs and settings. I also troubleshot token expiration along the way. The program manager gets Excel exports and compliance KPIs.

## Result

The app covers every FAA-regulated employee, meets every FAA guideline, and reduced the company's reliance on a paid third-party system.
