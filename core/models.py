from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

IMAGE_VALIDATORS = [FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "webp"])]


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class OrderedActiveModel(TimeStampedModel):
    display_order = models.PositiveIntegerField(default=0, help_text="Lower numbers show first.")
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ["display_order", "-created_at"]


# ---------------------------------------------------------------------------
# Services
# ---------------------------------------------------------------------------
class ServiceCategory(OrderedActiveModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=110, unique=True, blank=True)
    icon_css_class = models.CharField(
        max_length=60, blank=True, help_text="Optional icon class, e.g. 'bi-fire' (Bootstrap Icons)."
    )

    class Meta(OrderedActiveModel.Meta):
        verbose_name_plural = "Service categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    logo = models.ImageField(upload_to="brands/", blank=True, null=True, validators=IMAGE_VALIDATORS)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Service(OrderedActiveModel):
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name="services")
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True, blank=True)
    short_description = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="services/", validators=IMAGE_VALIDATORS)
    brands = models.ManyToManyField(Brand, blank=True, related_name="services")

    # SEO
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)

    class Meta(OrderedActiveModel.Meta):
        verbose_name_plural = "Services"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("core:service_detail", args=[self.slug])


# ---------------------------------------------------------------------------
# Clients
# ---------------------------------------------------------------------------
class ClientLogo(OrderedActiveModel):
    STATUS_CHOICES = [("live", "Live Client"), ("previous", "Previous Client")]

    client_name = models.CharField(max_length=150)
    logo = models.ImageField(upload_to="clients/", validators=IMAGE_VALIDATORS)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="live")

    class Meta(OrderedActiveModel.Meta):
        verbose_name_plural = "Client logos"

    def __str__(self):
        return f"{self.client_name} ({self.get_status_display()})"


# ---------------------------------------------------------------------------
# Gallery
# ---------------------------------------------------------------------------
class GalleryImage(OrderedActiveModel):
    image = models.ImageField(upload_to="gallery/", validators=IMAGE_VALIDATORS)
    caption = models.CharField(max_length=50, help_text="Maximum 50 characters.")
    category = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.caption


# ---------------------------------------------------------------------------
# Team
# ---------------------------------------------------------------------------
class TeamMember(OrderedActiveModel):
    image = models.ImageField(upload_to="team/", validators=IMAGE_VALIDATORS)
    name = models.CharField(max_length=100, blank=True)
    role = models.CharField(max_length=100, blank=True)
    caption = models.CharField(max_length=50, blank=True, help_text="Maximum 50 characters.")

    def __str__(self):
        return self.name or self.caption or f"Team member #{self.pk}"


# ---------------------------------------------------------------------------
# Trust cards (interactive "reveal" cards used on Home & About)
# ---------------------------------------------------------------------------
class TrustCard(OrderedActiveModel):
    PAGE_CHOICES = [("home", "Home Page"), ("about", "About Page")]

    page = models.CharField(max_length=10, choices=PAGE_CHOICES, default="home")
    closed_label = models.CharField(max_length=60, help_text="Text shown before the card is opened, e.g. 'TRUST'.")
    headline = models.CharField(max_length=100, help_text="Revealed headline, e.g. '12+ Years of Experience'.")
    detail = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.headline


# ---------------------------------------------------------------------------
# Enquiries (contact / quote requests)
# ---------------------------------------------------------------------------
class Enquiry(TimeStampedModel):
    STATUS_CHOICES = [
        ("new", "New"),
        ("contacted", "Contacted"),
        ("quoted", "Quoted"),
        ("won", "Won"),
        ("closed", "Closed"),
    ]

    SERVICE_CHOICES = [
        ("fire_alarm", "Fire Alarm System"),
        ("cctv", "CCTV System"),
        ("access_control", "Access Control System"),
        ("pa_system", "Public Address System"),
        ("fire_extinguisher", "Fire Extinguisher"),
        ("wld_rodent", "WLD & Rodent"),
        ("intrusion", "Intrusion System"),
        ("vesda", "VESDA"),
        ("other", "Other"),
    ]

    coordinator_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)

    required_date = models.DateField(blank=True, null=True)
    facility_type = models.CharField(max_length=100, blank=True)
    service_required = models.CharField(max_length=30, choices=SERVICE_CHOICES)
    brand = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=150, blank=True)

    message = models.TextField(blank=True)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="new")

    # Anti-abuse metadata (not shown in public forms)
    source_page = models.CharField(max_length=100, blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Enquiries"

    def __str__(self):
        return f"{self.coordinator_name} - {self.get_service_required_display()}"
