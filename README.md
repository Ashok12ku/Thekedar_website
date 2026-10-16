# Thekedar Interiors & Exteriors — Django Website

A complete, mobile-responsive Django + Bootstrap 5 website for a main
contractor (thekedar) offering Interior & Exterior design and execution
services: Carpentry, Painting, Lighting, Tiles, Decoration, and Turnkey
Projects.

---

## 1. Project Setup

```bash
# 1. Unzip and enter the project
cd thekedar_website

# 2. Create & activate a virtual environment
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply database migrations
python manage.py migrate

# 5. (Optional but recommended) Seed sample Services, Stats & Testimonials
python manage.py seed_demo_data

# 6. Create an admin login
python manage.py createsuperuser

# 7. Run the development server
python manage.py runserver
```

Visit:
- **Website:** http://127.0.0.1:8000/
- **Admin panel:** http://127.0.0.1:8000/admin/

> `seed_demo_data` does NOT add Portfolio photos (it needs real image files).
> Add your project photos from the admin under **Portfolio Items**.

---

## 2. Directory Structure

```
thekedar_website/
├── manage.py
├── requirements.txt
├── db.sqlite3                     # created after migrate
├── contractor_project/            # project-level settings
│   ├── settings.py
│   ├── urls.py                    # includes core.urls + media serving
│   ├── wsgi.py / asgi.py
├── core/                          # main app
│   ├── models.py                  # Service, PortfolioItem, Inquiry, Testimonial, CompanyStat
│   ├── forms.py                   # InquiryForm with phone validation
│   ├── views.py                   # home, about, services, portfolio, contact
│   ├── urls.py                    # app-level routes
│   ├── admin.py                   # lead-tracking friendly admin config
│   ├── context_processors.py      # exposes company info to all templates
│   └── management/commands/
│       └── seed_demo_data.py
├── templates/core/
│   ├── base.html                  # navbar, footer, WhatsApp button
│   ├── home.html
│   ├── about.html
│   ├── services.html
│   ├── service_detail.html
│   ├── portfolio.html
│   └── contact.html
├── static/
│   ├── css/style.css
│   └── js/main.js
└── media/                         # uploaded images land here (dev)
```

---

## 3. Key Features

- **Home:** Hero banner, quick lead form (also posts to the same page),
  animated stats counter, service highlights, featured portfolio,
  testimonial carousel, CTA banner.
- **About:** Experience, 4-step process, quality commitment.
- **Services:** Card grid pulling from the `Service` model + individual
  service detail pages (`/services/<slug>/`).
- **Portfolio:** Category-filterable gallery with pagination
  (`?category=interior`, `?category=exterior`, etc.), supports
  Before/After category.
- **Contact / Get Quote:** Full `InquiryForm` (Name, Phone, Email,
  Location, Service, Budget Range, Message) with server-side validation
  (Indian 10-digit mobile number check).
- **Admin panel:** Every model is registered with sensible `list_display`,
  `list_filter`, and `search_fields`. The `Inquiry` admin includes a
  **status** workflow (New → Contacted → Site Visit → Quoted → Won/Lost)
  with bulk actions, so it doubles as a simple CRM for your leads.
- **WhatsApp floating button** and clickable phone/email links site-wide
  (edit the numbers in `settings.py`).

---

## 4. Editing Business Info

Open `contractor_project/settings.py` and update:

```python
COMPANY_NAME = "Thekedar Interiors & Exteriors"
COMPANY_PHONE = "+91-98XXXXXXXX"
COMPANY_WHATSAPP = "919800000000"   # digits only, used for wa.me links
COMPANY_EMAIL = "info@thekedarinteriors.com"
COMPANY_ADDRESS = "Raebareli, Uttar Pradesh, India"
```

These automatically appear in the navbar, footer, WhatsApp button, and
contact page — no template edits needed.

---

## 5. Adding Content (No Coding Needed)

Log in at `/admin/` and manage:

- **Services** — title, description, icon (use any class name from
  [Bootstrap Icons](https://icons.getbootstrap.com/), e.g. `bi-hammer`),
  and an optional image.
- **Portfolio Items** — title, category, main image, optional
  before/after images, location, date.
- **Testimonials** — client name, review, star rating, project type,
  publish/unpublish toggle.
- **Company Stats** — the 4 counter numbers on the Home page (Years of
  Experience, Projects Completed, etc.) — fully editable, no code change
  needed when your numbers grow.
- **Inquiries** — every lead submitted from the site lands here. Filter
  by status/service/budget, update status as you follow up, and use bulk
  actions to mark leads Contacted / Won / Lost.

---

## 6. Switching to PostgreSQL (Production)

1. `pip install psycopg2-binary`
2. In `settings.py`, replace the `DATABASES` dict with the commented
   PostgreSQL block already included in the file (uses environment
   variables `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`).
3. Run `python manage.py migrate` again against the new database.

---

## 7. Deployment Checklist

Before going live:

- [ ] Set `DEBUG = False` in `settings.py`
- [ ] Set a new, secret `SECRET_KEY` (use an environment variable)
- [ ] Set `ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']`
- [ ] Switch to PostgreSQL (see above)
- [ ] Run `python manage.py collectstatic` and serve `/staticfiles/`
      via your web server (nginx) or `whitenoise`
- [ ] Serve `/media/` (portfolio photos) via nginx or cloud storage
      (e.g. AWS S3 via `django-storages`) — the dev server's media
      serving in `urls.py` only runs when `DEBUG = True`
- [ ] Put Gunicorn/Daphne behind nginx (don't use `runserver` in production)
- [ ] Set up a real email backend (currently console backend) if you want
      email notifications on new inquiries — see `EMAIL_BACKEND` in
      Django docs and update `settings.py`
- [ ] Enable HTTPS (`SECURE_SSL_REDIRECT`, HSTS settings)

---

## 8. Notes on the Frontend

Bootstrap 5 and Bootstrap Icons are loaded via CDN in `base.html` — no
build step (npm/webpack) required. All custom styling lives in
`static/css/style.css`, and the primary brand color (a terracotta
orange, `--primary: #d9631e`) can be changed in one place at the top of
that file to instantly re-theme the whole site.
