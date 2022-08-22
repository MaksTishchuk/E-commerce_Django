from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Customer(models.Model):
    """ Model Customer """

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('User'))
    full_name = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('Full Name'))
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name=_('Phone'))
    address = models.CharField(max_length=300, null=True, blank=True, verbose_name=_('Address'))
    joined_in = models.DateTimeField(auto_now_add=True, verbose_name=_('Joined In'))

    def __str__(self):
        return f'User: {self.user}'

    class Meta:
        ordering = ('user',)
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
