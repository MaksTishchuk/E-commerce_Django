from django import forms

from shop.models import Product


class CustomAdminLoginForm(forms.Form):
    """ Form for admin login """

    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())


class CustomAdminCreateProductForm(forms.ModelForm):
    """ Form for create product in custom admin """

    more_images = forms.FileField(required=False, widget=forms.FileInput(attrs={
        "class": "form-control",
        "multiple": True
    }))

    class Meta:
        model = Product
        fields = ["title", "slug", "category", "image", "market_price",
                  "selling_price", "description", "warranty", "return_policy"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter the product title here..."
            }),
            "slug": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter the unique slug here..."
            }),
            "category": forms.Select(attrs={
                "class": "form-control"
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
            "market_price": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Market price of the product..."
            }),
            "selling_price": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Selling price of the product..."
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Description of the product...",
                "rows": 5
            }),
            "warranty": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter the product warranty here..."
            }),
            "return_policy": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter the product return policy here..."
            }),

        }


