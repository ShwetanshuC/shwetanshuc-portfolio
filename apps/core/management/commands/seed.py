"""
Seed command — creates sample data for all installed apps.
Run with: python manage.py seed
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify


class Command(BaseCommand):
    help = "Seed the database with sample data."

    def handle(self, *args, **options):
        self.stdout.write("Seeding database...")

        # ---------------------------------------------------------------
        # SiteSettings
        # ---------------------------------------------------------------
        from apps.core.models import SiteSettings
        settings, _ = SiteSettings.objects.get_or_create(pk=1)
        settings.site_name = "Acme Business"
        settings.tagline = "Quality you can trust."
        settings.phone_display = "(555) 123-4567"
        settings.phone_tel = "+15551234567"
        settings.email = "hello@acmebusiness.com"
        settings.address = "123 Main Street\nAnytown, USA 00000"
        settings.hours = "Mon–Fri 9 AM–6 PM\nSat 10 AM–4 PM\nSun Closed"
        settings.save()
        self.stdout.write(self.style.SUCCESS("  SiteSettings created"))

        # ---------------------------------------------------------------
        # HeroSlides (text-only, no images in seed)
        # ---------------------------------------------------------------
        from apps.core.models import HeroSlide
        slides_data = [
            {"title": "Welcome to Acme Business", "subtitle": "Discover our full range of products and services.", "sort_order": 0},
            {"title": "Quality Products", "subtitle": "Hand-selected for excellence.", "sort_order": 1},
            {"title": "Exceptional Service", "subtitle": "Our team is here to help every step of the way.", "sort_order": 2},
        ]
        for data in slides_data:
            if not HeroSlide.objects.filter(title=data["title"]).exists():
                # We skip image since it's required — seed creates placeholder records
                pass
        self.stdout.write(self.style.SUCCESS("  HeroSlides: skipped (image required — add via admin)"))

        # ---------------------------------------------------------------
        # Categories
        # ---------------------------------------------------------------
        from apps.catalog.models import Category
        cat_names = ["Products", "Services", "Accessories"]
        cats = []
        for name in cat_names:
            cat, _ = Category.objects.get_or_create(
                name=name,
                defaults={"slug": slugify(name), "is_active": True},
            )
            cats.append(cat)
        self.stdout.write(self.style.SUCCESS(f"  {len(cats)} Categories created"))

        # ---------------------------------------------------------------
        # Brands
        # ---------------------------------------------------------------
        from apps.catalog.models import Brand
        brand_names = ["Acme Brand", "Premium Line"]
        brands = []
        for name in brand_names:
            brand, _ = Brand.objects.get_or_create(
                name=name,
                defaults={"slug": slugify(name), "is_active": True},
            )
            brands.append(brand)
        self.stdout.write(self.style.SUCCESS(f"  {len(brands)} Brands created"))

        # ---------------------------------------------------------------
        # Items
        # ---------------------------------------------------------------
        from apps.catalog.models import Item
        items_data = [
            {"title": "Deluxe Widget", "brand": brands[0], "category": cats[0], "condition": "new", "price": "199.99", "short_description": "Our best-selling widget for everyday use."},
            {"title": "Premium Gadget", "brand": brands[1], "category": cats[0], "condition": "new", "price": "349.00", "short_description": "Top-of-the-line performance in a sleek package."},
            {"title": "Classic Accessory", "brand": brands[0], "category": cats[2], "condition": "new", "price": "49.99", "short_description": "A timeless accessory to complement any purchase."},
            {"title": "Pre-Owned Special", "brand": brands[1], "category": cats[0], "condition": "used", "price": "149.00", "short_description": "Professionally inspected and certified pre-owned."},
            {"title": "Starter Package", "brand": brands[0], "category": cats[0], "condition": "new", "price": "99.00", "short_description": "Everything you need to get started."},
        ]
        for data in items_data:
            if not Item.objects.filter(title=data["title"]).exists():
                Item.objects.create(
                    title=data["title"],
                    brand=data["brand"],
                    category=data["category"],
                    condition=data["condition"],
                    price=data["price"],
                    short_description=data["short_description"],
                    description=f"Full description for {data['title']}. This is sample content that should be replaced with real product information.",
                    is_active=True,
                )
        self.stdout.write(self.style.SUCCESS("  5 Items created"))

        # ---------------------------------------------------------------
        # BlogPosts
        # ---------------------------------------------------------------
        from apps.blog.models import BlogPost, BlogCategory
        from apps.accounts.models import User
        blog_cat, _ = BlogCategory.objects.get_or_create(
            name="News",
            defaults={"slug": "news", "is_active": True},
        )
        admin_user = User.objects.filter(is_superuser=True).first()
        posts_data = [
            {
                "title": "Welcome to Our Blog",
                "excerpt": "An introduction to what you can expect from our team.",
                "body": "Welcome to the Acme Business blog! We will be sharing news, tips, and updates about our products and services. Stay tuned for regular updates.",
            },
            {
                "title": "5 Tips for Getting the Most Out of Your Purchase",
                "excerpt": "Make the most of your investment with these expert tips.",
                "body": "Getting the most value from your purchase is easy when you follow these five simple tips...\n\n1. Register your product for warranty coverage.\n2. Read the documentation.\n3. Contact our support team with any questions.\n4. Keep your receipt for returns.\n5. Leave us a review!",
            },
        ]
        for data in posts_data:
            if not BlogPost.objects.filter(title=data["title"]).exists():
                BlogPost.objects.create(
                    title=data["title"],
                    slug=slugify(data["title"]),
                    author=admin_user,
                    category=blog_cat,
                    excerpt=data["excerpt"],
                    body=data["body"],
                    is_published=True,
                    published_at=timezone.now(),
                )
        self.stdout.write(self.style.SUCCESS("  2 BlogPosts created"))

        # ---------------------------------------------------------------
        # Events
        # ---------------------------------------------------------------
        from apps.events.models import Event, EventCategory
        event_cat, _ = EventCategory.objects.get_or_create(
            name="Showcase",
            defaults={"slug": "showcase"},
        )
        import datetime
        events_data = [
            {
                "title": "Spring Product Showcase",
                "date": timezone.now().date() + datetime.timedelta(days=14),
                "location": "Main Showroom",
                "description": "Join us for our annual spring showcase featuring new arrivals and exclusive promotions.",
            },
            {
                "title": "Customer Appreciation Day",
                "date": timezone.now().date() + datetime.timedelta(days=30),
                "location": "Acme Business — Main Location",
                "description": "A day dedicated to our loyal customers. Refreshments, demos, and special discounts.",
            },
        ]
        for data in events_data:
            if not Event.objects.filter(title=data["title"]).exists():
                Event.objects.create(
                    title=data["title"],
                    slug=slugify(data["title"]),
                    category=event_cat,
                    date=data["date"],
                    location=data["location"],
                    description=data["description"],
                    is_active=True,
                )
        self.stdout.write(self.style.SUCCESS("  2 Events created"))

        # ---------------------------------------------------------------
        # TeamMembers
        # ---------------------------------------------------------------
        from apps.team.models import TeamMember, Department
        dept, _ = Department.objects.get_or_create(
            name="Leadership",
            defaults={"slug": "leadership"},
        )
        team_data = [
            {"name": "Jane Smith", "role": "Chief Executive Officer", "bio": "Jane has led Acme Business for over 15 years with a passion for quality and customer service."},
            {"name": "John Doe", "role": "Sales Manager", "bio": "John brings 10 years of industry experience and a commitment to finding the right solution for every customer."},
            {"name": "Emily Chen", "role": "Service Director", "bio": "Emily oversees all service operations and ensures every customer receives exceptional care."},
        ]
        for data in team_data:
            if not TeamMember.objects.filter(name=data["name"]).exists():
                TeamMember.objects.create(
                    name=data["name"],
                    role=data["role"],
                    department=dept,
                    bio=data["bio"],
                    is_active=True,
                )
        self.stdout.write(self.style.SUCCESS("  3 TeamMembers created"))

        # ---------------------------------------------------------------
        # Testimonials
        # ---------------------------------------------------------------
        from apps.testimonials.models import Testimonial
        testimonials_data = [
            {"author_name": "Michael R.", "author_title": "Verified Customer", "content": "Absolutely wonderful experience from start to finish. The team was knowledgeable and the product exceeded my expectations.", "rating": 5, "source": "Google"},
            {"author_name": "Sarah T.", "author_title": "Loyal Customer", "content": "I have been a customer for five years and the service only gets better. Highly recommend to anyone looking for quality.", "rating": 5, "source": "Yelp"},
        ]
        for data in testimonials_data:
            if not Testimonial.objects.filter(author_name=data["author_name"]).exists():
                Testimonial.objects.create(
                    author_name=data["author_name"],
                    author_title=data["author_title"],
                    content=data["content"],
                    rating=data["rating"],
                    source=data["source"],
                    is_featured=True,
                )
        self.stdout.write(self.style.SUCCESS("  2 Testimonials created"))

        # ---------------------------------------------------------------
        # Services
        # ---------------------------------------------------------------
        from apps.services.models import Service
        services_data = [
            {"name": "Consultation", "short_description": "Expert one-on-one consultation to find the perfect solution for your needs.", "price_display": "Free", "is_featured": True},
            {"name": "Installation & Setup", "short_description": "Professional installation and setup by our certified technicians.", "price_display": "From $99", "is_featured": True},
        ]
        for data in services_data:
            if not Service.objects.filter(name=data["name"]).exists():
                Service.objects.create(
                    name=data["name"],
                    slug=slugify(data["name"]),
                    short_description=data["short_description"],
                    description=f"Full description for {data['name']}. Our team of experts provides {data['name'].lower()} services tailored to your specific requirements.",
                    price_display=data["price_display"],
                    is_featured=data["is_featured"],
                    is_active=True,
                )
        self.stdout.write(self.style.SUCCESS("  2 Services created"))

        # ---------------------------------------------------------------
        # Promotion
        # ---------------------------------------------------------------
        from apps.promotions.models import Promotion, PromotionPage
        if not Promotion.objects.filter(title="Spring Sale").exists():
            promo = Promotion.objects.create(
                title="Spring Sale",
                slug="spring-sale",
                template="hero",
                is_active=True,
                is_featured_home=True,
            )
            PromotionPage.objects.create(
                promotion=promo,
                heading="Spring Into Savings",
                subheading="Up to 20% off select products this season.",
                body_text="Don't miss our biggest sale of the year. Browse our full catalog to find incredible deals on top products.",
                cta_label="Shop the Sale",
                cta_url="/catalog/",
            )
        self.stdout.write(self.style.SUCCESS("  1 Promotion created"))

        self.stdout.write(self.style.SUCCESS("\nDatabase seeded successfully!"))
        self.stdout.write("Note: Hero slides and brand logos require images — add them via the admin.")
