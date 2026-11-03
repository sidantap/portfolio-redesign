---
layout: ../../layouts/Project.astro
title: Reading how first-year nurses feel
kind: NLP research
org: NKU · with Dr. Zhou
date: '2025-11'
period: Jul – Dec 2025
summary: A Python pipeline that scrapes forum posts from first-year nurses, cleans them, and classifies stress, depression, workplace and wellbeing themes, with an R Shiny dashboard of how sentiment changes over time.
impact: Four themes classified; a conference paper is planned
img: fig/nurse-pipeline.svg
tags: [natural language processing, text classification, lemmatization, web scraping, sentiment over time, nltk, scikit-learn, pandas, r shiny]
links: []
---

## The question

First-year nurses talk openly about their jobs in online forums, in a way they rarely do in surveys. Read at scale, those posts could show what weighs on new nurses and when. The question: can a pipeline sort those posts into the themes that matter, stress, depression, the workplace and wellbeing, and show how they change over time?

<figure><img src="../../fig/nurse-pipeline.svg" alt="Pipeline: scrape forum posts, clean and lemmatize the text, classify into stress, depression, workplace and wellbeing themes, and explore them over time in an R Shiny dashboard" /><figcaption>Fig. 1 · Posts in, themes over time out</figcaption></figure>

## The pipeline

1. **Collect.** A Python scraper gathers forum posts written by first-year nurses.
2. **Clean.** Forum text is messy: quotes of other posts, abbreviations, typos and signatures. The text is normalized, then **lemmatized** with NLTK so "stressed", "stressing" and "stress" count as the same idea.
3. **Classify.** A scikit-learn classifier assigns each post to the four themes.
4. **Explore.** An R Shiny dashboard shows how the themes and sentiment shift over time.

## Why it interests me

Getting meaning out of messy, unstructured language is the part of AI I find most interesting. Here it matters: patterns like these could show when new nurses most need support. The work supports a planned conference paper.
