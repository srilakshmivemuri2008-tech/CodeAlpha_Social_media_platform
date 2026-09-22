# CodeAlpha_SocialMediaPlatform

A mini social media web app built for the **CodeAlpha Full Stack Development Internship — Task 2**.

Built with **Django** (backend + templating) and **plain HTML/CSS/JavaScript** (frontend).

## Features

- User registration & login/logout (Django auth, custom `User` model with bio + avatar link)
- Create posts (text + optional image link)
- Comment on posts
- Like / unlike posts (instant, no page reload — via `fetch()` + a JSON API endpoint)
- Follow / unfollow other users (instant, same AJAX pattern)
- Personal feed: shows posts from people you follow + your own posts
- Public profile pages with post/follower/following counts
- "Explore" page to discover and follow other users
- Clean, responsive, hand-written CSS (no framework)

## Project structure

```
CodeAlpha_SocialMediaPlatform/
├── manage.py
├── requirements.txt
├── socialapp/          # Django project settings & URL routing
└── social/              # The app: models, views, forms, templates, static files
    ├── models.py         # User, Post, Comment, Like, Follow
    ├── views.py          # Feed, profile, post detail, like/follow AJAX endpoints
    ├── forms.py
    ├── urls.py
    ├── templates/social/
    └── static/social/{css,js}
```

## Setup & run locally

You'll need **Python 3.10+** installed.

```bash
# 1. Go into the project folder
cd CodeAlpha_SocialMediaPlatform

# 2. (Recommended) create a virtual environment
python -m venv venv
source venv/bin/activate        # on Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create the database tables
python manage.py makemigrations
python manage.py migrate

# 5. (Optional) create an admin account
python manage.py createsuperuser

# 6. Run the development server
python manage.py runserver
```

Then open **http://127.0.0.1:8000/** in your browser.

- Sign up for a new account at `/register/`
- Go to `/explore/` to find and follow other users (create 2-3 test accounts in
  separate browser windows/incognito tabs to see the feed & follow system work)
- `/admin/` gives you the Django admin panel if you created a superuser

## How the "instant" like/follow buttons work

The like and follow buttons don't submit a normal form — `social/static/social/js/main.js`
sends a `fetch()` POST request to a small JSON API view (`toggle_like` / `toggle_follow` in
`views.py`), and updates just that button's text/count in the DOM with the response.
This is a simple, framework-free way to get an AJAX-style interaction with plain JavaScript.

## Notes for the internship submission

- Push this folder as-is to a GitHub repo named `CodeAlpha_SocialMediaPlatform`
- Remember to add a `.gitignore`-respecting commit (already included) so `db.sqlite3`
  and `venv/` aren't pushed
- Record your video walkthrough showing: signup/login, creating a post, liking,
  commenting, following another user, and the feed updating accordingly
