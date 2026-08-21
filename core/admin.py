from django.contrib import admin

from .models import (
    Brand,
    ClientLogo,
    Enquiry,
    GalleryImage,
    Service,
    ServiceCategory,
    TeamMember,
    TrustCard,
)

admin.site.site_header = "HY-FY Technology Admin"
admin.site.site_title = "HY-FY Admin"
admin.site.index_title = "Website Content Management"


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "display_order", "active")
    list_editable = ("display_order", "active")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "display_order", "active", "updated_at")
    list_editable = ("display_order", "active")
    list_filter = ("category", "active")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "short_description")
    filter_horizontal = ("brands",)
    fieldsets = (
        (None, {"fields": ("category", "name", "slug", "image", "short_description", "description", "brands")}),
        ("SEO", {"fields": ("meta_title", "meta_description")}),
        ("Display", {"fields": ("display_order", "active")}),
    )


@admin.register(ClientLogo)
class ClientLogoAdmin(admin.ModelAdmin):
    list_display = ("client_name", "status", "display_order", "active")
    list_editable = ("display_order", "active")
    list_filter = ("status", "active")
    search_fields = ("client_name",)


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ("caption", "category", "display_order", "active")
    list_editable = ("display_order", "active")
    list_filter = ("category", "active")


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "caption", "display_order", "active")
    list_editable = ("display_order", "active")


@admin.register(TrustCard)
class TrustCardAdmin(admin.ModelAdmin):
    list_display = ("headline", "page", "closed_label", "display_order", "active")
    list_editable = ("display_order", "active")
    list_filter = ("page", "active")


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = (
        "coordinator_name",
        "phone_number",
        "email",
        "service_required",
        "location",
        "status",
        "created_at",
    )
    list_editable = ("status",)
    list_filter = ("status", "service_required", "created_at")
    search_fields = ("coordinator_name", "email", "phone_number", "location")
    readonly_fields = ("source_page", "ip_address", "created_at", "updated_at")
    date_hierarchy = "created_at"
