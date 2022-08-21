from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django import forms

from .models import Order


class OrderForm(forms.ModelForm):

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    class Meta:
        model = Order
        fields = ['ordered_by', 'shipping_address', 'phone', 'email', 'captcha']
