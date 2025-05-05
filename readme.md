# 🚀 Headliner

PagePeek is a lightweight Flask API that fetches the `<title>` tag of any provided webpage URL. It’s designed to power blog systems (like yours) that need to convert plain URLs into rich, clickable links with actual page titles.

## ✨ Features

- 🔗 Fetches the `<title>` of any webpage.

- ⚡ In-memory + SQLite caching to avoid redundant requests.

- 🛡 Handles errors gracefully (invalid URLs, timeouts, etc.).

- 🔌 Easy to integrate with any frontend (React, etc.).

- 🪄 Hosted easily on PythonAnywhere or any Flask-friendly platform.

## API

- **POST /get-title**
  - Request body:

      ```json
      { "url": "https://example.com" }
      ```

  - Response:

      ```json
      { "title": "Example Domain" }
      ```

✅ Caches titles in SQLite to reduce duplicate fetches.

## Setup

Set allowed origins in `.env`:

```bash
ALLOWED_ORIGINS=https://your-frontend.com,https://other-allowed.com
```

```bash
pip install -r requirements.txt
```

- Debug:

```bash
python app.py
```

- Production:

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```
