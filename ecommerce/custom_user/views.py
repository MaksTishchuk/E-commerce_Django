from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import get_template
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, FormView, TemplateView, DetailView, UpdateView
from xhtml2pdf import pisa

from cart.models import Order, CartProduct, Cart, Customer
from custom_user.forms import (
    CustomerRegistrationForm, CustomerLoginForm, ForgotPasswordForm, ResetPasswordForm,
    CustomerUpdateProfileForm
)
from custom_user.utils import password_reset_token


class CustomerRegistrationView(CreateView):
    """ View for registration customer """

    template_name = 'custom_user/customer_registration.html'
    form_class = CustomerRegistrationForm
    success_url = reverse_lazy('customer-login')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        email = form.cleaned_data.get('email')
        user = User.objects.create_user(username, email, password)
        form.instance.user = user
        # login(self.request, user)
        return super().form_valid(form)


class CustomerLoginView(FormView):
    """ View for login customer """

    template_name = 'custom_user/customer_login.html'
    form_class = CustomerLoginForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None and Customer.objects.filter(user=user).exists():
            login(self.request, user)
        else:
            return render(
                self.request,
                self.template_name,
                {'form': self.form_class, 'error': 'Invalid credentials'}
            )
        return super().form_valid(form)


class CustomerLogoutView(View):
    """ View for logout customer """

    def get(self, request):
        logout(request)
        return redirect('home')


class CustomerProfileView(TemplateView):
    """ Customer profile view """

    template_name = 'custom_user/customer_profile.html'

    def dispatch(self, request, *args, **kwargs):
        if not (
                request.user.is_authenticated and Customer.objects.filter(
            user=request.user).exists()
        ):
            return redirect('customer-login')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.request.user.customer
        context['customer'] = customer
        orders = Order.objects.filter(cart__customer=customer)
        context['orders'] = orders
        return context


class CustomerUpdateProfileView(UpdateView):
    """ Customer profile update view """

    model = Customer
    form_class = CustomerUpdateProfileForm
    template_name = 'custom_user/customer_update_profile.html'
    success_url = reverse_lazy('customer-profile')


class CustomerOrderDetailView(DetailView):
    """ Order detail view """

    template_name = 'custom_user/customer_order_detail.html'
    model = Order
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = Order.objects.filter(id=self.kwargs.get('pk')).select_related('cart').last()
        cart_products = order.cart.cartproduct_set.all().select_related('product')
        context['cart_products'] = cart_products
        return context


class CustomerForgotPasswordView(FormView):
    """ Forgot password view """

    template_name = 'custom_user/forgot_password.html'
    form_class = ForgotPasswordForm
    success_url = '/user/forgot-password/?msg=sent'

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        # get current host ip/domain
        url = self.request.META['HTTP_HOST']
        customer = Customer.objects.get(user__email=email)
        user = customer.user
        text_content = 'Please click the link below to reset your password!'
        html_content = url + "/user/reset-password/" + email + "/" \
                       + password_reset_token.make_token(user) + "/"
        send_mail(
            'Password Reset Link | Maks Ecommerce',
            text_content + html_content,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        return super().form_valid(form)


class CustomerResetPasswordView(FormView):
    """ Reset password view """

    template_name = 'custom_user/reset_password.html'
    form_class = ResetPasswordForm
    success_url = reverse_lazy('customer-login')

    def dispatch(self, request, *args, **kwargs):
        email = self.kwargs.get("email")
        user = User.objects.get(email=email)
        token = self.kwargs.get("token")
        if user is None or not password_reset_token.check_token(user, token):
            return redirect(reverse("customer-forgot-password") + "?msg=error")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        password = form.cleaned_data['new_password']
        email = self.kwargs.get("email")
        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()
        return super().form_valid(form)


def make_order_pdf(request, pk):
    order = Order.objects.filter(id=pk).select_related('cart').last()
    cart_products = order.cart.cartproduct_set.all().select_related('product')
    template_path = 'custom_user/pdf_file.html'
    context = {'order': order, 'cart_products': cart_products}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=ORDER_{str(order.id)}'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
