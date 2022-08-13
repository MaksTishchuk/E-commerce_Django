from django.contrib import admin
from django.utils.safestring import mark_safe

from custom_admin.models import AdminUser


@admin.register(AdminUser)
class AdminUserAdmin(admin.ModelAdmin):
    """ Admin User in admin panel """

    list_display = ("id", "user", "full_name", "phone", "joined_in", "get_image")
    list_display_links = ("id", "user", "full_name")
    save_as = True
    fields = (
        "user",
        "full_name",
        "phone",
        "joined_in",
        "image",
        "get_image"
    )
    readonly_fields = ("joined_in", "get_image")

    def get_image(self, obj):
        """ View photo in admin panel """

        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100">')
        else:
            return f'Image not set'

    get_image.short_description = 'Image'
