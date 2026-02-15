---
name: noticias-cangrejo
description: Fetch and summarize recent news articles from GNews for any user-provided topic, then produce a Markdown digest with date, greeting, and top links. Use when a user asks for current news briefings, topic-based updates, multilingual headline digests, or wants repeatable GNews-powered summaries that can be published through OpenClaw/ClawHub.
category: data
tags: news, api, gnews, digest
metadata:
  clawdbot:
    emoji: "🦀"
    requires:
      api_key:
        name: GNEWS_API_KEY
        label: "GNews API Key"
        description: "Enter your GNews API key from gnews.io"
---

# NoticiasCangrejo

Generate a Markdown news digest for any topic using the GNews API.

## When To Use

Use this skill when the user asks for recent news on any topic, such as politics, science, startups, health, finance, sports, or local events, and wants a concise, linkable summary.

## Environment Requirement

Set this environment variable before execution:

- `GNEWS_API_KEY`

## Workflow

1. Receive a topic from the user.
2. Validate that `GNEWS_API_KEY` exists.
3. Query GNews Search API for up to 20 articles using topic + language.
4. Compute relevance based on topic-word overlap against article title and description.
5. Keep the top 15 ranked articles.
6. Print Markdown output with:
   - Date (`YYYY/MM/DD`)
   - Greeting line in Spanish
   - Topic line
   - Numbered list of article title + URL
7. Optionally save output to a file with `--output`.

## Execution

No `pip install` is required.

Use the bundled entrypoint:

```bash
./noticias-cangrejo "quantum computing"
```

Optional parameters:

- `--lang` (default: `en`)
- `--max-articles` (default: `20`)
- `--output` to write Markdown to a file

## Example Usage

```bash
export GNEWS_API_KEY="your_api_key_here"
./noticias-cangrejo "global markets" --lang en --max-articles 20 --output ./markets.md
```
