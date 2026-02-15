# NoticiasCangrejo

NoticiasCangrejo is an OpenClaw skill that fetches news from GNews (`gnews.io`) for any topic and outputs a Markdown summary of the top articles.

## Features

- Works with any topic provided by the user
- Uses GNews Search API
- Pulls up to 20 articles and returns the 15 most relevant
- Outputs clean Markdown with date, greeting, titles, and URLs
- Includes dashboard API key metadata for ClawHub/OpenClaw publishing
- No third-party Python packages required

## Installation

1. Enter the skill folder:

```bash
cd noticias-cangrejo
```

2. Ensure scripts are executable:

```bash
chmod +x noticias-cangrejo scripts/fetch_news.py
```

## Environment Variable Setup

Set your GNews API key:

```bash
export GNEWS_API_KEY="your_api_key_here"
```

Do not commit real API keys to source control.

## CLI Usage

Basic:

```bash
./noticias-cangrejo "space exploration"
```

Custom language and result size:

```bash
./noticias-cangrejo "renewable energy" --lang en --max-articles 20
```

Save summary to a file:

```bash
./noticias-cangrejo "cybersecurity" --output ./cybersecurity-news.md
```

## OpenClaw Usage

When this skill is installed, ask for a topic summary, for example:

- "Usa noticias-cangrejo para Terpel Colombia"
- "Resume las noticias sobre Formula 1"

The skill reads `GNEWS_API_KEY` from dashboard/environment configuration and returns Markdown output.

## Publishing Notes (ClawHub)

- Skill folder name is slug-friendly: `noticias-cangrejo`
- `SKILL.md` includes dashboard metadata for API key requirement
- No hardcoded API credentials are included
- Runtime is dependency-free (standard library only)
