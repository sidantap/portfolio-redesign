---
layout: ../../layouts/Project.astro
title: FAA drug and alcohol testing randomizer
kind: Application
org: Atlas Air
date: '2025-09'
period: May – Dec 2025
summary: An in-house R Shiny app that randomly selects employees for FAA-mandated drug and alcohol testing, replacing a paid third-party process.
impact: Covers every FAA-regulated employee and meets all FAA guidelines
img: fig/faa-selection.svg
tags: [random sampling, rollover logic, deduplication, regulatory compliance, microsoft graph api, oauth 2.0, audit logging, r shiny, sharepoint]
links: []
---

FAA-regulated employers must randomly test a set share of their safety-sensitive employees for drugs and alcohol every year, from pilots to ground crew. The draw has to be random, every eligible person has to be in the pool, and the employer has to be able to show an inspector exactly what happened. This app does that in-house.

<figure><img src="../../fig/faa-selection.svg" alt="Flow: master list to eligible pool, quarterly target with rollover, random drug-and-alcohol and drug-only draws, deduplication, and results written to SharePoint" /><figcaption>Fig. 1 · One quarter of selections</figcaption></figure>

## The rules it encodes

- **Eligibility.** A master employee list becomes the quarter's eligible pool.
- **Targets.** Annual and quarterly targets come from the testing rates, with completed-test counts tracked against them.
- **Rollover.** Tests that were selected but not completed carry into the next quarter.
- **Two categories.** Drug-and-alcohol and drug-only selections are drawn separately.
- **Deduplication.** Each draw is checked against prior selections and prior-quarter history.

## Connected to SharePoint

The app reads and writes master data, results, history, audit logs and settings in SharePoint through the **Microsoft Graph API**, authenticated with **Azure AD and OAuth 2.0**. I also troubleshot token expiration along the way. The program manager gets Excel exports and compliance KPIs.

## What I owned

The whole lifecycle: requirements, architecture, build, validation, deployment, documentation and training.

## Impact

It covers every FAA-regulated employee, meets every FAA guideline, and reduced the company's reliance on a paid third-party system.
