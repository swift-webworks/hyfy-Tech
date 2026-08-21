from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from core.models import Brand, Service, ServiceCategory, TrustCard

# A minimal 1x1 transparent PNG used as a placeholder image for seeded records.
PLACEHOLDER_PNG = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
    b"\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01"
    b"\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
)

SERVICE_DATA = {
    "Fire Alarm Systems": [
        ("Addressable Fire Alarm Panel", ["EST3", "Ravel", "Morley", "Notifier", "Apollo"]),
        ("Conventional Fire Alarm Panel", ["Ravel"]),
    ],
    "CCTV Systems": [
        ("IP-Based Camera", ["Hikvision", "Dahua", "CP Plus"]),
        ("PTZ Camera", ["Honeywell", "Hikvision"]),
    ],
    "Access Control Systems": [
        ("Fingerprint Reader", ["ZKTeco", "ESSL"]),
        ("Card Reader", ["HID Card Reader", "Spectra"]),
    ],
    "Public Address Systems": [("PA Instruction Panel", ["Bosch", "Ahuja"])],
    "Fire Extinguishers": [("ABC Fire Extinguisher", ["Kiranex", "Safex"])],
    "WLD & Rodent": [("Water Leakage Detection", ["Csystems"])],
    "Intrusion Systems": [("Intrusion Detection System", ["Bosch", "Godrej"])],
    "VESDA": [("VESDA Smoke Detection", ["XTrails"])],
}

TRUST_CARDS = [
    ("TRUST", "100% Trusted Across Chennai", "Verify before publishing.", "home"),
    ("SAFE", "Safe Testing & Implementation", "Verify before publishing.", "home"),
    ("EXPERIENCE", "Years of Experience", "Confirm exact figure with client.", "about"),
    ("CLIENTS", "Satisfied Clients", "Confirm exact figure with client.", "about"),
]


class Command(BaseCommand):
    help = "Seed demo/placeholder content so the site is browsable before real content is added."

    def handle(self, *args, **options):
        for order, (category_name, services) in enumerate(SERVICE_DATA.items()):
            category, _ = ServiceCategory.objects.get_or_create(
                name=category_name, defaults={"display_order": order}
            )
            for s_order, (service_name, brand_names) in enumerate(services):
                if Service.objects.filter(name=service_name).exists():
                    continue
                service = Service(
                    category=category,
                    name=service_name,
                    short_description=f"Professional {service_name.lower()} installation, repair and maintenance.",
                    display_order=s_order,
                )
                service.image.save(f"{service_name}.png", ContentFile(PLACEHOLDER_PNG), save=False)
                service.save()
                for brand_name in brand_names:
                    brand, _ = Brand.objects.get_or_create(name=brand_name)
                    service.brands.add(brand)

        for closed_label, headline, detail, page in TRUST_CARDS:
            TrustCard.objects.get_or_create(
                headline=headline, defaults={"closed_label": closed_label, "detail": detail, "page": page}
            )

        self.stdout.write(self.style.SUCCESS("Demo data seeded. Add real images/logos via Django Admin."))
