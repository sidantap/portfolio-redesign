---
layout: ../../layouts/Project.astro
title: An NKU chatbot on a fine-tuned GPT-2
kind: Machine learning research
org: NKU · research poster
date: '2024-08'
period: Feb – Aug 2024
summary: We built 1,611 training samples from the NKU website and fine-tuned GPT-2 on them, so it could answer questions about Northern Kentucky University better than a general-purpose chatbot.
impact: 10–15% better than ChatGPT on NKU-specific test questions
img: fig/chatbot-sample.svg
tags: [large language models, fine-tuning, instruction tuning, domain adaptation, dataset curation, data labeling, web scraping, transformers, gpt-2, gpt-4o, jina ai, aws ec2, aws s3, python]
links: []
---

A research poster at the NKU School of Computing & Analytics, with Simran Shrestha, Pheo Ward and Dr. Junxiu Zhou.

## Question

General chatbots know a little about everything and not much about one place. Ask about a university's programs, offices or mission and you get something vague. Could a much smaller model, trained on that university's own pages, answer those questions better?

## Method

Most of the work was the data. A model can only be as good as its examples.

1. **Collect.** A Python program gathered the HTML of the NKU website.
2. **Extract.** Jina AI's reader turned each page into clean text.
3. **Curate.** We cleaned that text into **1,611 samples**.
4. **Format.** Each sample became an instruction, input and output, drafted with GPT-4o and reviewed by hand.
5. **Train.** We fine-tuned GPT-2, a 1.5-billion-parameter transformer, on the dataset. The data pipeline ran on AWS EC2 and S3.

<figure><img src="../../fig/chatbot-sample.svg" alt="One training sample shown as JSON with instruction, input and output fields, annotated with what each field is for" /><figcaption>Fig. 1 · One training sample, field by field</figcaption></figure>

Instruction format matters: it teaches the model the *shape* of a good answer, a question in and a direct answer out, not just facts to memorize.

## Results

On ten NKU-specific test questions, the fine-tuned model did **10–15% better than ChatGPT**. The answer in Fig. 1 is its response to "What is the mission of NKU?"

## Limitations

Ten questions is a small test, and a better answer to them isn't the same as a reliable assistant. The poster's next steps were more training data, and a user interface so the NKU community could actually use it.

## Takeaway

A small model with the right data can beat a large one on a narrow job, and getting the data right is most of the work.
