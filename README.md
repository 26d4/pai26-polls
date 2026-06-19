# Polls app
Simple polls app using Django, DRF and HTMX

Anyone can vote, only registered users can make polls

Note: this was made in a big hurry, so don't expect anything remarkable

Contents of `polls_site`:

- `polls_site` - core configuration
- `polls_api` - models, REST API, SSE endpoint for updating vote counts
- `polls_web` - web pages, HTMX, templates, depends on api

The app can be started with docker compose:

- set the `DJANGO_SECRET_KEY` env. variable
- optionally load example data with `docker compose run --rm loaddata`
- then use `docker compose up`
