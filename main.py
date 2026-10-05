import feedparser
import json
from datetime import datetime, timedelta
from collections import Counter

# Simple keyword-based scorer (no external LLM needed)
KEYWORDS = ['ai', 'llm', 'gpt', 'openai', 'agent', 'model', 'release', 'research']

def fetch_headlines(url='https://hnrss.org/frontpage'):
    feed = feedparser.parse(url)
    items = []
    for entry in feed.entries[:20]:  # limit to 20
        items.append({
            'title': entry.title,
            'link': entry.link,
            'published': entry.get('published', datetime.now().isoformat()),
            'score': 0
        })
    return items

def score_items(items):
    for item in items:
        title_lower = item['title'].lower()
        item['score'] = sum(1 for kw in KEYWORDS if kw in title_lower)
    return items

def select_top(items, n=3):
    return sorted(items, key=lambda x: x['score'], reverse=True)[:n]

def generate_digest(items):
    lines = [f"# Daily AI Digest - {datetime.now().strftime('%Y-%m-%d')}", ""]
    for item in items:
        lines.append(f"- **{item['title']}** ({item['score']} pts)")
        lines.append(f"  Link: {item['link']}")
    return '\n'.join(lines)

if __name__ == '__main__':
    items = fetch_headlines()
    scored = score_items(items)
    top = select_top(scored, 3)
    digest = generate_digest(top)
    print(digest)
    # Save as markdown file
    with open('digest.md', 'w') as f:
        f.write(digest)
    print('\nSaved to digest.md')