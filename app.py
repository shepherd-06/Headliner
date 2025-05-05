from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import hashlib
import sqlite3
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables
load_dotenv()
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "").split(",")

# Initialize simple SQLite cache
conn = sqlite3.connect("cache.sqlite", check_same_thread=False)
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS title_cache (
        url_hash TEXT PRIMARY KEY,
        title TEXT
    )
''')
conn.commit()


def get_cached_title(url):
    url_hash = hashlib.md5(url.encode()).hexdigest()
    c.execute("SELECT title FROM title_cache WHERE url_hash = ?", (url_hash,))
    row = c.fetchone()
    return row[0] if row else None


def save_title_to_cache(url, title):
    url_hash = hashlib.md5(url.encode()).hexdigest()
    c.execute(
        "INSERT OR REPLACE INTO title_cache (url_hash, title) VALUES (?, ?)", (url_hash, title))
    conn.commit()


@app.before_request
def check_origin():
    origin = request.headers.get("Origin")
    if origin:
        origin = origin.rstrip("/")
    if origin not in [o.strip().rstrip("/") for o in ALLOWED_ORIGINS]:
        return jsonify({"error": "Unauthorized origin"}), 403


@app.route('/get-titles', methods=['POST'])
def get_titles():
    data = request.get_json()
    urls = data.get('urls') if data else None

    if not urls or not isinstance(urls, list):
        return jsonify({"error": "Expected 'urls' as a list in JSON body"}), 400

    results = []

    for url in urls:
        if not isinstance(url, str) or not url.strip():
            results.append({
                "url": url,
                "title": "Invalid URL"
            })
            continue

        url = url.strip()

        # Check cache first
        cached = get_cached_title(url)
        if cached:
            results.append({
                "url": url,
                "title": cached
            })
            continue

        try:
            resp = requests.get(url, timeout=5)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, 'html.parser')
            title = soup.title.string.strip() if soup.title else "No title found"

            # Save to cache
            save_title_to_cache(url, title)

            results.append({
                "url": url,
                "title": title
            })
        except Exception as e:
            results.append({
                "url": url,
                "title": f"Error: {str(e)}"
            })

    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)
