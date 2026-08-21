from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from core.models import Service


class StaticViewSitemap(Sitemap):
    """Static, always-present pages."""

    changefreq = "weekly"
    protocol = "https"

    def priority(self, item):
        return {
            "core:home": 1.0,
            "core:services": 0.9,
            "core:about": 0.7,
            "core:clients": 0.6,
            "core:contact": 0.8,
        }.get(item, 0.5)

    def items(self):
        return [
            "core:home",
            "core:services",
            "core:about",
            "core:clients",
            "core:contact",
        ]

    def location(self, item):
        return reverse(item)


class ServiceSitemap(Sitemap):
    """One entry per published service (e.g. /services/fire-alarm-systems/)."""

    changefreq = "monthly"
    priority = 0.8
    protocol = "https"

    def items(self):
        return Service.objects.filter(active=True).select_related("category")

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse("core:service_detail", args=[obj.slug])
