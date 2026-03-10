import json
import re
import os

with open("news.json", "r", encoding="utf-8") as f:
    text = f.read()
    # Strip BOM if present
    if text.startswith('\ufeff'):
        text = text[1:]
    news = json.loads(text)

for item in news:
    url = item["url"]
    image_path = item["image"]
    if os.path.exists(url):
        with open(url, "r", encoding="utf-8") as f:
            content = f.read()

        # Check if we already inserted the eyecatch image to avoid duplication
        if 'alt="アイキャッチ画像"' in content:
            print(f"Already updated {url}")
            continue
        
        # Replace </h1> with </h1> + img tag
        img_tag = f'\n            <img src="{image_path}" alt="アイキャッチ画像" class="article-image" style="margin-top: 1.5rem; margin-bottom: 2rem;">'
        new_content = re.sub(r'(</h1>)', r'\1' + img_tag, content, count=1)
        
        if new_content != content:
            with open(url, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Updated {url}")
        else:
            print(f"H1 tag not found in {url}")
