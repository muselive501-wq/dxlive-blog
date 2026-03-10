import os
import re
import json

SEARCH_BAR_HTML = """
                <div class="search-container">
                    <form action="search.html" method="get">
                        <input type="text" name="q" placeholder="記事を検索..." class="search-input" required>
                        <button type="submit" class="search-btn">🔍</button>
                    </form>
                </div>"""

TOC_HTML = """
            <div class="toc-container">
                <h2>目次</h2>
                <ul id="toc-list" class="toc-list"></ul>
            </div>"""

RELATED_HTML = """
            <div class="related-articles-container">
                <h3>関連記事</h3>
                <div id="related-articles-grid" class="article-grid"></div>
            </div>"""

for filename in os.listdir('.'):
    if not filename.endswith('.html') or filename == 'search.html':
        continue
        
    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    modified = False

    # 1. Add Search Bar if not exists
    if 'search-container' not in content:
        # Some files might have spaces before </nav>
        content = re.sub(r'(\s*)</nav>', r'\1' + SEARCH_BAR_HTML + r'\n\1</nav>', content)
        modified = True

    # 2. Identify if it's an article page (has article-body)
    is_article = False
    if 'class="section-container article-body"' in content:
        is_article = 'new_template'
    elif 'class="article-body"' in content:
        is_article = 'old_template'

    if is_article:
        # TOC (insert after the main eyecatch image)
        if 'toc-container' not in content:
            content = re.sub(r'(<img[^>]*class="article-image"[^>]*>)', r'\1' + '\n' + TOC_HTML, content, count=1)
            modified = True
            
        # Related Articles
        if 'related-articles-container' not in content:
            if is_article == 'new_template':
                content = content.replace("</article>", RELATED_HTML + "\n        </article>")
            else:
                content = content.replace("</section>", RELATED_HTML + "\n        </section>")
            modified = True
            
        # Script
        if 'seo_features.js' not in content:
            content = content.replace("</body>", '    <script src="seo_features.js"></script>\n</body>')
            modified = True
            
        # JSON-LD
        if 'application/ld+json' not in content:
            title_match = re.search(r'<title>(.*?)(\| DXLIVE FAN BLOG)?</title>', content)
            desc_match = re.search(r'<meta name="description" content="(.*?)">', content)
            img_match = re.search(r'<img src="(.*?)" alt="アイキャッチ画像"', content)
            
            # Find date "YYYY.MM.DD"
            date_match = re.search(r'>(\d{4}\.\d{2}\.\d{2})<', content)
            
            if title_match and desc_match and img_match:
                title = title_match.group(1).replace(" | DXLIVE FAN BLOG", "")
                desc = desc_match.group(1)
                img = "https://example.com/" + img_match.group(1)
                date = date_match.group(1).replace('.', '-') if date_match else "2026-03-10"
                
                json_ld = {
                    "@context": "https://schema.org",
                    "@type": "Article",
                    "headline": title.strip(),
                    "image": [img],
                    "datePublished": date + "T08:00:00+08:00",
                    "dateModified": date + "T08:00:00+08:00",
                    "author": [{
                        "@type": "Person",
                        "name": "DXLIVE FAN BLOG"
                    }],
                    "description": desc.strip()
                }
                
                script_tag = f'\n    <script type="application/ld+json">\n    {json.dumps(json_ld, ensure_ascii=False, indent=4)}\n    </script>\n</head>'
                content = content.replace("</head>", script_tag)
                modified = True

    if modified:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filename}")
        
print("SEO features injected.")
