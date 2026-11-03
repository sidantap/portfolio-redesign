---
layout: ../../layouts/Project.astro
title: Vidvo, the Canva for short-form video
kind: Venture & commercialization
org: KCV Innovation Fellowship · Team #2
date: '2025-10'
period: Fall 2025
summary: In the Kentucky Commercialization Ventures fellowship, our team took Vidvo, an AI tool that turns a small business's text, photos and product data into short branded videos, from a one-slide idea to a commercialization plan.
impact: One of ten fellows in the Fall 2025 cohort; four research deliverables from concept to go-to-market plan
img: fig/vidvo-pdiagram.svg
tags: [commercialization, customer discovery, lean canvas, swot, market sizing, freemium pricing, p-diagram, failure mode analysis, technology readiness levels, go-to-market, generative ai, saas]
links:
  - { t: KCV announcement, href: 'https://www.kycommercializationventures.com/post/ten-graduate-from-fall-2025-innovation-fellowship-cohort' }
---

Kentucky Commercialization Ventures trains the people who take Kentucky's research and inventions to market. In the Fall 2025 fellowship I was on **Team #2**, with Stephanie Carter, Nicolette Josue and Taylor Shearer. Our task across the fellowship was to take one idea all the way from concept to a plan someone could fund. Ours was **Vidvo**.

## The idea

We started by studying a founder: Melanie Perkins, who built Canva on one premise, *design for everyone*. She saw how hard professional design tools were and made one anybody could use.

We asked where that same gap still exists. Our answer was short-form video. Small businesses know they need Reels, TikToks and Shorts, but the choice is between professional editors that take skill and time (Adobe Premiere) and mobile apps that are quick but limited (CapCut). Most owners don't have the time, the budget or a marketing person.

> Vidvo is an AI-powered short-form video tool that turns simple inputs, text, product photos or existing brand assets, into fully branded short videos, with Canva-level simplicity.

The goal: just as Canva made design accessible, make motion storytelling accessible.

## Is there a market?

We wrote the business on a **lean canvas** and stress-tested it with a **SWOT**.

| | |
|---|---|
| **Problem** | Small businesses face high cost and skill barriers to professional marketing video |
| **Customers** | Small business owners, startups, social media managers, freelancers |
| **Value proposition** | "Create high-quality videos in minutes, no experience required" |
| **Unfair advantage** | Deep simplicity, low price, an automated AI workflow |
| **Channels** | Social ads, partnerships with small business centers, marketing forums |
| **Revenue** | Freemium, then a **$10/month** premium tier; later, tiered SaaS and add-on render credits |
| **Costs** | AI infrastructure, cloud hosting, UX design, marketing |
| **Key metrics** | Monthly user growth, videos exported, engagement |

The video marketing industry is valued at over $30 billion, and small businesses make up about 80% of digital ad creators. Our target was to cut content production cost by about 70% and make production at least five times faster than a traditional editing workflow.

The SWOT was honest about the risks: no brand recognition yet, dependence on reliable cloud and AI infrastructure, fewer advanced features at launch, and well-funded competitors (Canva, CapCut, Adobe Express) in a market that's saturating fast.

## Talking to customers

Before building anything, we interviewed potential users. Two early conversations shaped the plan:

- **A fitness studio** that posts on Instagram and Facebook rated its current tool 3 out of 5, and rated interest in a short-form video tool 4 out of 5. Willingness to pay came down to one thing: quality.
- **A Kentucky education initiative** that posts on LinkedIn, Facebook and X rated Canva 1 out of 5, and also rated interest 4 out of 5, with willingness to pay held back by a tight marketing budget.

Both said the same thing: the pain is the *time and skill* video takes. That told us the product had to be business-first, fast and cheap, not a feature-rich editor. The plan called for at least three more interviews before locking the MVP.

## Designing the system

For the technology research, we described Vidvo as a system and asked what could go wrong with it.

<figure><img src="../../fig/vidvo-pdiagram.svg" alt="P-diagram: user prompts, templates and uploads go into Vidvo, which outputs a video file, preview frames and error logs; resolution, export parameters and GPU limits are controlled; internet instability, API throttling, unclear prompts and high traffic are noise" /><figcaption>Fig. 1 · The P-diagram: inputs, controls, noise and outputs</figcaption></figure>

The architecture is four layers: an **input layer** (prompts, images, templates), a **processing layer** (prompt analysis and model inference), a **rendering engine** (GPU compute, frame assembly, autosave) and an **export layer** (codecs, aspect ratios, presets). Around it sit logging, autosave, and integrations with media libraries, templates and music licensing.

The **P-diagram** separates what we control (resolution, export settings, GPU limits) from what we can't (shaky connections, API throttling, vague prompts, traffic spikes). The design has to deliver a good video despite the noise, not only when everything goes right.

## What could go wrong

<figure><img src="../../fig/vidvo-fishbone.svg" alt="Ishikawa diagram with technology, measurement, environment and method causes of a failed or off-brand export, and a TRL scale from 1 to 9 with 3 to 4 highlighted as the current stage" /><figcaption>Fig. 2 · Failure modes by category, and where the technology stands</figcaption></figure>

We grouped the failure modes the way a manufacturing team would:

- **Technology:** the GPU render pipeline overloads, a codec or export fails, autosave doesn't fire.
- **Measurement:** no quality check before export; prompts too vague to act on.
- **Environment:** network throttling and heavy user load.
- **Method:** branding placed wrong, no aspect-ratio presets, missing copyright filtering.

That put Vidvo at **TRL 3–4**: an early prototype with its failure modes identified. The next milestone is TRL 4, a basic prototype with at least one key failure mode validated, then TRL 5–7 by building and testing countermeasures for the rest.

## Going to market

| | |
|---|---|
| **Positioning** | "The simplest AI video tool for non-experts" |
| **Launch** | Month 1 teaser campaign → month 2 closed beta → month 3 full launch with feedback loops |
| **Targets** | 10,000 sign-ups in 3 months, 20% paid conversion, 4.5/5 satisfaction |
| **Budget** | $500k: 40% digital marketing, 30% development, 30% sales and support |
| **Marketing** | LinkedIn and Instagram ads, tutorial content, creator partnerships |
| **IP** | The style engine, brand-consistency logic and UI workflow; copyright, trade dress and trademark |
| **Partners** | Cloud GPU providers, stock media licensors, small business marketing platforms |
| **Risks** | Model errors, rendering failures, copyright and privacy |

## What I took from it

Most of commercialization happens before the product: who exactly it's for, what they'd pay, what breaks, and how ready it really is. Writing a P-diagram and a fishbone for software felt odd at first; it turned out to be the clearest way to see what a v1 had to get right.
