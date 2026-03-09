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
        "id": 111,
        "categoryId": "creators",
        "title": "美女ぞろい！DXLIVEで「相性抜群の女の子」を見つける最短ルート",
        "date": "2026.03.10",
        "category": "キャスト紹介",
        "excerpt": "DXLIVEで人気のジャンル（人妻・素人・美少女）と、自分に合ったキャストを効率よく探すための検索テクニックを公開します。",
        "url": "popular-casts.html",
        "image": "assets/images/news_thumbnail_4_1773045768252.png"
    },
    {
        "id": 110,
        "categoryId": "news",
        "title": "2026年最新！ライブチャット比較・ランキング。なぜDXLIVEが最強なの？",
        "date": "2026.03.10",
        "category": "サイト比較",
        "excerpt": "他社サイトとDXLIVEを徹底比較。画質、料金、キャストの質、独自機能の観点からDXLIVEが選ばれる理由を解説します。",
        "url": "comparison.html",
        "image": "assets/images/news_thumbnail_3_1773045736171.png"
    },
    {
        "id": 109,
        "categoryId": "knowhow",
        "title": "DXLIVEの「身バレ」を徹底防止！安心して楽しむためのルールと裏技",
        "date": "2026.03.10",
        "category": "プライバシー",
        "excerpt": "知り合いにバレずに遊ぶための設定、履歴削除、匿名決済の方法など、プライバシーを守るための全知識をまとめました。",
        "url": "privacy-rules.html",
        "image": "assets/images/news_thumbnail_2_1773045722676.png"
    },
    {
        "id": 108,
        "categoryId": "knowhow",
        "title": "えっ、見れない！？DXLIVEの「困った」を5分で解決するQ&A",
        "date": "2026.03.10",
        "category": "トラブル解決",
        "excerpt": "繋がらない、重い、メールが届かない等のよくあるトラブルの解決策を、初心者でも分かりやすくまとめました。",
        "url": "trouble-shooting.html",
        "image": "assets/images/news_thumbnail_1_1773045710180.png"
    },
    {
        "id": 107,
        "categoryId": "knowhow",
        "title": "いつでもどこでも！DXLIVEをスマホで快適に楽しむ唯一の方法",
        "date": "2026.03.10",
        "category": "モバイルガイド",
        "excerpt": "アプリ版の有無や、スマホのブラウザでアプリのように快適に視聴するための設定方法を解説します。",
        "url": "mobile-guide.html",
        "image": "assets/images/news_thumbnail_4_1773045768252.png"
    },
    {
        "id": 106,
        "categoryId": "knowhow",
        "title": "2人だけの時間…DXLIVE「2ショット」と「リモちゃ」の極意",
        "date": "2026.03.10",
        "category": "独自機能",
        "excerpt": "2ショットチャットの楽しみ方や、遠隔操作で一体感を味わえる「リモちゃ」機能の魅力を徹底解説！",
        "url": "twoshot-guide.html",
        "image": "assets/images/news_thumbnail_3_1773045736171.png"
    },
    {
        "id": 105,
        "categoryId": "knowhow",
        "title": "【必見】DXLIVEの支払い方法！クレカ不要・匿名で安心な決済術",
        "date": "2026.03.10",
        "category": "支払い方法",
        "excerpt": "クレジットカードなしで利用する方法や、家族にバレないVプリカ・コンビニ払いの匿名決済を解説します。",
        "url": "payment-guide.html",
        "image": "assets/images/news_thumbnail_2_1773045722676.png"
    },
    {
        "id": 104,
        "categoryId": "news",
        "title": "知らないと損！DXLIVEで無料ポイントをガッツリ貰う方法まとめ",
        "date": "2026.03.10",
        "category": "キャンペーン",
        "excerpt": "今すぐ貰える無料お試しポイントの獲得方法から、お得な倍増キャンペーン、クーポンの使い方まで公開！",
        "url": "campaign-info.html",
        "image": "assets/images/news_thumbnail_1_1773045710180.png"
    },
    {
        "id": 103,
        "categoryId": "news",
        "title": "DXLIVEの料金は高い？1分いくら？ポイントの仕組みを完全網羅",
        "date": "2026.03.10",
        "category": "料金・ポイント",
        "excerpt": "DXLIVEの料金体系、1分あたりの単価、お得な購入方法、利用時の節約テクニックを分かりやすく解説。",
        "url": "pricing-guide.html",
        "image": "assets/images/news_thumbnail_4_1773045768252.png"
    },
    {
        "id": 102,
        "categoryId": "knowhow",
        "title": "【完全保存版】DXLIVEの始め方・使い方を初心者が迷わないよう徹底解説！",
        "date": "2026.03.10",
        "category": "初心者ガイド",
        "excerpt": "DXLIVEの登録手順から、最初の使い方のコツ、退会方法まで、初心者が最初に読むべき情報を全てまとめました。",
        "url": "beginner-guide.html",
        "image": "assets/images/news_thumbnail_3_1773045736171.png"
    },
    {
        "id": 101,
        "categoryId": "knowhow",
        "title": "【徹底検証】DXLIVEは怪しい？評判・安全性・違法性をプロが分かりやすく解説！",
        "date": "2026.03.10",
        "category": "評判・安全性",
        "excerpt": "DXLIVEの評判や安全性について徹底検証。怪しい噂や違法性の有無、クレジットカード決済の安全性まで、初心者が気になるポイントをプロが解説します。",
        "url": "safety-guide.html",
        "image": "assets/images/news_thumbnail_1_1773045710180.png"
    },
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


# --- Rewritten Content for Personal Blog Tone ---
# Add your rewritten titles, excerpts, and content here.
# Key should be the original URL or item ID.
REWRITTEN_CONTENT = {
    "https://www.dxlive.com/blog/hearticontip/": {
        "title": "【使ってみた】チャットがハートだらけに！？新機能「ハート応援」が可愛すぎた件",
        "excerpt": "DXLIVEに新しい応援チップが来たよ！コインがハートに変わるだけじゃなくて、画面がめちゃくちゃ華やかになるから推し活が捗りすぎる…✨",
        "content": """
        <h4>チャットのチップが<strong>可愛いハートに大変身！</strong>❤️<br />
        推しの子を応援するとき、画面いっぱいにハートを飛ばせるようになったんだよ。これ、テンション上がる！</h4>

        <figure class="wp-block-image size-large"><img src="https://www.dxlive.com/blog/wp-content/uploads/2026/02/DXGirlchanxxx-1-1024x726.png" alt=""></figure>

        <h3><strong>ハートを送ると、女の子の画面にあなたの気持ちが届くよ✨</strong></h3>

        <figure class="wp-block-image size-large"><img src="https://www.dxlive.com/blog/wp-content/uploads/2026/02/DXGirlchanxxx-1-687x1024.gif" alt=""></figure>

        <h2><strong><mark>3月は「ハートフル月間」！お得な特典も盛りだくさん</mark></strong>🎁</h2>

        <p>今月はとにかくハートがお得！私が気になった特典をまとめてみたよ：</p>
        <ul>
            <li><strong>特典①：</strong>ハートチップが通常より半額の<strong>0.1ポイント</strong>！コスパ良すぎ。</li>
            <li><strong>特典②：</strong>抽選で<strong>2ショット5分無料</strong>が当たるチャンス🎯 毎週チェックしてね。</li>
            <li><strong>特典③：</strong>ホワイトデーの週末はチップゴールがさらにお得に！</li>
        </ul>

        <p>女の子もサムネイルで「ハートして❤️」ってアピールしてる子が多いみたい。推しの喜ぶ顔が見たいなら、今月はハート攻め確定だね！笑</p>

        <p>たくさんのハートで、配信を盛り上げていこう〜！</p>
        """
    },
    "https://www.dxlive.com/blog/bd1025/": {
        "title": "3月にお誕生日の女の子まとめ🎂 お祝いして限定クーポンもらっちゃおう！",
        "excerpt": "今月誕生日を迎えるDXガールズたちを紹介！当日お祝いすると特別なクーポンがもらえる子もいるから、スケジュール帳にメモしておいてね📅",
        "content": """
        <p>3月生まれの女の子たちをまとめてみたよ！バースデー当日に「おめでとう！」って言いに行くだけで、きっと特別な時間が過ごせるはず✨</p>

        <p>なんと…お名前に🎟マークがついてる子は、お誕生日当日限定で<strong>お得なクーポン</strong>を配ってくれるみたいだよ！これは見逃せないね。</p>

        <div class="wp-block-group mb-40">
           <p><strong>3月のバースデーガール（一部抜粋）</strong></p>
           <ul>
               <li>3/1：merotan33ちゃん</li>
               <li>3/3：HINApxpちゃん、xoREIちゃん（🎟）</li>
               <li>3/4：FUMIcc1ちゃん（🎟）</li>
               <li>3/10：SAKURAoggちゃん</li>
               <li>3/14：aaaLEIKAaaaちゃん（🎟）</li>
           </ul>
        </div>

        <p>お気に入りの子のお誕生日はしっかりチェックして、最高の一日にしてあげてね！🎂</p>
        """
    },
    "https://www.dxlive.com/blog/noa1214_event_mar2026/": {
        "title": "noa1214ちゃんの3月イベントが熱い！私物プレゼント抽選会もあるってよ🎁",
        "excerpt": "お気に入り1000人達成＆誕生日！noaちゃんのお祝いイベントが目白押し。激レアな私物プレゼントもあるから、今のうちにチェックしておこう✨",
        "content": """
        <figure class="wp-block-image size-large"><img src="https://www.dxlive.com/blog/wp-content/uploads/2026/03/noa1214_anime_Mar2026.png" alt=""></figure>

        <p>いつも応援してる noa1214ちゃん が、3月はすごいことになってるよ！✨</p>

        <p>2月のバレンタインも盛り上がったけど、今月はさらにお祝いムード全開！</p>

        <div style="background: #fff0f5; padding: 20px; border-radius: 10px; border: 1px solid #ffb6c1;">
            <p><strong>🌸 3月の見逃せないイベント 🌸</strong></p>
            <p><strong>① 3月8日(日) 23時〜：お気に入り1000人達成記念！</strong><br>
            20分参加するだけで、もれなく限定動画がもらえちゃう神イベントだよ。動画、絶対ゲットしたい…！</p>
            
            <p><strong>② 3月28日(土) 23時〜：ノアちゃん聖誕祭！🎂</strong><br>
            こっちが本番！なんとノアちゃんの<strong>私物プレゼント抽選会</strong>があるんだって。1等は当日着用の…（ry）とにかく気合い入れて参加するしかないね！</p>
        </div>

        <p>3/25からの3日間で抽選券がもらえるみたいだから、今のうちに予定空けておこう！<br>noaちゃん、ランキングも急上昇中だし本当に勢いすごいよね。みんなで一緒にお祝いしよう〜！✨</p>
        """
    },
    "https://www.dxlive.com/blog/rururuiiii_event_mar672026/": {
        "title": "【美女降臨】るいちゃんのハートイベントがスタート！ポイントバックも狙えるチャンス✨",
        "excerpt": "あの絶世美女、るいちゃんが週末イベント開催！新機能のハートを贈ると、るいちゃんからお返しのポイントがもらえちゃう！？太っ腹すぎる…！",
        "content": """
        <figure class="wp-block-image size-large"><img src="https://www.dxlive.com/blog/wp-content/uploads/2026/03/rururuiiii-1024x474.png" alt=""></figure>

        <p>3月も「るいちゃん」が遊びに来てくれるよ〜！相変わらずの美しさにため息が出ちゃうね✨</p>

        <h2>開催は3月6日(金)・7日(土)の23時30分ごろから！</h2>

        <p>最初は無料チャットからスタートするみたいだよ。とりあえず顔を出しに行くだけでも価値アリ！💕</p>

        <div style="background: #e6f7ff; padding: 20px; border-radius: 10px; border: 1px solid #91d5ff;">
            <p><strong>💖 るいちゃんからのハートフル特典 💖</strong></p>
            <p>この週末、ハートチップでたくさん応援した人には、るいちゃんからポイントバックのプレゼントがあるみたい。回数が増えるほどお得だよ！</p>
            <ul>
                <li>15回以上 👉 1ポイント返ってくる！</li>
                <li>30回以上 👉 5ポイントも！？</li>
                <li>50回以上 👉 驚きの10ポイント！！</li>
            </ul>
        </div>

        <p>0.1ポイントのハートをコツコツ贈るだけでOKだから、るいちゃん推しは絶対参加してみてね✨</p>
        """
    }
}


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


def rewrite_excerpt(title, excerpt, original_url=None):
    """
    Rewrite/clean the excerpt for display.
    Uses REWRITTEN_CONTENT if available.
    """
    if original_url and original_url in REWRITTEN_CONTENT:
        return REWRITTEN_CONTENT[original_url].get("excerpt", clean_html(excerpt))

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
    # Namespaces for RSS extensions
    namespaces = {
        'content': 'http://purl.org/rss/1.0/modules/content/',
        'dc': 'http://purl.org/dc/elements/1.1/'
    }

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
        
        # --- Filtering: Only include articles that have been rewritten/curated ---
        if link not in REWRITTEN_CONTENT:
            continue
            
        print(f"Adding curated article: {title}")

        # Fetch the full content (content:encoded)
        content_encoded = item.find("content:encoded", namespaces)
        content_html = content_encoded.text if content_encoded is not None else ""

        # Check for rewritten content
        final_title = title
        final_content = content_html
        if link in REWRITTEN_CONTENT:
            # Applying rewritten content
            final_title = REWRITTEN_CONTENT[link].get("title", title)
            final_content = REWRITTEN_CONTENT[link].get("content", content_html)

        date_str = parse_date(pub_date)
        category_id = get_category_id(category)
        excerpt = rewrite_excerpt(title, raw_excerpt, link)

        # Cycle through local images
        image = LOCAL_IMAGES[idx % len(LOCAL_IMAGES)]

        articles.append({
            "id": idx + 1,
            "categoryId": category_id,
            "title": final_title,
            "date": date_str,
            "category": category,
            "excerpt": excerpt,
            "content": final_content,
            "url": f"article.html?id={idx + 1}",
            "originalUrl": link,
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
