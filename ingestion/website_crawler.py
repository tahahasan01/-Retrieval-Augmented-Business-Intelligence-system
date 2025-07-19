import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os
import time

visited = set()

# Check robots.txt for allowed paths
from urllib.robotparser import RobotFileParser

def is_allowed(url, user_agent="*"):
    parsed = urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    rp = RobotFileParser()
    try:
        rp.set_url(robots_url)
        rp.read()
        return rp.can_fetch(user_agent, url)
    except Exception:
        return True  # If robots.txt can't be read, assume allowed


def crawl(url, domain, depth=2, delay=1):
    if url in visited or depth == 0:
        return
    if not is_allowed(url):
        print(f"Blocked by robots.txt: {url}")
        return
    visited.add(url)
    try:
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        # Save page content
        fname = urlparse(url).path.replace('/', '_') or 'index'
        fname = fname.split('?')[0]  # Remove query params
        with open(f"data/unstructured/{fname}.html", "w", encoding="utf-8") as f:
            f.write(resp.text)
        print(f"Saved {url}")
        # Find and crawl links
        for link in soup.find_all("a", href=True):
            next_url = urljoin(url, link['href'])
            if urlparse(next_url).netloc == domain and next_url not in visited:
                time.sleep(delay)
                crawl(next_url, domain, depth-1, delay)
    except Exception as e:
        print(f"Failed to crawl {url}: {e}")

# Example usage:
# start_url = "https://en.wikipedia.org/wiki/Artificial_intelligence"
# domain = urlparse(start_url).netloc
# crawl(start_url, domain, depth=2, delay=1) 