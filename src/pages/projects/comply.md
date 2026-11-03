---
layout: ../../layouts/Project.astro
title: comply., a system of record for DOT drug and alcohol testing
kind: Product
org: My startup
date: '2026-11'
period: 2026 – now
summary: Employers that run DOT random testing often keep the pool in spreadsheets and send it to an outside administrator they can't see into. comply. keeps that program in one place, from the HR system to the inspector.
impact: Live for FAA (14 CFR Part 120); the other DOT agencies are next
img: img/comply.jpg
tags: [product, react, typescript, compliance, motion design]
links:
  - { t: complydot.org, href: 'https://www.complydot.org' }
  - { t: Play the brand intro, href: 'https://sidantap.github.io/portfolio/comply.html' }
---

## What it does

comply. syncs employees from the HR system and routes every pool change through an approval queue with the HR reason attached. It runs random selections that anyone can re-run to prove they were fair, then tracks each test from the notice and the nearest open collection site to the MRO result. The audit report and draft MIS numbers are always ready for an inspection. The program manager makes every decision; the software keeps the record.

## Built on the rules

Selections use a seeded xoshiro128** generator with an unbiased Fisher–Yates shuffle, so every draw can be re-checked. Rate math follows FAA AC 120-126A. Person-level alerts flag the problems the FAA fined employers for in 2026: all six of the 2026 FAA enforcement cases map to an alert the demo raises. The selection, rate and compliance logic is covered by 28 unit tests.

<figure><img src="../../img/comply.jpg" alt="The comply. homepage" /><figcaption>complydot.org</figcaption></figure>

## Brand and intro

The landing page opens with an intro and a mascot. The word "comply" crashes into its period and jiggles, a firefly circles it, lights the dot with its tail, lands in front of the name, and the whole logo docks into the nav. The same firefly guides visitors through the product demo, flying to the next button and saying what to press.

The flight is simulated rather than keyframed: steering with arrival braking, a slow wander, body pitch from velocity, wings that beat in flight and fold on landing, and a tail light that brightens when you scroll or come close. It holds still for visitors who turn motion off.

## Stack

React 19, TypeScript, Vite, Vitest and three.js, deployed on Vercel. The demo runs on a fictional airline with made-up people.
