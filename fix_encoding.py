import os

def fix_file(path):
    with open(path, 'rb') as f:
        data = f.read()
    
    try:
        # Try to recover: The data was written as CP932 (default PS) 
        # but it was a string that was read from UTF-8 using CP932.
        # So: Original UTF-8 Bytes -> Read as CP932 (String) -> Written as CP932 (Bytes)
        # To fix: Read Bytes (as CP932) -> String -> Encode as CP932 (Original Bytes) -> Decode as UTF-8
        
        # Actually, simpler: The file is currently CP932.
        # Let's read it as CP932, encode to bytes using CP932, then decode as UTF-8.
        text = data.decode('cp932', errors='replace')
        original_bytes = text.encode('cp932', errors='replace')
        fixed_text = original_bytes.decode('utf-8', errors='replace')
        
        # Also fix the specific string replacement issue if any
        fixed_text = fixed_text.replace('繧AN BLOG', 'FAN BLOG')
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(fixed_text)
        print(f"Fixed {path}")
    except Exception as e:
        print(f"Failed to fix {path}: {e}")

files = [
    'index.html', 'comparison.html', 'category.html', 'campaign-info.html',
    'article.html', 'about.html', 'twoshot-guide.html', 'trouble-shooting.html',
    'safety-guide.html', 'privacy-rules.html', 'pricing-guide.html',
    'popular-casts.html', 'payment-guide.html', 'mobile-guide.html',
    'lovense_guide.html', 'beginner-guide.html', 'update_news.py'
]

for f in files:
    if os.path.exists(f):
        fix_file(f)
