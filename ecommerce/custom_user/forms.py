from django import forms
from django.contrib.auth.models import User

from cart.models import Customer


class CustomerRegistrationForm(forms.ModelForm):
    """ Form for user registration """

    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.CharField(widget=forms.EmailInput())

    class Meta:
        model = Customer
        fields = ['username', 'password', 'email', 'full_name', 'phone', 'address']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Customer with this username already exists!')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email addresses must be unique!')
        return email


class CustomerLoginForm(forms.Form):
    """ Form for user login """

    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())


class ForgotPasswordForm(forms.Form):
    """ Forgot password form """

    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter the email used in customer account..'
    }))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not Customer.objects.filter(user__email=email).exists():
            raise forms.ValidationError('Customer with this email does not exists..')
        return email


class ResetPasswordForm(forms.Form):
    """ Reset password form """

    new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'autocomplete': 'new-password',
        'placeholder': 'Enter New Password',
    }), label="New Password")
    confirm_new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'autocomplete': 'new-password',
        'placeholder': 'Confirm New Password',
    }), label="Confirm New Password")

    def clean_confirm_new_password(self):
        new_password = self.cleaned_data.get("new_password")
        confirm_new_password = self.cleaned_data.get("confirm_new_password")
        if new_password != confirm_new_password:
            raise forms.ValidationError(
                "New Passwords did not match!")
        return confirm_new_password


class CustomerUpdateProfileForm(forms.ModelForm):
    """ Customer update profile form """

    class Meta:
        model = Customer
        fields = ['full_name', 'phone', 'address']
