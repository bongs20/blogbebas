<img width="1263" height="657" alt="image" src="https://github.com/user-attachments/assets/91591bd3-5869-4dbf-9a87-d8f3c0cd2661" />

BlogBebas - expressive micro blog with voting (Django)

BlogBebas is a simple, expressive blogging platform where users can post, comment, and vote. It supports categories, profiles with avatars, and media attachments.

Quick start

1) Install

    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

2) Migrate and seed (optional)

    python manage.py migrate
    python manage.py seed_demo
    python manage.py createsuperuser  # optional

3) Run

    python manage.py runserver

Open http://127.0.0.1:8000

Key features
- Auth (register/login/logout), profiles with avatar and bio
- Posts and comments with attachments (image/video/audio/file or URL)
- Voting with scores
- Categories: user-created; admins verify/unverify/delete; search in sidebar
- Home: Posts of the Day, sort by New/Top, pagination
- Admin: branded Django admin, manage all content
- Responsive UI with Bootstrap 5 and mobile FAB

Docs
- <a href="docs/FEATURES.md">
- docs/ARCHITECTURE.md
- docs/SETUP.md
