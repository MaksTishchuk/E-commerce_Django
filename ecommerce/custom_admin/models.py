from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class AdminUser(models.Model):
    """ Model AdminUser """

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('User'))
    phone = models.CharField(max_length=12, verbose_name=_('Phone'))
    full_name = models.CharField(max_length=200, verbose_name=_('Full Name'))
    image = models.ImageField(upload_to='admins_img/%Y/%m/%d/', verbose_name=_('Image'))
    joined_in = models.DateTimeField(auto_now_add=True, verbose_name=_('Joined in'))

    def __str__(self):
        return self.user.username
