---
layout: ../../layouts/Project.astro
title: A data pipeline that runs every night for $0
kind: Data engineering
org: Personal · open source
date: '2026-10'
period: Oct 2026 – now
summary: Cincinnati 311 requests, NOAA weather and NHTSA vehicle complaints, loaded incrementally into a DuckDB warehouse, tested and modeled with dbt, and scored by a text classifier, every night on GitHub Actions at no cost.
impact: 84.7% on a held-out test set, about 80% live on complaints it has never seen, and runs finish in under a minute
img: img/nightly-overview.jpg
tags: [incremental ingestion, watermarking, late-arriving data, medallion architecture, dbt, dbt tests, data quarantine, star schema, data lineage, sentence embeddings, logistic regression, model monitoring, duckdb, github actions, python]
links:
  - { t: Live dashboard, href: 'https://sidantap.github.io/nightly-311-pipeline/' }
  - { t: Code and README, href: 'https://github.com/sidantap/nightly-311-pipeline' }
---

At work my pipelines run on systems I can't show anyone. So I built one I can: a small pipeline that does the same jobs on public data, runs unattended every night, and publishes what it did. Below are the five decisions that shape it.

## 1 · Load only what changed

Three public sources, each messy in its own way: **Cincinnati 311 service requests** (they change after they're created: closed, reopened, re-categorized), **NOAA daily weather** at the airport (recent days get revised) and **NHTSA vehicle complaints**.

<figure><img src="../../fig/nightly-windows.svg" alt="Five nights of load windows; each night re-reads a two-day overlap behind the previous watermark, then loads new rows up to the new watermark" /><figcaption>Fig. 1 · Watermark plus overlap, night by night (dates illustrative)</figcaption></figure>

Each source keeps a **watermark**, the newest record already loaded. A run asks only for rows after it, minus an **overlap** to catch late changes: two days for 311, seven for weather, three for complaints. Re-reading a little is far cheaper than missing an edit.

## 2 · Never edit what arrived

Rows land unchanged in **bronze**. Nothing is cleaned on the way in, so any number on the dashboard can be traced back to exactly what the API returned. Everything after that is a dbt model:

<figure><img src="../../fig/nightly-lineage.svg" alt="dbt lineage graph from three raw sources through staging and silver models, a quarantine table, gold dimensions and facts, to the ML predictions and live metrics" /><figcaption>Fig. 2 · Every table the run builds, wired by its real ref() calls</figcaption></figure>

## 3 · Quarantine, don't drop

Rows that break a rule aren't fixed silently and aren't deleted. They go to a **quarantine** table with the reason, and the rest move on.

| Rule | Rows held |
|---|---|
| Closed before it was created | 126 |
| No location | 6 |
| Location outside the city | 5 |

Then **dbt tests** run: unique and non-null keys on every table, accepted values for statuses and categories, relationships from every fact to its dimensions, no negative days-to-close. A failed test fails the run, and the dashboard keeps yesterday's numbers.

## 4 · Model for the questions

The **gold** layer is a star schema: a service-request fact, request-type and date dimensions, and a daily table joining requests to the weather. With that grain, "did rain change anything?" is one query:

<figure><img src="../../fig/nightly-requests.svg" alt="Bar chart of daily 311 requests over 90 days, with rainy days in blue; weekends dip sharply every week" /><figcaption>Fig. 3 · Requests per day, rainy days in blue (real data)</figcaption></figure>

## 5 · Score the model every night

NHTSA complaints come with a component tag, which makes them an answer key. A small open-source embedding model (bge-small) turns each description into a vector, and a logistic regression predicts which of 13 parts of the car it's about. Trained on complaints received before July 1, 2026, it scored **84.7%** on a held-out test set. Every night it classifies the new complaints and is scored against NHTSA's own tags.

<figure><img src="../../fig/nightly-accuracy.svg" alt="Live accuracy holding near 80 percent each night, below the 84.7 percent test-set line" /><figcaption>Fig. 4 · Live accuracy vs. the test set (real data)</figcaption></figure>

The gap between 84.7% and about 80% is why it's scored live: new complaints drift from the training data, and a model that only reports its test score hides that.

<figure><img src="../../fig/nightly-f1.svg" alt="Precision, recall and F1 for 13 vehicle components; steering and seats highest, electrical lowest" /><figcaption>Fig. 5 · Where it's strong and where it's weak</figcaption></figure>

## Running it for free

GitHub Actions runs everything at 07:17 UTC. The warehouse is one DuckDB file, gzipped and kept as a GitHub release asset between runs: download, run, upload. The dashboard is a static page on GitHub Pages that reads one JSON file the run writes. The first three runs failed (an API timeout on the first backfill, then a request with no type breaking a key); each fix is in the run history.
