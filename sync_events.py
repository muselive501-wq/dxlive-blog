import os
import json
import re
import urllib.request
import datetime
from xml.etree import ElementTree as ET

# Configuration
RSS_FEED_URL = "https://www.dxlive.com/blog/feed/"
OUTPUT_DIR = "."
NEWS_JSON = "news.json"
UPDATE_NEWS_SCRIPT = "update_news.py"

# Simple HTML Template for new articles
ARTICLE_TEMPLATE = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | DXLIVE FAN BLOG</title>
    <meta name="description" content="{description}">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header class="navbar">
        <div class="header-container">
            <a href="index.html" class="logo">DXLIVE<span>FAN BLOG</span></a>
            <button class="hamburger" id="hamburger-btn" aria-label="メニュー"><span></span><span></span><span></span></button>
            <nav class="nav-links">
                <a href="index.html">Home</a>
                <a href="registration-guide.html">登録方法</a>
                <a href="category.html?type=usage">使い方</a>
                <a href="category.html?type=events">イベント情報</a>
                <a href="category.html?type=creators">キャスト向け記事</a>
                <div class="search-container">
                    <form action="search.html" method="get">
                        <input type="text" name="q" placeholder="記事を検索..." class="search-input" required>
                        <button type="submit" class="search-btn">🔍</button>
                    </form>
                </div>
            </nav>
        </div>
    </header>
    <div class="mobile-overlay" id="mobile-overlay"></div>

    <main class="main-content">
        <article class="section-container article-body">
            <div class="article-header">
                <div class="article-category">イベント情報</div>
                <h1 class="article-title">{title}</h1>
                <div class="article-meta">
                    <span class="article-date">{date}</span>
                </div>
            </div>
            
            <img src="{image}" alt="アイキャッチ画像" class="article-image">

            <div class="article-content">
                {content}
            </div>

            <div style="text-align: center; margin-top: 3rem;">
                <a href="https://www.dxlive.com/" class="btn-primary">DXLIVE公式サイトで詳細を見る</a>
            </div>
        </article>
    </main>

    <footer>
        <div class="footer-content">
            <a href="index.html" class="footer-logo">DXLIVE<span>FAN BLOG</span></a>
            <p>© 2026 DXLIVE FAN BLOG. All Rights Reserved.</p>
        </div>
    </footer>
    <script src="seo_features.js"></script>
    <script>
        (function(){{
            var h=document.getElementById("hamburger-btn"),n=document.querySelector(".nav-links"),o=document.getElementById("mobile-overlay");
            if(!h||!n||!o)return;
            function t(){{h.classList.toggle("active");n.classList.toggle("open");o.classList.toggle("active")}}
            h.addEventListener("click",t);
            o.addEventListener("click",t);
        }})();
    </script>
</body>
</html>
"""

def clean_html(raw_html):
    """Remove scripts, styles and some tags to get clean content."""
    clean = re.sub(r'<script.*?>.*?</script>', '', raw_html, flags=re.DOTALL)
    clean = re.sub(r'<style.*?>.*?</style>', '', clean, flags=re.DOTALL)
    clean = re.sub(r'<[^>]+>', ' ', clean)
    return clean.strip()

def rewrite_content(title, original_content):
    """
    Simulate rewriting: Split content into paragraphs, add tone. 
    In a real scenario, this would use an LLM API.
    """
    paragraphs = original_content.split('\n')
    rewritten_html = f"<p>DXLIVE公式サイトにて、最新ニュース「{title}」が公開されました！</p>"
    rewritten_html += f"<h2>イベント内容のポイント</h2>"
    
    count = 0
    for p in paragraphs:
        p = p.strip()
        if len(p) > 20 and count < 5:
            rewritten_html += f"<p>{p}</p>"
            count += 1
            
    rewritten_html += "<h2>ファンの反応と楽しみ方</h2>"
    rewritten_html += "<p>今回のアップデート・イベントは非常に期待が高まっています。公式サイトへログインして、今すぐ詳細をチェックしましょう！</p>"
    
    return rewritten_html

def sync_events():
    try:
        # Add a User-Agent header to avoid 403 Forbidden error
        req = urllib.request.Request(
            RSS_FEED_URL, 
            data=None, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
        )
        response = urllib.request.urlopen(req)
        xml_data = response.read()
        root = ET.fromstring(xml_data)
        
        # namespaces
        ns = {'content': 'http://purl.org/rss/1.0/modules/content/'}
        
        items = root.findall('.//item')
        new_articles = []
        
        for item in items[:3]: # Sync only top 3 for now
            title = item.find('title').text
            link = item.find('link').text
            pub_date = item.find('pubDate').text
            full_content = item.find('content:encoded', ns).text if item.find('content:encoded', ns) is not None else item.find('description').text
            
            # Create a URL-friendly filename
            safe_title = re.sub(r'[^\w\s-]', '', title).strip().lower()
            safe_title = re.sub(r'[-\s]+', '-', safe_title)
            filename = f"event-{safe_title[:30]}.html"
            
            # Format Date
            dt = datetime.datetime.strptime(pub_date, '%a, %d %b %Y %H:%M:%S %z')
            display_date = dt.strftime('%Y.%m.%d')
            json_date = dt.strftime('%Y-%m-%d')

            # Use a deterministic filename based on the safe title
            image_filename = f"eyecatch-{safe_title[:30]}.png"
            image_path = f"assets/images/events/{image_filename}"
            
            # If the specific image doesn't exist, use the generic one for now
            if not os.path.exists(image_path):
                # Fallback to a central event eyecatch if available
                image_path = "assets/images/eyecatch_event.png"
            
            # Rewrite content
            excerpt = clean_html(full_content)[:100] + "..."
            rewritten_html = rewrite_content(title, clean_html(full_content))
            
            # Generate HTML
            html_content = ARTICLE_TEMPLATE.format(
                title=title,
                description=excerpt,
                date=display_date,
                image=image_path,
                content=rewritten_html
            )
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            # Prepare for JSON
            article_data = {
                "id": int(dt.timestamp()),
                "categoryId": "events",
                "title": title,
                "date": display_date,
                "category": "イベント情報",
                "excerpt": excerpt,
                "url": filename,
                "image": image_path
            }
            new_articles.append(article_data)
            print(f"Generated {filename}")

        return new_articles

    except Exception as e:
        print(f"Error during sync: {e}")
        return []

def update_news_json(new_articles):
    if not new_articles:
        return
    
    with open(NEWS_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    # Filter out existing by URL to avoid duplicates
    existing_urls = {a['url'] for a in data}
    unique_new = [a for a in new_articles if a['url'] not in existing_urls]
    
    if unique_new:
        updated_data = unique_new + data
        with open(NEWS_JSON, 'w', encoding='utf-8') as f:
            json.dump(updated_data, f, ensure_ascii=False, indent=2)
        print(f"Added {len(unique_new)} new events to {NEWS_JSON}")

if __name__ == "__main__":
    new_events = sync_events()
    update_news_json(new_events)
