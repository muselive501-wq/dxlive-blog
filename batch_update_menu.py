import os
import re

NEW_NAV = """                <a href="index.html">Home</a>
                <a href="registration-guide.html">登録方法</a>
                <a href="category.html?type=usage">使い方</a>
                <a href="category.html?type=events">イベント情報</a>
                <a href="category.html?type=creators">キャスト向け記事</a>"""

SEARCH_CONTAINER = """                <div class="search-container">
                    <form action="search.html" method="get">
                        <input type="text" name="q" placeholder="記事を検索..." class="search-input" required>
                        <button type="submit" class="search-btn">🔍</button>
                    </form>
                </div>"""

def update_html_menu(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Find the nav-links container and replace its content
    # Look for the block between <nav class="nav-links"> and </nav>
    pattern = re.compile(r'(<nav class="nav-links">)(.*?)(</nav>)', re.DOTALL)
    
    def replace_nav(match):
        # Keep the original search bar if it exists, or add it if missing
        if 'search-container' in match.group(2):
            # Extract existing search bar to preserve it (though we have a standard one)
            search_match = re.search(r'(<div class="search-container">.*?</div>)', match.group(2), re.DOTALL)
            current_search = search_match.group(1) if search_match else SEARCH_CONTAINER
            return f"{match.group(1)}\n{NEW_NAV}\n\n{current_search}\n{match.group(3)}"
        else:
            return f"{match.group(1)}\n{NEW_NAV}\n\n{SEARCH_CONTAINER}\n{match.group(3)}"

    new_content = pattern.sub(replace_nav, content)
    
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def main():
    updated_count = 0
    for filename in os.listdir('.'):
        if filename.endswith('.html'):
            if update_html_menu(filename):
                print(f"Updated menu in {filename}")
                updated_count += 1
    print(f"Finished. Updated {updated_count} files.")

if __name__ == "__main__":
    main()
