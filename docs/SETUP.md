# Setup and Local Development

## Prerequisites
- Python 3.12+
- pip, venv

## Install
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Migrate & seed
```bash
python manage.py migrate
python manage.py seed_demo  # optional: loads demo users, categories, posts, comments, votes
python manage.py createsuperuser  # optional
```

## Run
```bash
python manage.py runserver
```

Open http://127.0.0.1:8000

## Media files
- Uploaded files are stored in `media/`. In dev, they’re served via Django with `MEDIA_URL=/media/`.

## Environment tweaks
- DEBUG is on by default.
- Change site branding or meta in `templates/base.html`.
