from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic import TemplateView

from .sitemaps import ServiceSitemap, StaticViewSitemap

sitemaps = {
    "static": StaticViewSitemap,
    "services": ServiceSitemap,
}

urlpatterns = [
    # Admin URL is configurable via env (DJANGO_ADMIN_URL) so it is not
    # left guessable at the default /admin/ in production.
    path(settings.DJANGO_ADMIN_URL, admin.site.urls),

    path("", include("core.urls")),

    # SEO
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
        name="robots_txt",
    ),
]

# Custom error handlers
handler404 = "core.views.error_404"
handler500 = "core.views.error_500"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
