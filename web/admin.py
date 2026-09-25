from django.contrib import admin

from .models import Navbar, SubMenu, Banner, WebsiteSection


admin.site.register(Navbar)
admin.site.register(SubMenu)
admin.site.register(Banner)


@admin.register(WebsiteSection)
class WebsiteSectionAdmin(admin.ModelAdmin):

    list_display = (
        "heading",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "heading",
        "paragraph",
    )