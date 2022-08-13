from django.contrib.auth.models import User
from django.db import models


class AdminUser(models.Model):
    """ Model AdminUser """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=12)
    full_name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='admins_img/%Y/%m/%d/')
    joined_in = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
