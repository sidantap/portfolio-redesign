---
layout: ../../layouts/Post.astro
title: A data pipeline that runs every night for $0
kind: Case
date: '2026-10-20'
minutes: 7
draft: true
summary: Cincinnati 311 requests, NOAA weather and NHTSA vehicle complaints, loaded incrementally, tested with dbt and modeled into a star schema every night on GitHub Actions, with a small classifier scored against labels it has never seen.
tags: [data engineering, dbt, duckdb, github actions, data quality]
---

At work most of my pipelines run on Azure Databricks against systems I can't show anyone. So I built one I can: a small pipeline that does the same jobs on public data, runs every night, and publishes what it did. It costs nothing to run.

## The question

Could I build the whole path, from three messy public sources to a dashboard, with the habits I use at work: incremental loads, a raw layer nobody edits, tests that stop the run, a quarantine for bad rows, and a record of every run? And could it run on free tools, unattended, every night?

## The sources

Three public sources, each messy in its own way:

- **Cincinnati 311 service requests** from the city's Socrata API. Requests change after they're created: they get closed, reopened and re-categorized.
- **NOAA daily weather** at the CVG airport station. NOAA revises recent days as late observations arrive.
- **NHTSA vehicle complaints**, the federal file of complaints drivers send in, each with a free-text description and a component tag.

## Loading only what changed

Each source keeps a watermark: the newest record already loaded. A run asks only for rows after that watermark, minus an overlap to catch late changes: two days for 311, seven for weather and three for complaints. 311 is read in 20,000-row pages on `date_last_update`, one indexed filter that catches both new and changed requests.

Rows land unchanged in a **bronze** layer first. Nothing is cleaned on the way in, so any number on the dashboard can be traced back to exactly what the API returned.

## Clean, test, quarantine

dbt builds the **silver** layer: one current version of each request, typed and conformed. Rows that break a rule don't get fixed silently and don't get dropped. They go to a quarantine table with the reason, for example a request closed before it was created, a missing location, or a location outside the city. So far that's about 136 rows, nearly all of them closed before they were created.

Then the tests run: unique and non-null keys on every table, accepted values for statuses and categories, relationships from every fact row to its dimensions, and no negative days-to-close. If a test fails, the run fails and the dashboard keeps yesterday's numbers.

The **gold** layer is a star schema: a service request fact, request type and date dimensions, and a daily table that joins requests to the weather.

## A model scored every night

NHTSA complaints come with a component tag, which makes them an answer key. A small open-source embedding model (bge-small) turns each description into a vector, and a logistic regression predicts which of 13 parts of the car it's about. It was trained on complaints received before July 1, 2026, and scored 84.7% on a held-out test set. Every night it classifies the new complaints and is scored against NHTSA's own tags. Live accuracy sits around 80%.

<figure><img src="../../img/nightly-model.jpg" alt="The complaint model page of the dashboard: live accuracy by night, model details and F1 score by component" /><figcaption>The model page: accuracy on new complaints each night, and F1 by component</figcaption></figure>

## Running it for free

GitHub Actions runs everything at 07:17 UTC, about 3 a.m. in Cincinnati. The warehouse is a single DuckDB file, gzipped and kept as a GitHub release asset between runs: download it, run the pipeline, upload it again. The dashboard is a static page on GitHub Pages that reads one JSON file the run writes. A normal night finishes in under a minute.

<figure><img src="../../img/nightly-overview.jpg" alt="The Nightly 311 dashboard overview with KPI tiles and a chart of requests per day" /><figcaption>The dashboard the run publishes every night</figcaption></figure>

## What went wrong

The first three runs failed. The first backfill tried to pull too much 311 history at once and the API timed out, so I added retries and shortened the first backfill to 30 days, and 7 for complaints. A request with no type broke a dimension key, which now gets an explicit UNKNOWN. Each fix is in the run history.

## What I took from it

The parts that make a pipeline trustworthy are mostly small: a watermark, an overlap, a raw layer, a test that's allowed to fail the run. None of them needed a big platform. They needed to be there from the first run.
