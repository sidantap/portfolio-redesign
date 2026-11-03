---
layout: ../../layouts/Project.astro
title: Reading how first-year nurses feel
kind: NLP research
org: NKU · with Dr. Zhou
date: '2025-11'
period: Jul – Dec 2025
summary: A Python pipeline that scrapes forum posts from first-year nurses, cleans them, and classifies stress, depression, workplace and wellbeing themes, with an R Shiny dashboard of how they change over time.
impact: Four themes classified; a conference paper is planned
img: fig/nurse-walk.svg
tags: [natural language processing, text classification, text preprocessing, lemmatization, stop-word removal, web scraping, unstructured data, sentiment analysis, time series, nltk, scikit-learn, pandas, r shiny]
links: []
---

New nurses talk openly in online forums, more openly than in any survey. Read at scale, those posts could show what weighs on them and when. This research pipeline reads them for us.

<figure><img src="../../fig/nurse-walk.svg" alt="A made-up forum post shown at each step: the raw text, cleaned text, lemmatized tokens colored by theme, and theme scores for stress, depression, workplace and wellbeing" /><figcaption>Fig. 1 · Follow one post through the pipeline (made-up example)</figcaption></figure>

## Following one post

**Collect.** A Python scraper gathers posts written by first-year nurses.

**Clean.** Forum text is messy: quotes of other posts, abbreviations, typos, signatures. It's lowercased, and punctuation and stop words like "the" and "is" are removed, leaving the words that carry meaning.

**Lemmatize.** NLTK reduces each word to its base form: "exhausted" becomes *exhaust*, "cried" becomes *cry*. Without this, the model would treat every form of a word as a different signal.

**Classify.** A scikit-learn classifier sorts posts into four themes, **stress, depression, workplace and wellbeing**.

**Explore.** An R Shiny dashboard counts posts by theme over time so changes across the first year become visible.

## Why it matters to me

Getting meaning out of messy, unstructured language is the part of AI I find most interesting. Here it matters: patterns like these could show when new nurses most need support. The work supports a planned conference paper.
