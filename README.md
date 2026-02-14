# NoticiasCangrejo

NoticiasCangrejo is an OpenClaw skill that fetches news from GNews (`gnews.io`) for any topic and outputs a Markdown summary of the top articles.

## Features

- Works with any topic provided by the user
- Uses GNews Search API
- Pulls up to 20 articles and returns the 15 most relevant
- Outputs clean Markdown with date, greeting, titles, and URLs
- Includes dashboard API key metadata for ClawHub/OpenClaw publishing

## Installation

1. Enter the skill folder:

```bash
cd noticias-cangrejo
```

2. Install dependencies:

```bash
pip install -r requirements.txt
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
python3 scripts/fetch_news.py "space exploration"
```

Custom language and result size:

```bash
python3 scripts/fetch_news.py "renewable energy" --lang en --max-articles 20
```

Save summary to a file:

```bash
python3 scripts/fetch_news.py "cybersecurity" --output ./cybersecurity-news.md
```

## OpenClaw Usage

When this skill is installed, provide a topic request such as:

- "Get me a NoticiasCangrejo summary for inflation in Europe"
- "Summarize latest news about Formula 1"

The skill reads `GNEWS_API_KEY` from environment/dashboard configuration and returns Markdown output.

## Publishing Notes (ClawHub)

- Skill folder name is slug-friendly: `noticias-cangrejo`
- `SKILL.md` includes dashboard metadata for API key requirement
- Dependencies are minimal and pinned to required runtime library only
- No hardcoded API credentials are included
