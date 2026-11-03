---
layout: ../../layouts/Project.astro
title: FAA drug and alcohol testing randomizer
kind: App
org: Atlas Air
date: '2025-09'
period: May – Dec 2025
summary: An in-house R Shiny app that randomly selects employees for FAA-mandated drug and alcohol testing, replacing a third-party process.
impact: Covers every FAA-regulated employee and meets all FAA guidelines
tags: [r shiny, microsoft graph, sharepoint, oauth, compliance]
links: []
---

## What it is

An R Shiny app that randomly selects employees for FAA-mandated drug and alcohol testing, covering everyone regulated, from pilots to ground crew. I owned it end to end: requirements, architecture, build, validation, deployment, documentation and training.

## The rules it encodes

Master and quarterly eligible pools, drug-and-alcohol versus drug-only categories, annual and quarterly targets, completed-test counts, rollover, deduplication against prior selections, and prior-quarter history.

## Connected to SharePoint

The app reads and writes master data, results, history, audit logs and settings in SharePoint through Microsoft Graph, with Azure AD and OAuth 2.0. Users get Excel exports and compliance KPIs.

## Impact

It covers every FAA-regulated employee, meets every FAA guideline, and reduced reliance on a paid third-party system.
