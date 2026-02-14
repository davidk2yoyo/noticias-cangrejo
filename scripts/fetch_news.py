#!/usr/bin/env python3
"""Fetch topic-based news from GNews and print a Markdown summary."""

from __future__ import annotations

import argparse
import datetime as dt
import os
import sys
from typing import Any, Dict, List

import requests

GNEWS_ENDPOINT = "https://gnews.io/api/v4/search"
DEFAULT_LANG = "en"
DEFAULT_MAX_ARTICLES = 20
MAX_SELECTED_ARTICLES = 15


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch news for any topic from GNews and output a Markdown summary."
    )
    parser.add_argument("topic", help="Topic to search for (e.g., 'quantum computing').")
    parser.add_argument("--lang", default=DEFAULT_LANG, help="Language code (default: en).")
    parser.add_argument(
        "--max-articles",
        type=int,
        default=DEFAULT_MAX_ARTICLES,
        help="Maximum number of articles to request from API (default: 20).",
    )
    parser.add_argument(
        "--output",
        help="Optional output file path to save the Markdown summary.",
    )
    return parser.parse_args()


def get_api_key() -> str:
    api_key = os.getenv("GNEWS_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError(
            "Missing GNEWS_API_KEY environment variable. "
            "Set it before running this script."
        )
    return api_key


def fetch_articles(topic: str, lang: str, max_articles: int, api_key: str) -> List[Dict[str, Any]]:
    safe_max = max(1, min(max_articles, DEFAULT_MAX_ARTICLES))
    params = {
        "q": topic,
        "lang": lang,
        "max": safe_max,
        "apikey": api_key,
    }

    try:
        response = requests.get(GNEWS_ENDPOINT, params=params, timeout=20)
    except requests.Timeout as exc:
        raise RuntimeError(
            "Request to GNews timed out. Please try again in a moment."
        ) from exc
    except requests.RequestException as exc:
        raise RuntimeError(f"Network error while contacting GNews: {exc}") from exc

    if response.status_code == 401:
        raise RuntimeError(
            "Unauthorized (401): invalid GNews API key. Verify GNEWS_API_KEY."
        )
    if response.status_code == 429:
        raise RuntimeError(
            "Rate limit reached (429): too many requests to GNews. Try again later."
        )
    if response.status_code != 200:
        detail = response.text.strip()
        raise RuntimeError(
            f"GNews API error (status {response.status_code}). Details: {detail or 'No details returned.'}"
        )

    try:
        payload = response.json()
    except ValueError as exc:
        raise RuntimeError("GNews API returned invalid JSON.") from exc

    articles = payload.get("articles")
    if not isinstance(articles, list):
        raise RuntimeError("Unexpected GNews response format: 'articles' is missing or invalid.")

    return articles


def relevance_score(article: Dict[str, Any], topic_terms: List[str]) -> int:
    title = str(article.get("title") or "").lower()
    description = str(article.get("description") or "").lower()
    text = f"{title} {description}"

    score = 0
    for term in topic_terms:
        if term in text:
            score += 1

    if title:
        for term in topic_terms:
            if term in title:
                score += 1

    return score


def select_top_articles(articles: List[Dict[str, Any]], topic: str) -> List[Dict[str, Any]]:
    topic_terms = [term for term in topic.lower().split() if term]

    ranked = sorted(
        articles,
        key=lambda item: (
            relevance_score(item, topic_terms),
            str(item.get("publishedAt") or ""),
        ),
        reverse=True,
    )

    return ranked[:MAX_SELECTED_ARTICLES]


def render_markdown(topic: str, articles: List[Dict[str, Any]]) -> str:
    today = dt.date.today().strftime("%Y/%m/%d")
    lines = [
        f"# {today}",
        "",
        f'Buenos días, este es el resumen de NoticiasCangrejo para "{topic}" — {today}.',
        "",
    ]

    if not articles:
        lines.append("No se encontraron artículos para este tema.")
        return "\n".join(lines)

    for idx, article in enumerate(articles, start=1):
        title = str(article.get("title") or "Sin título").strip()
        url = str(article.get("url") or "").strip()
        if url:
            lines.append(f"{idx}. [{title}]({url})")
        else:
            lines.append(f"{idx}. {title}")

    return "\n".join(lines)


def main() -> int:
    args = parse_args()

    if not args.topic.strip():
        print("Error: Topic must not be empty.", file=sys.stderr)
        return 1

    try:
        api_key = get_api_key()
        articles = fetch_articles(args.topic.strip(), args.lang, args.max_articles, api_key)
        top_articles = select_top_articles(articles, args.topic.strip())
        markdown = render_markdown(args.topic.strip(), top_articles)
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(markdown)

    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as handle:
                handle.write(markdown + "\n")
        except OSError as exc:
            print(f"Error writing output file: {exc}", file=sys.stderr)
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
