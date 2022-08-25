from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, FormView, DetailView, ListView, CreateView, \
    UpdateView, DeleteView

from cart.models import Order
from shop.models import Product, ProductImage
from .forms import CustomAdminLoginForm, CustomAdminCreateProductForm
from .mixins import AdminRequiredMixin
from .models import AdminUser


class CustomAdminLoginView(FormView):
    """ Custom admin login view """

    template_name = 'custom_admin/admin_login.html'
    form_class = CustomAdminLoginForm
    success_url = reverse_lazy('custom-admin-home')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user and (AdminUser.objects.filter(user=user).exists() or user.is_staff):
            login(self.request, user)
        else:
            return render(
                self.request,
                self.template_name,
                {'form': self.form_class, 'error': 'Invalid credentials'}
            )
        return super().form_valid(form)


class CustomAdminHomeView(AdminRequiredMixin, TemplateView):
    """ Home page view for custom admin """

    template_name = 'custom_admin/admin_home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pending_orders'] = Order.objects.filter(
            order_status='Order Received'
        ).order_by('-id')
        return context


class CustomAdminOrderDetailView(AdminRequiredMixin, DetailView):
    """ Detail View order for custom admin """

    template_name = 'custom_admin/admin_order_detail.html'
    model = Order
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = Order.objects.filter(id=self.kwargs.get('pk')).select_related('cart').last()
        cart_products = order.cart.cartproduct_set.all().select_related('product')
        context['cart_products'] = cart_products
        context["all_status"] = order.ORDER_STATUS
        return context


class CustomAdminAllOrdersView(AdminRequiredMixin, ListView):
    """ Custom admin all orders view """

    template_name = 'custom_admin/admin_all_orders.html'
    queryset = Order.objects.all().order_by("-id")
    context_object_name = "all_orders"


class CustomAdminOrderStatusView(AdminRequiredMixin, View):
    """ Change order status view """

    def post(self, request, *args, **kwargs):
        order_id = self.kwargs["pk"]
        order = Order.objects.get(id=order_id)
        new_status = request.POST.get("status")
        order.order_status = new_status
        order.save()
        return redirect(reverse_lazy("custom-admin-order", kwargs={"pk": order_id}))


class CustomAdminAllProductsView(AdminRequiredMixin, ListView):
    """ Custom admin all products view """

    template_name = 'custom_admin/admin_all_products.html'
    queryset = Product.objects.all().order_by('-id')
    context_object_name = 'all_products'


class CustomAdminAddProductView(AdminRequiredMixin, CreateView):
    """ Custom admin create product """

    template_name = 'custom_admin/admin_create_product.html'
    form_class = CustomAdminCreateProductForm
    success_url = reverse_lazy('custom-admin-all-products')

    def form_valid(self, form):
        product = form.save()
        images = self.request.FILES.getlist("more_images")
        for image in images:
            ProductImage.objects.create(product=product, image=image)
        return super().form_valid(form)


class CustomAdminEditProductView(AdminRequiredMixin, UpdateView):
    """ Custom admin edit product """

    model = Product
    form_class = CustomAdminCreateProductForm
    template_name = 'custom_admin/admin_create_product.html'
    success_url = reverse_lazy('custom-admin-all-products')


class CustomAdminDeleteProductView(AdminRequiredMixin, DeleteView):
    """ Custom admin delete product """

    model = Product
    template_name = 'custom_admin/admin_delete_product.html'
    success_url = reverse_lazy('custom-admin-all-products')
