import urllib.request
import re
import datetime
import json
import os

# Import functions from sync_events
from sync_events import ARTICLE_TEMPLATE, clean_html, rewrite_content, update_news_json

URLS = [
    "https://www.dxlive.com/blog/category/event/" 
]

def get_event_links():
    req = urllib.request.Request(URLS[0], headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req).read().decode('utf-8')
    links = re.findall(r'<a href="(https://www.dxlive.com/blog/[^"]+)"[^>]*>', html)
    unique_links = list(set([l for l in links if 'category' not in l and 'page' not in l and 'author' not in l]))
    return unique_links

def fetch_and_import():
    links = get_event_links()
    new_articles = []
    
    with open('news.json', 'r', encoding='utf-8') as f:
        existing_data = json.load(f)
    existing_urls = {a['original_url'] for a in existing_data if 'original_url' in a}
    # For now, just rely on filename match
    existing_filenames = {a['url'] for a in existing_data}
    
    for link in links:
        print(f"Fetching {link}")
        req = urllib.request.Request(link, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            html = urllib.request.urlopen(req).read().decode('utf-8')
        except Exception as e:
            print(f"Failed to fetch {link}: {e}")
            continue
            
        # Extract title
        title_match = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.IGNORECASE | re.DOTALL)
        if not title_match:
            title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
        title = title_match.group(1).replace(' | DXLIVE', '').strip() if title_match else "Event"
        title = re.sub(r'<[^>]+>', '', title)
        
        # Extract date
        date_match = re.search(r'<time[^>]*datetime="(.*?)"', html, re.IGNORECASE)
        if date_match:
            date_str = date_match.group(1)[:10]
        else:
            # try to find a date string
            date_match = re.search(r'(\d{4}\.\d{2}\.\d{2})', html)
            date_str = date_match.group(1).replace('.', '-') if date_match else "2026-01-01"
            
        dt = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        display_date = dt.strftime('%Y.%m.%d')
        
        # Extract content
        content_match = re.search(r'<div class="entry-content[^>]*>(.*?)</div>', html, re.IGNORECASE | re.DOTALL)
        if content_match:
            full_content = content_match.group(1)
        else:
            full_content = "イベントの詳細が発表されました。"
            
        safe_title = re.sub(r'[^\w\s-]', '', title).strip().lower()
        safe_title = re.sub(r'[-\s]+', '-', safe_title)
        filename = f"event-{safe_title[:30]}.html"
        
        if filename in existing_filenames:
            print(f"Skipping {filename}, already exists.")
            continue
            
        image_filename = f"eyecatch-{safe_title[:30]}.png"
        image_path = f"assets/images/events/{image_filename}"
        
        if not os.path.exists(image_path):
            image_path = "assets/images/eyecatch_event.png"
            
        excerpt = clean_html(full_content)[:100] + "..."
        rewritten_html = rewrite_content(title, clean_html(full_content))
        
        html_content = ARTICLE_TEMPLATE.format(
            title=title,
            description=excerpt,
            date=display_date,
            image=image_path,
            content=rewritten_html
        )
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        article_data = {
            "id": int(dt.timestamp()) + len(new_articles), # ensure unique id
            "categoryId": "events",
            "title": title,
            "date": display_date,
            "category": "イベント情報",
            "excerpt": excerpt,
            "url": filename,
            "image": image_path,
            "original_url": link
        }
        new_articles.append(article_data)
        print(f"Imported {title}")
        
    return new_articles

if __name__ == "__main__":
    new_events = fetch_and_import()
    if new_events:
        update_news_json(new_events)
        print("Done importing past events.")
    else:
        print("No new events to import.")
