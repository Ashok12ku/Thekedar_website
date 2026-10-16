from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("services/", views.services_list, name="services"),
    path("services/<slug:slug>/", views.service_detail, name="service_detail"),
    path("portfolio/", views.portfolio, name="portfolio"),
    path("contact/", views.contact, name="contact"),
]
