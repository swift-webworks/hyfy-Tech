from django.conf import settings

from core.models import ServiceCategory


def site_settings(request):
    return {
        "SITE_NAME": settings.SITE_NAME,
        "SITE_URL": settings.SITE_URL,
        "COMPANY_PHONE": settings.COMPANY_PHONE,
        "COMPANY_PHONE_2": settings.COMPANY_PHONE_2,
        "COMPANY_EMAIL": settings.COMPANY_EMAIL,
        "COMPANY_ADDRESS": settings.COMPANY_ADDRESS,
        "WHATSAPP_NUMBER": settings.WHATSAPP_NUMBER,
        "WHATSAPP_NUMBER_2": settings.WHATSAPP_NUMBER_2,
        "GOOGLE_MAPS_EMBED_URL": settings.GOOGLE_MAPS_EMBED_URL,
        "GOOGLE_ANALYTICS_ID": settings.GOOGLE_ANALYTICS_ID,
        "nav_categories": ServiceCategory.objects.filter(active=True).order_by("display_order"),
    }