import os
import json
import re
from PIL import Image, ImageEnhance

# We have 4 new events
events = [
    {
        "url": "event-noa1214ちゃんバレンタインイベント-2月14日.html",
        "base": "assets/images/eyecatch_noa_announcement_v2.png",
        "output": "assets/images/events/eyecatch_noa_valentine.png",
        "tint": (255, 200, 200) # pink/red tint
    },
    {
        "url": "event-るいちゃんハートで応援イベント開催.html",
        "base": "assets/images/eyecatch_heart_chip_v2.png",
        "output": "assets/images/events/eyecatch_rui_heart.png",
        "tint": (255, 150, 200) # deep pink
    },
    {
        "url": "event-バレンタイン特別リモちゃ企画.html",
        "base": "assets/images/eyecatch_event.png",
        "output": "assets/images/events/eyecatch_valentine_rimocha.png",
        "tint": (255, 180, 180) # light red
    },
    {
        "url": "event-女の子の写真イベント一覧.html",
        "base": "assets/images/eyecatch_event.png",
        "output": "assets/images/events/eyecatch_photo_events.png",
        "tint": (200, 200, 255) # blue tint
    }
]

def apply_tint(image_path, output_path, tint_color):
    if not os.path.exists(image_path):
        print(f"Base {image_path} not found")
        return False
    try:
        img = Image.open(image_path).convert('RGB')
        # Create a solid color image
        color_layer = Image.new('RGB', img.size, tint_color)
        # Blend the image with the color layer
        out = Image.blend(img, color_layer, alpha=0.3)
        # Enhance color a bit
        enhancer = ImageEnhance.Color(out)
        out = enhancer.enhance(1.2)
        out.save(output_path)
        print(f"Created {output_path}")
        return True
    except Exception as e:
        print(f"Failed to tint {image_path}: {e}")
        return False

# Load news JSON
with open('news.json', 'r', encoding='utf-8') as f:
    news_data = json.load(f)

for ev in events:
    success = apply_tint(ev['base'], ev['output'], ev['tint'])
    if success:
        # Update JSON
        for item in news_data:
            if item.get('url') == ev['url']:
                item['image'] = ev['output']
                break
        
        # Update HTML
        if os.path.exists(ev['url']):
            with open(ev['url'], 'r', encoding='utf-8') as f:
                html = f.read()
            html = re.sub(r'assets/images/eyecatch_event.png', ev['output'], html)
            with open(ev['url'], 'w', encoding='utf-8') as f:
                f.write(html)
                print(f"Updated HTML for {ev['url']}")

# Save updated JSON
with open('news.json', 'w', encoding='utf-8') as f:
    json.dump(news_data, f, ensure_ascii=False, indent=2)
print("Done updating json and html.")

