from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator


class Service(models.Model):
    """
    A service offered by the contractor, e.g. Carpentry, Painting,
    Full Interior Design & Execution, etc.
    Shown on the Home page (highlights) and the Services page (full list).
    """
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True, blank=True,
                             help_text="Auto-generated from title if left blank.")
    short_description = models.CharField(
        max_length=250,
        help_text="Short one-liner shown on service cards / home page highlights."
    )
    description = models.TextField(
        help_text="Full description shown on the service detail / services page."
    )
    # Bootstrap Icons class name, e.g. 'bi-house-door', 'bi-brush', 'bi-lightbulb'
    icon_class = models.CharField(
        max_length=60, blank=True,
        help_text="Bootstrap Icons class, e.g. 'bi-house-door-fill' (see icons.getbootstrap.com)"
    )
    image = models.ImageField(upload_to="services/", blank=True, null=True)
    is_featured = models.BooleanField(
        default=True, help_text="Show this service in the Home page highlights section."
    )
    order = models.PositiveIntegerField(
        default=0, help_text="Lower numbers appear first."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "title"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("core:service_detail", kwargs={"slug": self.slug})


class PortfolioItem(models.Model):
    """
    A completed project photo/entry for the Portfolio / Gallery page.
    Supports categorisation and optional before/after comparison images.
    """
    CATEGORY_CHOICES = [
        ("interior", "Interior"),
        ("exterior", "Exterior"),
        ("carpentry", "Carpentry"),
        ("painting", "Painting"),
        ("lighting", "Lighting & Electricals"),
        ("tiles", "Flooring & Tiles"),
        ("turnkey", "Turnkey Project"),
        ("before_after", "Before / After"),
    ]

    title = models.CharField(max_length=150)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, db_index=True)
    main_image = models.ImageField(upload_to="portfolio/")
    before_image = models.ImageField(
        upload_to="portfolio/before/", blank=True, null=True,
        help_text="Optional — only used for Before/After style listings."
    )
    after_image = models.ImageField(
        upload_to="portfolio/after/", blank=True, null=True
    )
    description = models.TextField(blank=True)
    location = models.CharField(max_length=150, blank=True, help_text="City / Area of the project")
    client_budget_range = models.CharField(max_length=100, blank=True)
    is_featured = models.BooleanField(default=False, help_text="Show on Home page highlights.")
    date = models.DateField(help_text="Date the project was completed.")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"


class Testimonial(models.Model):
    """Client review shown on the Home page testimonial carousel."""
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    client_name = models.CharField(max_length=120)
    client_photo = models.ImageField(upload_to="testimonials/", blank=True, null=True)
    project_type = models.CharField(
        max_length=150, help_text="e.g. '3BHK Full Interior', 'Villa Exterior Facade'"
    )
    review = models.TextField()
    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES, default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.client_name} - {self.rating}★"

    def stars_range(self):
        """Helper for templates: returns range(rating) to loop over filled stars."""
        return range(self.rating)

    def empty_stars_range(self):
        return range(5 - self.rating)


class Inquiry(models.Model):
    """
    A lead / quote request captured from the Contact page or the
    Home page quick lead form. This is the model your sales/ops team
    will use every day from the Django admin.
    """
    SERVICE_CHOICES = [
        ("full_interior", "Full Interior Design & Execution"),
        ("exterior_facade", "Exterior Facade & Elevation Work"),
        ("carpentry", "Carpentry & Custom Furniture"),
        ("painting", "Painting & Wall Finishing"),
        ("lighting", "Decorative Lighting & Electricals"),
        ("flooring_tiles", "Flooring & Tile Fitting"),
        ("turnkey", "Complete Turnkey Project"),
        ("other", "Other / Not Sure Yet"),
    ]

    BUDGET_CHOICES = [
        ("under_1L", "Under ₹1 Lakh"),
        ("1L_5L", "₹1 Lakh - ₹5 Lakh"),
        ("5L_15L", "₹5 Lakh - ₹15 Lakh"),
        ("15L_30L", "₹15 Lakh - ₹30 Lakh"),
        ("30L_plus", "₹30 Lakh+"),
        ("not_sure", "Not decided yet"),
    ]

    STATUS_CHOICES = [
        ("new", "New"),
        ("contacted", "Contacted"),
        ("site_visit", "Site Visit Scheduled"),
        ("quoted", "Quotation Sent"),
        ("won", "Deal Won"),
        ("lost", "Lost / Not Interested"),
    ]

    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    location = models.CharField(max_length=150, help_text="City / Area of the project site")
    service_selected = models.CharField(max_length=30, choices=SERVICE_CHOICES)
    budget_range = models.CharField(max_length=20, choices=BUDGET_CHOICES, blank=True)
    message = models.TextField(blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new", db_index=True)
    internal_notes = models.TextField(
        blank=True, help_text="Internal follow-up notes (not visible to client)."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Inquiries"

    def __str__(self):
        return f"{self.name} - {self.get_service_selected_display()} ({self.created_at:%d %b %Y})"


class CompanyStat(models.Model):
    """
    Editable numbers for the Home page counter section
    (e.g. 20+ Years Experience, 100+ Projects, 30 Lakh+ Deal Value).
    Kept as a model so you can update figures from the admin, no code changes needed.
    """
    label = models.CharField(max_length=100, help_text="e.g. 'Years of Experience'")
    value = models.CharField(max_length=30, help_text="e.g. '20+', '100+', '₹30L+'")
    icon_class = models.CharField(max_length=60, blank=True, help_text="Bootstrap Icons class")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.value} {self.label}"
