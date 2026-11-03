---
layout: ../../layouts/Post.astro
title: Teaching GPT-2 about one university
kind: Research
date: '2024-08-15'
minutes: 5
draft: true
summary: We built 1,611 training samples from the NKU website and fine-tuned GPT-2 on them, so it could answer questions about Northern Kentucky University better than a general-purpose chatbot.
tags: [llm, fine-tuning, nlp, research]
---

This was a research poster at the NKU School of Computing & Analytics, with Simran Shrestha, Pheo Ward and Dr. Junxiu Zhou.

## The question

General chatbots know a little about everything and not much about one place. Ask about a specific university's programs, offices or mission and you get something vague or wrong. Could a much smaller model, trained on that one university's own pages, answer those questions better?

## Building the data

The model can only be as good as its examples, so most of the work was the data.

1. A Python program collected the HTML of the NKU website and saved it as text with the help of Jina AI's reader.
2. We cleaned that text into **1,611 samples**.
3. Each sample was converted into instruction, input and output form with GPT-4o, and we reviewed them by hand.

## Training

We fine-tuned GPT-2, a 1.5-billion-parameter transformer, on that dataset. The data pipeline ran on AWS EC2 and S3, and training took more than six hours.

## What we found

On ten NKU-specific test questions, the fine-tuned model did **10–15% better than ChatGPT**. Asked "What is the mission of NKU?", it answered:

> As a public comprehensive university located in a major metropolitan area, NKU delivers innovative, student-centered education and engages in impactful, scholarly, and creative endeavors.

## Where it falls short

Ten questions is a small test, and a better answer to them is not the same as a reliable assistant. The poster's next steps were more training data, and a user interface so the NKU community could actually use the chatbot.

## What I took from it

A small model with the right data can beat a big one on a narrow job. Getting the data right was most of the work, the same as in every data pipeline I've built since.
