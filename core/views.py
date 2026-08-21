import time

from django.contrib import messages
from django.core.cache import cache
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .email_utils import send_enquiry_autoreply, send_enquiry_notification
from .forms import EnquiryForm
from .models import ClientLogo, GalleryImage, Service, ServiceCategory, TeamMember, TrustCard

RATE_LIMIT_SECONDS = 60  # minimum time between enquiry submissions per IP


def _client_ip(request):
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def _handle_enquiry_submission(request, source_page):
    """Shared enquiry-form handling used by both the Home and Contact pages."""
    form = EnquiryForm(request.POST)
    ip = _client_ip(request)

    cache_key = f"enquiry-throttle-{ip}"
    if cache.get(cache_key):
        messages.error(request, "You've already submitted an enquiry recently. Our team will be in touch shortly.")
        return form, False

    if form.is_valid():
        enquiry = form.save(commit=False)
        enquiry.source_page = source_page
        enquiry.ip_address = ip
        enquiry.save()

        cache.set(cache_key, True, RATE_LIMIT_SECONDS)

        send_enquiry_notification(enquiry)
        send_enquiry_autoreply(enquiry)

        messages.success(
            request,
            "Thank you! Your enquiry has been received. Our team will contact you shortly.",
        )
        return form, True

    messages.error(request, "Please correct the errors below and try again.")
    return form, False


@require_http_methods(["GET", "POST"])
def home(request):
    if request.method == "POST":
        form, success = _handle_enquiry_submission(request, source_page="home")
        if success:
            return redirect("core:home")
    else:
        form = EnquiryForm(initial={"form_rendered_at": time.time()})

    featured_services = Service.objects.filter(active=True).select_related("category")[:3]
    client_logos = ClientLogo.objects.filter(active=True, status="live")
    gallery_images = GalleryImage.objects.filter(active=True)[:12]
    trust_cards = TrustCard.objects.filter(active=True, page="home")

    context = {
        "featured_services": featured_services,
        "client_logos": client_logos,
        "gallery_images": gallery_images,
        "trust_cards": trust_cards,
        "form": form,
        "meta_title": "HY-FY Technology | Fire Alarm, CCTV & Security System Installers in Chennai",
        "meta_description": (
            "HY-FY Technology provides fire alarm, CCTV surveillance, access control and "
            "security system installation, repair, maintenance and AMC services across Chennai."
        ),
    }
    return render(request, "home.html", context)


def about(request):
    trust_cards = TrustCard.objects.filter(active=True, page="about")
    team_members = TeamMember.objects.filter(active=True)
    context = {
        "trust_cards": trust_cards,
        "team_members": team_members,
        "meta_title": "About Us | HY-FY Technology",
        "meta_description": "Learn about HY-FY Technology's experience, certified technicians and commitment to reliable fire safety and security solutions in Chennai.",
    }
    return render(request, "about.html", context)


def services(request):
    categories = ServiceCategory.objects.filter(active=True).prefetch_related("services")
    category_slug = request.GET.get("category")

    services_qs = Service.objects.filter(active=True).select_related("category").prefetch_related("brands")
    if category_slug and category_slug != "all":
        services_qs = services_qs.filter(category__slug=category_slug)

    context = {
        "categories": categories,
        "services_list": services_qs,
        "active_category": category_slug or "all",
        "meta_title": "Our Services | Fire Alarm, CCTV, Access Control - HY-FY Technology",
        "meta_description": "Explore HY-FY Technology's full range of fire alarm, CCTV, access control, public address, fire extinguisher and other safety systems.",
    }
    return render(request, "services.html", context)


def service_detail(request, slug):
    service = get_object_or_404(
        Service.objects.select_related("category").prefetch_related("brands"),
        slug=slug,
        active=True,
    )
    related_services = (
        Service.objects.filter(category=service.category, active=True).exclude(pk=service.pk)[:3]
    )
    context = {
        "service": service,
        "related_services": related_services,
        "meta_title": service.meta_title or f"{service.name} | HY-FY Technology",
        "meta_description": service.meta_description or service.short_description,
    }
    return render(request, "services/service_detail.html", context)


def clients(request):
    live_clients = ClientLogo.objects.filter(active=True, status="live")
    previous_clients = ClientLogo.objects.filter(active=True, status="previous")
    context = {
        "live_clients": live_clients,
        "previous_clients": previous_clients,
        "meta_title": "Our Clients | HY-FY Technology",
        "meta_description": "See the hospitals, schools, offices, industries and institutions that trust HY-FY Technology for fire safety and security systems.",
    }
    return render(request, "clients.html", context)


@require_http_methods(["GET", "POST"])
def contact(request):
    if request.method == "POST":
        form, success = _handle_enquiry_submission(request, source_page="contact")
        if success:
            return redirect("core:contact")
    else:
        form = EnquiryForm(initial={"form_rendered_at": time.time()})

    context = {
        "form": form,
        "meta_title": "Contact Us | HY-FY Technology",
        "meta_description": "Get in touch with HY-FY Technology for fire alarm, CCTV, access control and security system enquiries in Chennai.",
    }
    return render(request, "contact.html", context)


def error_404(request, exception=None):
    return render(request, "404.html", status=404)


def error_500(request):
    return render(request, "500.html", status=500)
