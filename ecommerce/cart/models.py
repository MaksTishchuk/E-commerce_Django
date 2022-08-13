from django.contrib.auth.models import User
from django.db import models

from shop.models import Product


class Customer(models.Model):
    """ Model Customer """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    joined_in = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'User: {self.user}'

    class Meta:
        ordering = ('user',)
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'


class Cart(models.Model):
    """ Model Cart """

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    final_price = models.DecimalField(max_digits=10, default=0, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'User: {self.customer} - Cart: {self.id}'

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'


class CartProduct(models.Model):
    """ Model Cart Product """

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.PositiveIntegerField()

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

    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    ordered_by = models.CharField(max_length=200)
    shipping_address = models.CharField(max_length=200)
    phone = models.CharField(max_length=12)
    email = models.EmailField(null=True, blank=True)
    subtotal = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=20, default="Cash On Delivery")
    payment_completed = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return f'Order: {self.id}'

