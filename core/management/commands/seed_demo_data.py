from datetime import date
from django.core.management.base import BaseCommand
from core.models import Service, Testimonial, CompanyStat


class Command(BaseCommand):
    """
    Populates the database with starter content (services, stats, testimonials)
    so the site isn't empty on first run.

    Usage:
        python manage.py seed_demo_data

    Note: Portfolio photos are NOT seeded here since they require real image
    files — add those from /admin/ (Portfolio Items) with your own project photos.
    """
    help = "Seed the database with sample Services, CompanyStats, and Testimonials."

    def handle(self, *args, **options):
        services_data = [
            {
                "title": "Full Interior Design & Execution",
                "short_description": "Complete interior planning, design, and execution for homes and offices.",
                "description": "From concept to handover, we manage the full interior journey — space planning, "
                                "material selection, false ceilings, modular furniture, and finishing — delivered "
                                "by one accountable team.",
                "icon_class": "bi-house-heart-fill",
                "order": 1,
            },
            {
                "title": "Exterior Facade & Elevation Work",
                "short_description": "Modern facade design and elevation work that boosts curb appeal.",
                "description": "We design and execute exterior elevations, cladding, texture finishes, and facade "
                                "lighting to give your property a striking, durable exterior.",
                "icon_class": "bi-building",
                "order": 2,
            },
            {
                "title": "Carpentry & Custom Furniture",
                "short_description": "Custom-built wardrobes, kitchens, and furniture crafted to fit your space.",
                "description": "Our in-house carpentry team builds modular kitchens, wardrobes, TV units, and "
                                "bespoke furniture using quality ply and hardware, measured and fitted precisely.",
                "icon_class": "bi-hammer",
                "order": 3,
            },
            {
                "title": "Painting & Wall Finishing",
                "short_description": "Interior and exterior painting with premium, weatherproof finishes.",
                "description": "From smooth putty finishing to texture and weatherproof exterior coats, our "
                                "painting team delivers a clean, long-lasting finish on every wall.",
                "icon_class": "bi-brush-fill",
                "order": 4,
            },
            {
                "title": "Decorative Lighting & Electricals",
                "short_description": "False ceiling lighting, accent lighting, and safe electrical wiring.",
                "description": "We plan and install decorative and functional lighting layouts along with safe, "
                                "code-compliant electrical wiring for every room.",
                "icon_class": "bi-lightbulb-fill",
                "order": 5,
            },
            {
                "title": "Flooring & Tile Fitting",
                "short_description": "Precision tile and flooring installation for every room and facade.",
                "description": "Vitrified tiles, marble, wooden flooring, and bathroom/kitchen tiling — fitted "
                                "with precise leveling and finishing by experienced tile masons.",
                "icon_class": "bi-grid-3x3-gap-fill",
                "order": 6,
            },
        ]

        for data in services_data:
            obj, created = Service.objects.get_or_create(title=data["title"], defaults=data)
            self.stdout.write(self.style.SUCCESS(f"{'Created' if created else 'Exists'}: {obj.title}"))

        stats_data = [
            {"label": "Years of Experience", "value": "20+", "icon_class": "bi-award-fill", "order": 1},
            {"label": "Projects Completed", "value": "100+", "icon_class": "bi-building-fill-check", "order": 2},
            {"label": "Happy Clients", "value": "100+", "icon_class": "bi-emoji-smile-fill", "order": 3},
            {"label": "Largest Deal Value", "value": "₹30L+", "icon_class": "bi-cash-coin", "order": 4},
        ]
        for data in stats_data:
            obj, created = CompanyStat.objects.get_or_create(label=data["label"], defaults=data)
            self.stdout.write(self.style.SUCCESS(f"{'Created' if created else 'Exists'}: {obj.label}"))

        testimonials_data = [
            {
                "client_name": "Rohit Sharma",
                "project_type": "3BHK Full Interior",
                "review": "The team handled everything from carpentry to painting without any delays. "
                           "Very professional and the finish quality was excellent.",
                "rating": 5,
            },
            {
                "client_name": "Anita Verma",
                "project_type": "Villa Exterior Facade",
                "review": "Our villa's exterior looks completely transformed. Great attention to detail "
                           "and they stuck to the budget we agreed on.",
                "rating": 5,
            },
            {
                "client_name": "Manoj Tiwari",
                "project_type": "Modular Kitchen & Carpentry",
                "review": "Excellent carpentry work — the modular kitchen fits perfectly and looks premium. "
                           "Highly recommended for anyone looking for a single trusted contractor.",
                "rating": 4,
            },
        ]
        for data in testimonials_data:
            obj, created = Testimonial.objects.get_or_create(
                client_name=data["client_name"], project_type=data["project_type"], defaults=data
            )
            self.stdout.write(self.style.SUCCESS(f"{'Created' if created else 'Exists'}: {obj.client_name}"))

        self.stdout.write(self.style.SUCCESS("\nDemo data seeding complete!"))
        self.stdout.write("Add Portfolio Items with real photos from /admin/ to complete the gallery.")
