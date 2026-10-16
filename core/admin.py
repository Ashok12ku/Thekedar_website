from django.contrib import admin
from django.utils.html import format_html
from .models import Service, PortfolioItem, Testimonial, Inquiry, CompanyStat


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "short_description", "is_featured", "order", "thumb")
    list_editable = ("is_featured", "order")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "short_description")
    list_filter = ("is_featured",)

    def thumb(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:40px;border-radius:4px;" />', obj.image.url)
        return "-"
    thumb.short_description = "Image"


@admin.register(PortfolioItem)
class PortfolioItemAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "location", "date", "is_featured", "thumb")
    list_filter = ("category", "is_featured", "date")
    search_fields = ("title", "location", "description")
    list_editable = ("is_featured",)
    date_hierarchy = "date"

    def thumb(self, obj):
        if obj.main_image:
            return format_html('<img src="{}" style="height:40px;border-radius:4px;" />', obj.main_image.url)
        return "-"
    thumb.short_description = "Image"


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("client_name", "project_type", "rating", "is_published", "created_at")
    list_filter = ("rating", "is_published")
    search_fields = ("client_name", "project_type", "review")
    list_editable = ("is_published",)


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    """
    This is the most important admin screen for day-to-day business —
    it's where every lead from the website lands.
    """
    list_display = (
        "name", "phone", "service_selected", "budget_range",
        "location", "status", "created_at",
    )
    list_filter = ("status", "service_selected", "budget_range", "created_at")
    search_fields = ("name", "phone", "email", "location", "message")
    list_editable = ("status",)
    readonly_fields = ("created_at",)
    date_hierarchy = "created_at"
    ordering = ("-created_at",)

    fieldsets = (
        ("Client Details", {
            "fields": ("name", "phone", "email", "location")
        }),
        ("Requirement", {
            "fields": ("service_selected", "budget_range", "message")
        }),
        ("Lead Tracking (internal)", {
            "fields": ("status", "internal_notes", "created_at")
        }),
    )

    actions = ["mark_contacted", "mark_won", "mark_lost"]

    @admin.action(description="Mark selected inquiries as Contacted")
    def mark_contacted(self, request, queryset):
        queryset.update(status="contacted")

    @admin.action(description="Mark selected inquiries as Deal Won")
    def mark_won(self, request, queryset):
        queryset.update(status="won")

    @admin.action(description="Mark selected inquiries as Lost")
    def mark_lost(self, request, queryset):
        queryset.update(status="lost")


@admin.register(CompanyStat)
class CompanyStatAdmin(admin.ModelAdmin):
    list_display = ("label", "value", "order")
    list_editable = ("value", "order")


# Optional: customise admin site header/title for a nicer branded feel
admin.site.site_header = "Thekedar Interiors & Exteriors — Admin"
admin.site.site_title = "Thekedar Admin"
admin.site.index_title = "Manage Website Content & Leads"
