import json
import urllib.request
import re
from xml.etree import ElementTree as ET
# Note: For genuine LLM rewriting, we would import openai or google.generativeai here.

RSS_FEED_URL = "https://www.dxlive.com/blog/feed/"
OUTPUT_JSON = "news.json"
MAX_ITEMS = 6

def fetch_rss_feed(url):
    """Fetches and parses the RSS feed."""
    print(f"Fetching RSS feed from {url}...")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            xml_data = response.read()
            return ET.fromstring(xml_data)
    except Exception as e:
        print(f"Error fetching RSS: {e}")
        return None

def extract_image_url(content_encoded):
    """Simple regex to extract the first image from content."""
    if not content_encoded:
        return None
    match = re.search(r'img.*?src="(.*?)"', content_encoded)
    return match.group(1) if match else None

def rewrite_with_llm(title, excerpt):
    """
    Mock function representing an LLM API call.
    In production, this would send the text to OpenAI/Gemini to summarize and apply the blog persona.
    """
    # Example AI Transformation Logic Placeholder
    # response = openai.ChatCompletion.create(...)
    # return response.text
    
    # For now, we just return a slightly cleaned up version of the excerpt to simulate processing
    clean_excerpt = re.sub(r'<[^>]+>', '', excerpt).strip()
    # Let's truncate and add an ellipsis for the summary
    if len(clean_excerpt) > 100:
        clean_excerpt = clean_excerpt[:97] + "..."
    
    return {
        "title": f"【更新】{title}", # Example of LLM tweaking the title
        "excerpt": clean_excerpt
    }

def process_feed(root):
    """Processes the parsed XML and generates a list of rewritten articles."""
    articles = []
    
    # Namespaces usually present in WP RSS
    namespaces = {'content': 'http://purl.org/rss/1.0/modules/content/'}
    
    channel = root.find("channel")
    items = channel.findall("item")
    
    for idx, item in enumerate(items[:MAX_ITEMS]):
        title = item.findtext("title", "")
        link = item.findtext("link", "")
        pub_date = item.findtext("pubDate", "")
        # Simplistic date conversion
        if pub_date:
            # Example format: Wed, 06 Mar 2026 12:00:00 +0000 -> 2026.03.06
            parts = pub_date.split(" ")
            if len(parts) >= 4:
                months = {"Jan":"01", "Feb":"02", "Mar":"03", "Apr":"04", "May":"05", "Jun":"06", "Jul":"07", "Aug":"08", "Sep":"09", "Oct":"10", "Nov":"11", "Dec":"12"}
                date_str = f"{parts[3]}.{months.get(parts[2], '01')}.{parts[1].zfill(2)}"
            else:
                date_str = pub_date
        else:
            date_str = "N/A"
            
        category = item.findtext("category", "ニュース")
        content = item.find("content:encoded", namespaces)
        content_text = content.text if content is not None else item.findtext("description", "")
        
        # 1. Extract Image
        image_url = extract_image_url(content_text)
        # Fallback placeholder if no image found in post
        if not image_url:
             image_url = "https://images.unsplash.com/photo-1516280440502-869269ce3244?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
             
        # 2. Extract raw description
        raw_excerpt = item.findtext("description", "")
        
        # 3. "Rewrite" with LLM
        rewritten_data = rewrite_with_llm(title, raw_excerpt)

        articles.append({
            "id": idx + 1,
            "title": rewritten_data["title"],
            "date": date_str,
            "category": category,
            "excerpt": rewritten_data["excerpt"],
            "url": link,
            "image": image_url
        })
        
    return articles

if __name__ == "__main__":
    root = fetch_rss_feed(RSS_FEED_URL)
    if root:
        rewritten_articles = process_feed(root)
        
        # Save to JSON
        with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
            json.dump(rewritten_articles, f, ensure_ascii=False, indent=2)
            
        print(f"Successfully scraped and simulated rewriting of {len(rewritten_articles)} articles.")
        print(f"Saved to {OUTPUT_JSON}")
