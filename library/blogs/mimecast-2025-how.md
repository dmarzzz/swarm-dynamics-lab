---
id: mimecast-2025-how
type: blog
title: 'Mimecast Threat Intelligence: How ChatGPT Upended Email'
authors:
- Andrew Williams
year: 2025
url: https://www.mimecast.com/blog/how-chatgpt-upended-email/
site: Mimecast
topics:
- swarm-detection
read_depth: full
relevance: 4
added_by: shadow/sol-g49
accessed: '2026-10-03'
---

## Summary

Mimecast trains an email-authorship classifier and applies it to monthly customer-email samples. The estimate mixes benign and malicious text and measures likely AI writing rather than phishing intent, coordinated operators or direct evidence of autonomous agents controlling accounts.

## Key claims

- Updated 2025-04-17, originally 2024-09-30. Samples 2,000 emails/month January 2022 to March 2025; up to 10% classified AI-written in a month. No global 12% claim is supported by this source.
- Method: deep-learning engine trained on over 20,000 customer/synthetic emails, using GPT-4o, Claude 3.5 Sonnet, Command R+, Jamba Instruct and Llama3. Test sets include 10,000 human emails, 7,000 synthetic emails and two Kaggle corpora; reports 200,000 repeated classifications.
- Engine estimates AI use, not maliciousness. No calibrated prevalence confidence intervals, public model or labelled customer-email release provided here.

## Evidence quality

Primary vendor classifier study; synthetic-generator coverage and presumed-human historical emails constrain inference. Words such as 'delve' or greetings are not sufficient independent labels.

## Relevance to us

Dated short-text/communication prevalence source with sampling counts. Provides a caution against equating AI authorship with malicious swarm membership.
