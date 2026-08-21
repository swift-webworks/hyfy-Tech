from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("about-us/", views.about, name="about"),
    path("services/", views.services, name="services"),
    path("services/<slug:slug>/", views.service_detail, name="service_detail"),
    path("our-clients/", views.clients, name="clients"),
    path("contact-us/", views.contact, name="contact"),
]
