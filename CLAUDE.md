# CLAUDE.md — Master Template

Reusable Django 4.2 blank-slate project. All apps use generic names and are independently functional.

## Commands

```bash
# Activate virtual environment (create first if needed)
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy and configure environment
cp .env.example .env
# Edit .env: set DJANGO_SECRET_KEY

# Database migrations
python manage.py makemigrations
python manage.py migrate

# Create admin superuser
python manage.py createsuperuser

# Seed sample data
python manage.py seed

# Run development server
python manage.py runserver

# Collect static files (production)
python manage.py collectstatic
```

## Architecture

12 apps under `apps/` directory, all independently functional:

- **`core`** — SiteSettings singleton, HeroSlide, FeaturedBrand, HomeSectionCard, FAQ, SiteVisitCounter. Context processor injects `site_settings` and `nav_categories` everywhere. Three middleware classes (visit counter, form throttle, admin login throttle).
- **`catalog`** — Generic item catalog. Brand, Category, ItemType, Item, ItemImage models. Filters by brand, category, condition. `hide_price` flag. ManyToMany to promotions.
- **`promotions`** — Promotion model with 5 template types. PromotionPage (one-to-one), PromotionBlock, PromotionCTA inlines.
- **`blog`** — BlogCategory, BlogTag, BlogPost. Reading time property. Draft/published workflow.
- **`gallery`** — GalleryPhoto, GalleryVideo. `embed_url` property handles YouTube/Vimeo URLs.
- **`events`** — EventCategory (free-text with color), Event. Subscribe endpoint returns JSON.
- **`team`** — Department, TeamMember. Grouped by department in view.
- **`testimonials`** — Testimonial with star rating and featured flag.
- **`inquiries`** — Abstract BaseInquiry. Four concrete types: ContactInquiry, ItemInquiry, ServiceInquiry, QuoteRequest. Honeypot spam protection. CSV export admin action.
- **`services`** — Service, ServiceFeature (inline), ServiceAppointment with status workflow.
- **`accounts`** — Custom email-based User (replaces Django's default). Email is USERNAME_FIELD.
- **`workflows`** — Generic WorkflowType → WorkflowStage → WorkflowItem pipeline. WorkflowNote for audit trail. Staff dashboard view.

## Key Patterns

- **All apps**: `apps.py` sets both `name` (e.g. `apps.catalog`) and `label` (e.g. `catalog`).
- **Cross-app imports**: Always inside try/except blocks or function bodies to avoid circular imports.
- **AUTH_USER_MODEL**: All ForeignKeys use `settings.AUTH_USER_MODEL` string, never direct import.
- **Storage**: `ResizingFileSystemStorage` auto-converts uploads to progressive JPEG, fixes EXIF rotation, caps at 3840px.
- **Design tokens**: All CSS uses variables in `static/css/theme.css`. To rebrand: change `--color-primary`, `--font-heading`, `--font-body`.
- **No frontend build step** — plain HTML/CSS/JS only.
- **Databases**: SQLite (default), PostgreSQL (if DATABASE_URL set), MySQL (if MYSQL_HOST set).

## To Adapt for a New Client

1. Change `--color-primary` in `static/css/theme.css`
2. Update font variables and import a Google Font if desired
3. Run `python manage.py seed` and add initial content via admin
4. Update `SiteSettings` with real business name, contact info, hours
5. Remove or rename apps that aren't needed
6. Set `DJANGO_SECRET_KEY` and `DJANGO_DEBUG=false` in production `.env`

## Notes

- The `/Users/shwetanshu/Documents/Web Development/Events Module/` directory has been superseded by `apps/events/` in this project.
- Admin URL: `/admin/`
- Health check endpoint: `/healthz/`
- Workflows dashboard (login required): `/workflows/`
