from django.contrib import admin
from django.utils.safestring import mark_safe
from modeltranslation.admin import TranslationAdmin

from .models import Category, Product, ProductImage


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    """ Category in admin panel """

    prepopulated_fields = {'slug': ('title',)}
    list_display = ("id", "title", "slug", "get_image")
    list_display_links = ("id", "title")
    save_as = True
    fields = ("title", "slug", "image", "get_image")
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        """ View photo in admin panel """

        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100">')
        else:
            return f'Image not set'

    get_image.short_description = 'Image'


@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    """ Product in admin panel """

    prepopulated_fields = {'slug': ('title',)}
    list_display = (
        "id", "title", "category", "market_price", "selling_price", "quantity", "view_count",
        "get_image"
    )
    list_display_links = ("id", "title",)
    list_filter = ('category',)
    search_fields = ('title', 'description',)
    fields = (
        "category", "title", "slug", "description", "market_price", "selling_price", "quantity",
        "created_at", "warranty", "return_policy", "view_count", "image", "get_image",
    )
    readonly_fields = ('get_image', "created_at",)
    save_as = True
    save_on_top = True

    def get_image(self, obj):
        """ View photo in admin panel """

        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100">')
        else:
            return f'Image not set'

    get_image.short_description = 'Image'


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    """ Product Image in admin panel """

    list_display = ("id", "product", "get_image")
    list_display_links = ("id", "product")
    save_as = True
    fields = ("product", "image", "get_image")
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        """ View photo in admin panel """

        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100">')
        else:
            return f'Image not set'

    get_image.short_description = 'Image'
