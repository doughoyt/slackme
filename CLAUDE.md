# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SlackMe is a Flask-based webhook service that forwards SMS messages to Slack. Created to work around Anveo VoIP SMS limitations, it receives incoming SMS messages via GET requests and posts them to a Slack channel using the Slack Web API.

## Architecture

**Single-file application** (`app.py`):
- Flask web server with ProxyFix middleware for reverse proxy deployment
- Slack SDK integration via `slackAlert()` helper function
- Query parameter-based authentication using pre-shared token
- Environment variable configuration via python-dotenv

**Authentication flow**: GET request → validate auth token → validate required params → format Slack blocks → send to #Alerts channel

**Key limitation**: Uses GET requests with query parameters (not POST) because the sending service doesn't support POST or custom headers. Relies on HTTPS and periodic token rotation for security.

## Development Commands

**Setup environment**:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -r dev-requirements.txt
```

**Run tests**:
```bash
pytest                    # Run all tests
pytest test_app.py        # Run specific test file
pytest -v                 # Verbose output
pytest -k test_name       # Run specific test by name
```

**Run locally**:
```bash
python app.py             # Runs on port 5000
# or
flask run                 # Alternative using Flask CLI
```

**Docker**:
```bash
docker build -t slackme .
docker run -p 5000:5000 -e SLACK_BOT_TOKEN=xxx -e AUTH_TOKEN=xxx slackme
```

## Required Environment Variables

- `SLACK_BOT_TOKEN`: Slack bot OAuth token for posting messages
- `AUTH_TOKEN`: Pre-shared secret for authenticating incoming requests

Create a `.env` file in the project root for local development (already gitignored).

## Testing

Tests use pytest with pytest-mock for Slack API mocking. The test suite in `test_app.py` covers:
- Auth token validation (missing, incorrect)
- Required parameter validation (from, message)
- Successful message handling with mocked Slack calls

Mock the `slackAlert` function to prevent actual Slack API calls during tests.

## Code Patterns

- **Error handling**: Uses Flask's `abort()` with HTTP status codes and descriptions
- **Slack message format**: Messages use Block Kit with sections and dividers
- **Channel targeting**: Currently hard-coded to `#Alerts` in app.py:72
- **WSGI configuration**: ProxyFix configured for x-for, x-host, x-prefix, x-proto headers
