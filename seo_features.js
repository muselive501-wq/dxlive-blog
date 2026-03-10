// seo_features.js
document.addEventListener("DOMContentLoaded", () => {
    // 1. Generate Table of Contents (TOC)
    const articleBody = document.querySelector('.article-body');
    const h2Elements = articleBody ? articleBody.querySelectorAll('h2') : [];
    const tocContainer = document.querySelector('.toc-container');
    const tocList = document.getElementById('toc-list');
    
    if (h2Elements.length > 0 && tocContainer && tocList) {
        h2Elements.forEach((h2, index) => {
            // Assign ID to h2 if not present
            if (!h2.id) {
                h2.id = 'heading-' + index;
            }
            
            // Create TOC list item
            const li = document.createElement('li');
            const a = document.createElement('a');
            a.href = '#' + h2.id;
            a.textContent = h2.textContent;
            
            // Smooth scroll
            a.addEventListener('click', (e) => {
                e.preventDefault();
                const targetId = e.target.getAttribute('href').substring(1);
                const targetElement = document.getElementById(targetId);
                if (targetElement) {
                    window.scrollTo({
                        top: targetElement.offsetTop - 80, // Offset for sticky header
                        behavior: 'smooth'
                    });
                }
            });
            
            li.appendChild(a);
            tocList.appendChild(li);
        });
    } else if (tocContainer) {
        // Hide TOC if no h2 elements found
        tocContainer.style.display = 'none';
    }

    // 2. Load Related Articles
    const relatedContainer = document.getElementById('related-articles-grid');
    if (relatedContainer) {
        const currentPath = window.location.pathname.split('/').pop();
        
        // Fetch news.json
        fetch('news.json')
            .then(response => response.json())
            .then(news => {
                // Find current article category
                const currentArticle = news.find(item => item.url === currentPath);
                if (currentArticle) {
                    const currentCategory = currentArticle.categoryId;
                    
                    // Filter articles by same category, exclude current
                    const relatedArticles = news.filter(item => item.categoryId === currentCategory && item.url !== currentPath);
                    
                    // Shuffle or take first 3
                    const displayArticles = relatedArticles.slice(0, 3);
                    
                    if (displayArticles.length > 0) {
                        displayArticles.forEach(article => {
                            const card = document.createElement('div');
                            card.className = 'article-card';
                            card.innerHTML = `
                                <img src="${article.image}" alt="${article.title}" class="article-image">
                                <div class="article-content">
                                    <div class="article-meta">
                                        <span class="category-badge">${article.category}</span>
                                        <span class="article-date">${article.date}</span>
                                    </div>
                                    <h3 class="article-title">${article.title}</h3>
                                    <a href="${article.url}" class="read-more">READ MORE</a>
                                </div>
                            `;
                            // Make whole card clickable
                            card.addEventListener('click', () => {
                                window.location.href = article.url;
                            });
                            relatedContainer.appendChild(card);
                        });
                    } else {
                        // Fallback: show latest 3 articles if no related found
                        const latest = news.filter(item => item.url !== currentPath).slice(0, 3);
                        latest.forEach(article => {
                            const card = document.createElement('div');
                            card.className = 'article-card';
                            card.innerHTML = `
                                <img src="${article.image}" alt="${article.title}" class="article-image">
                                <div class="article-content">
                                    <div class="article-meta">
                                        <span class="category-badge">${article.category}</span>
                                        <span class="article-date">${article.date}</span>
                                    </div>
                                    <h3 class="article-title">${article.title}</h3>
                                    <a href="${article.url}" class="read-more">READ MORE</a>
                                </div>
                            `;
                            card.addEventListener('click', () => {
                                window.location.href = article.url;
                            });
                            relatedContainer.appendChild(card);
                        });
                    }
                }
            })
            .catch(error => console.error('Error loading related articles:', error));
    }
});
