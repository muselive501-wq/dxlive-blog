#!/usr/bin/env python3
"""
DXLIVE Blog Auto-Update Script
Fetches the latest articles from the DXLIVE blog RSS feed,
categorizes them, and outputs a news.json file for the static site.
"""

import json
import os
import re
import urllib.request

from xml.etree import ElementTree as ET

RSS_FEED_URL = "https://www.dxlive.com/blog/feed/"
OUTPUT_JSON = "news.json"
MAX_ITEMS = 8

# Map Japanese category names from DXLIVE to our categoryId system
CATEGORY_MAP = {
    "キャンペーン": "news",
    "アップデート": "news",
    "お知らせ": "news",
    "ニュース": "news",
    "クリエイター": "creators",
    "特集": "creators",
    "イベント": "events",
    "ノウハウ": "knowhow",
}

# Static articles that should always be preserved in the JSON
STATIC_ARTICLES = [
    {
        "id": 100,
        "categoryId": "knowhow",
        "title": "【公式ガイド】ラブンス（Lovense）を使ってファンと交流しよう！",
        "date": "2026.03.09",
        "category": "ノウハウ",
        "excerpt": "ファンからのチップやアクションに連動して動き、配信を劇的に盛り上げるインタラクティブトイ「Lovense（ラブンス）」の使い方をキャスト向けに徹底解説！",
        "url": "lovense_guide.html",
        "image": "assets/images/news_thumbnail_3_1773045736171.png"
    }
]

# Local placeholder images to cycle through (avoid hotlinking external images)
LOCAL_IMAGES = [
    "assets/images/news_thumbnail_1_1773045710180.png",
    "assets/images/news_thumbnail_2_1773045722676.png",
    "assets/images/news_thumbnail_3_1773045736171.png",
    "assets/images/news_thumbnail_4_1773045768252.png",
]


def fetch_rss_feed(url):
    """Fetches and parses the RSS feed."""
    print(f"Fetching RSS feed from {url}...")
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            xml_data = response.read()
            return ET.fromstring(xml_data)
    except Exception as e:
        print(f"Error fetching RSS: {e}")
        return None


def clean_html(text):
    """Remove HTML tags and clean up text."""
    if not text:
        return ""
    clean = re.sub(r'<[^>]+>', '', text).strip()
    clean = clean.replace('\n', ' ').replace('\r', '')
    clean = re.sub(r'\s+', ' ', clean)
    return clean


def rewrite_excerpt(title, excerpt):
    """
    Rewrite/clean the excerpt for display.
    In production, replace this with an LLM API call (OpenAI/Gemini)
    for genuine content rewriting.
    """
    clean = clean_html(excerpt)
    if len(clean) > 120:
        clean = clean[:117] + "..."
    return clean


def parse_date(pub_date):
    """Convert RSS date format to YYYY.MM.DD."""
    if not pub_date:
        return "N/A"
    months = {
        "Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04",
        "May": "05", "Jun": "06", "Jul": "07", "Aug": "08",
        "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"
    }
    parts = pub_date.split(" ")
    if len(parts) >= 4:
        return f"{parts[3]}.{months.get(parts[2], '01')}.{parts[1].zfill(2)}"
    return pub_date


def get_category_id(category_name):
    """Map a Japanese category name to a categoryId."""
    return CATEGORY_MAP.get(category_name, "news")


def process_feed(root):
    """Processes the parsed XML and generates a list of articles."""
    articles = []
    namespaces = {'content': 'http://purl.org/rss/1.0/modules/content/'}

    channel = root.find("channel")
    if channel is None:
        print("Error: No channel found in RSS feed.")
        return articles

    items = channel.findall("item")
    print(f"Found {len(items)} items in feed. Processing up to {MAX_ITEMS}...")

    for idx, item in enumerate(items[:MAX_ITEMS]):
        title = item.findtext("title", "")
        link = item.findtext("link", "")
        pub_date = item.findtext("pubDate", "")
        category = item.findtext("category", "ニュース")
        raw_excerpt = item.findtext("description", "")

        date_str = parse_date(pub_date)
        category_id = get_category_id(category)
        excerpt = rewrite_excerpt(title, raw_excerpt)

        # Cycle through local images
        image = LOCAL_IMAGES[idx % len(LOCAL_IMAGES)]

        articles.append({
            "id": idx + 1,
            "categoryId": category_id,
            "title": title,
            "date": date_str,
            "category": category,
            "excerpt": excerpt,
            "url": link,
            "image": image
        })

    return articles


def main():
    root = fetch_rss_feed(RSS_FEED_URL)
    if root is None:
        print("Failed to fetch RSS feed. Keeping existing news.json.")
        return

    scraped_articles = process_feed(root)
    if not scraped_articles:
        print("No articles scraped. Keeping existing news.json.")
        return

    # Merge: scraped articles first, then static articles
    all_articles = scraped_articles + STATIC_ARTICLES

    # Save to JSON
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(all_articles, f, ensure_ascii=False, indent=2)

    print(f"✅ Successfully updated {OUTPUT_JSON} with {len(scraped_articles)} scraped + {len(STATIC_ARTICLES)} static articles.")


if __name__ == "__main__":
    main()
