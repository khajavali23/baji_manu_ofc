
from django.contrib import admin

from .models import (
    Navbar,
    SubMenu,
    Banner,
    WebsiteSection,
    SubMenuContent,
    NavbarContent,
    NavbarDocument,
    SubMenuDocument,
    BannerButton,
)

class BannerButtonInline(admin.TabularInline):

    model = BannerButton

    extra = 1

    ordering = ("order",)



# =========================================================
# NAVBAR
# =========================================================

@admin.register(Navbar)
class NavbarAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "url",
    )

    search_fields = (
        "name",
        "url",
    )


# =========================================================
# SUBMENU
# =========================================================

@admin.register(SubMenu)
class SubMenuAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "navbar",
    )

    search_fields = (
        "name",
        "navbar__name",
    )


# =========================================================
# BANNER
# =========================================================


# =========================================================
# BANNER BUTTON INLINE
# =========================================================

class BannerButtonInline(admin.TabularInline):

    model = BannerButton

    extra = 1

    ordering = ("order",)


# =========================================================
# BANNER
# =========================================================

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):

    list_display = (
        "title",
    )

    search_fields = (
        "title",
        "description",
    )

    inlines = [
        BannerButtonInline,
    ]

    list_display = (
        "title",
    )

    search_fields = (
        "title",
        "description",
    )

    inlines = [
        BannerButtonInline,
    ]

    fieldsets = (
        (
            "Banner Details",
            {
                "fields": (
                    "title",
                    "image",
                    "description",
                )
            }
        ),
    )
# =========================================================
# WEBSITE SECTION
# =========================================================

@admin.register(WebsiteSection)
class WebsiteSectionAdmin(admin.ModelAdmin):

    list_display = (
        "heading",
        "link",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "heading",
        "paragraph",
        "link",
    )


# =========================================================
# SUBMENU CONTENT
# =========================================================

@admin.register(SubMenuContent)
class SubMenuContentAdmin(admin.ModelAdmin):

    list_display = (
        "submenu",
        "heading",
    )

    search_fields = (
        "heading",
        "paragraph",
        "submenu__name",
    )


# =========================================================
# SUBMENU DOCUMENT
# =========================================================

@admin.register(SubMenuDocument)
class SubMenuDocumentAdmin(admin.ModelAdmin):

    list_display = (
        "submenu_content",
        "document_name",
        "document",
    )

    search_fields = (
        "document_name",
        "submenu_content__submenu__name",
    )


# =========================================================
# NAVBAR CONTENT
# =========================================================

@admin.register(NavbarContent)
class NavbarContentAdmin(admin.ModelAdmin):

    list_display = (
        "navbar",
        "heading",
    )

    search_fields = (
        "heading",
        "paragraph",
        "navbar__name",
    )


# =========================================================
# NAVBAR DOCUMENT
# =========================================================

@admin.register(NavbarDocument)
class NavbarDocumentAdmin(admin.ModelAdmin):

    list_display = (
        "navbar_content",
        "document_name",
        "document",
    )

    search_fields = (
        "document_name",
        "navbar_content__navbar__name",
    )

