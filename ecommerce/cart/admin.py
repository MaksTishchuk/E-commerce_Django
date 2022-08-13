from django.contrib import admin

from .models import Customer, Cart, CartProduct, Order


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """ Customer in admin panel """

    list_display = ("id", "user", "full_name", "phone", "joined_in",)
    list_display_links = ("id", "user", "full_name")
    save_as = True
    fields = (
        "user",
        "full_name",
        "phone",
        "address",
        "joined_in",
    )
    readonly_fields = ("joined_in",)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """ Cart in admin panel """

    list_display = ("id", "customer", "final_price", "created_at",)
    list_display_links = ("id", "customer",)
    save_as = True
    fields = (
        "customer",
        "final_price",
        "created_at",
    )
    readonly_fields = ("created_at",)


@admin.register(CartProduct)
class CartProductAdmin(admin.ModelAdmin):
    """ Cart Product in admin panel """

    list_display = ("id", "cart", "product", "rate", "quantity", "subtotal",)
    list_display_links = ("id", "cart", "product")
    save_as = True
    fields = (
        "cart",
        "product",
        "rate",
        "quantity",
        "subtotal",
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """ Order in admin panel """

    list_display = ("id", "cart", "ordered_by", "email", "phone", "created_at", "total")
    list_display_links = ("id", "cart", "ordered_by")
    save_as = True
    fields = (
        "cart",
        "ordered_by",
        "shipping_address",
        "phone",
        "email",
        "subtotal",
        "discount",
        "total",
        "order_status",
        "created_at",
        "payment_method",
        "payment_completed",
    )
    readonly_fields = ('created_at',)
