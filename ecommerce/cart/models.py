from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from custom_user.models import Customer
from shop.models import Product


class Cart(models.Model):
    """ Model Cart """

    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Customer')
    )
    final_price = models.DecimalField(
        max_digits=10, default=0, decimal_places=2, verbose_name=_('Final Price')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))

    def __str__(self):
        return f'User: {self.customer} - Cart: {self.id}'

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'


class CartProduct(models.Model):
    """ Model Cart Product """

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name=_('Cart'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('Product'))
    rate = models.PositiveIntegerField(verbose_name=_('Rate'))
    quantity = models.PositiveIntegerField(default=1, verbose_name=_('Quantity'))
    subtotal = models.PositiveIntegerField(verbose_name=_('Subtotal'))

    def __str__(self):
        return f'Cart: {self.cart.id} - Cart Product: {self.id} - {self.product} - {self.quantity}'

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Cart Product'
        verbose_name_plural = 'Cart Products'


class Order(models.Model):
    """ Model Order """

    ORDER_STATUS = (
        ("Order Received", "Order Received"),
        ("Order Processing", "Order Processing"),
        ("On the way", "On the way"),
        ("Order Completed", "Order Completed"),
        ("Order Canceled", "Order Canceled"),
    )

    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, verbose_name=_('Cart'))
    ordered_by = models.CharField(max_length=200, verbose_name=_('Ordered by'))
    shipping_address = models.CharField(max_length=200, verbose_name=_('Address'))
    phone = models.CharField(max_length=20, verbose_name=_('Phone'))
    email = models.EmailField(null=True, blank=True, verbose_name=_('Email'))
    subtotal = models.PositiveIntegerField(verbose_name=_('Subtotal'))
    discount = models.PositiveIntegerField(verbose_name=_('Discount'))
    total = models.PositiveIntegerField(verbose_name=_('Total'))
    order_status = models.CharField(
        max_length=50, choices=ORDER_STATUS, verbose_name=_('Order Status')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    payment_method = models.CharField(
        max_length=20, default="Cash On Delivery", verbose_name=_('Payment Method')
    )
    payment_completed = models.BooleanField(
        default=False, null=True, blank=True, verbose_name=_('Payment Completed')
    )

    def __str__(self):
        return f'Order: {self.id}'

