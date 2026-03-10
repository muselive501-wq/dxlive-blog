import os
import glob

html_files = glob.glob('*.html')
updated_count = 0
for file in html_files:
    try:
        with open(file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        original_content = content
        # Update header logo
        content = content.replace(
            '<div class="logo">DXLIVE<span>FAN BLOG</span></div>',
            '<a href="index.html" class="logo">DXLIVE<span>FAN BLOG</span></a>'
        )
        
        # Update footer logo
        content = content.replace(
            '<div class="footer-logo">DXLIVE<span>FAN BLOG</span></div>',
            '<a href="index.html" class="footer-logo">DXLIVE<span>FAN BLOG</span></a>'
        )
        
        if content != original_content:
            with open(file, 'w', encoding='utf-8') as f:
                f.write(content)
            updated_count += 1
            print(f"Updated {file}")
            
    except Exception as e:
        print(f"Error processing {file}: {e}")

print(f"Successfully updated logo links in {updated_count} HTML files.")
