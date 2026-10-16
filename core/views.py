from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods

from .models import Service, PortfolioItem, Testimonial, CompanyStat
from .forms import InquiryForm


def home(request):
    """Home page: hero, service highlights, counters, testimonials, quick lead form."""
    if request.method == "POST":
        form = InquiryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Thank you! Your request has been received. Our team will call you shortly."
            )
            return redirect("core:home")
        else:
            messages.error(request, "Please correct the errors below and try again.")
    else:
        form = InquiryForm()

    context = {
        "services": Service.objects.filter(is_featured=True)[:6],
        "featured_portfolio": PortfolioItem.objects.filter(is_featured=True)[:6],
        "testimonials": Testimonial.objects.filter(is_published=True)[:6],
        "stats": CompanyStat.objects.all(),
        "form": form,
    }
    return render(request, "core/home.html", context)


def about(request):
    """About Us page: experience, process, quality commitment."""
    context = {
        "stats": CompanyStat.objects.all(),
    }
    return render(request, "core/about.html", context)


def services_list(request):
    """Full Services page — all services as cards."""
    context = {
        "services": Service.objects.all(),
    }
    return render(request, "core/services.html", context)


def service_detail(request, slug):
    """Individual service detail page."""
    service = get_object_or_404(Service, slug=slug)
    context = {
        "service": service,
        "other_services": Service.objects.exclude(slug=slug)[:4],
    }
    return render(request, "core/service_detail.html", context)


def portfolio(request):
    """Portfolio / Gallery page with category filtering."""
    category = request.GET.get("category", "all")
    items = PortfolioItem.objects.all()

    if category != "all":
        items = items.filter(category=category)

    paginator = Paginator(items, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "categories": PortfolioItem.CATEGORY_CHOICES,
        "selected_category": category,
    }
    return render(request, "core/portfolio.html", context)


@require_http_methods(["GET", "POST"])
def contact(request):
    """Contact / Get Quote page with full inquiry form."""
    if request.method == "POST":
        form = InquiryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Thank you! Your quote request has been submitted. "
                "Our team will contact you within 24 hours."
            )
            return redirect("core:contact")
        else:
            messages.error(request, "Please correct the errors below and try again.")
    else:
        # Allow pre-filling the service dropdown via ?service=carpentry links
        initial = {}
        preselect_service = request.GET.get("service")
        if preselect_service:
            initial["service_selected"] = preselect_service
        form = InquiryForm(initial=initial)

    context = {"form": form}
    return render(request, "core/contact.html", context)
