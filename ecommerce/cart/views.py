from django.db.models import F
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView

from .models import Customer, Cart, CartProduct, Order
from shop.models import Product
from .form import OrderForm
from .mixins import CartMixin


class AddToCartView(CartMixin, View):
    """ Add to cart view """

    def get(self, request, *args, **kwargs):
        product_id = self.kwargs['prod_id']
        product = get_object_or_404(Product, id=product_id)
        cart_id = self.request.session.get('cart_id', None)
        if cart_id:
            cart = Cart.objects.filter(id=cart_id).last()
            this_cart_product = cart.cartproduct_set.filter(product=product)
            if this_cart_product.exists():
                cart_product = this_cart_product.last()
                cart_product.quantity += 1
                cart_product.subtotal = cart_product.quantity * product.selling_price
                cart_product.save()
                cart.final_price += product.selling_price
                cart.save()
            else:
                cart_product = CartProduct.objects.create(
                    cart=cart, product=product, rate=product.selling_price, quantity=1,
                    subtotal=product.selling_price
                )
                cart.final_price += product.selling_price
                cart.save()
        else:
            cart = Cart.objects.create(final_price=0)
            self.request.session['cart_id'] = cart.id
            cart_product = CartProduct.objects.create(
                cart=cart, product=product, rate=product.selling_price, quantity=1,
                subtotal=product.selling_price
            )
            cart.final_price += product.selling_price
            cart.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class MyCartView(CartMixin, TemplateView):
    """ View for cart """

    template_name = 'cart/my_cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get('cart_id', None)
        cart_products = CartProduct.objects.filter(
            cart=cart_id
        ).select_related('product', 'cart').order_by('id')
        context['cart_products'] = cart_products
        if cart_products:
            context['final_price'] = cart_products[0].cart.final_price
        return context


class ManageCartView(CartMixin, View):
    """ Manage cart products """

    def get(self, request, *args, **kwargs):
        cart_product_id = self.kwargs['cartprod_id']
        action = request.GET.get('action')
        cart_product = CartProduct.objects.filter(
            id=cart_product_id).select_related('cart', 'product').last()
        cart = cart_product.cart
        if action == 'increment':
            cart_product.quantity += 1
            cart_product.subtotal += cart_product.rate
            cart_product.save()
            cart.final_price += cart_product.rate
            cart.save()
        elif action == 'decrement':
            cart_product.quantity -= 1
            cart_product.subtotal -= cart_product.rate
            cart_product.save()
            cart.final_price -= cart_product.rate
            cart.save()
            if cart_product.quantity < 1:
                cart_product.delete()
        elif action == 'remove':
            cart.final_price -= cart_product.subtotal
            cart.save()
            cart_product.delete()
        else:
            raise Http404()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class ClearCartView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        cart_id = self.request.session.get('cart_id', None)
        if cart_id:
            cart = Cart.objects.filter(id=cart_id).last()
            cart.cartproduct_set.all().delete()
            cart.final_price = 0
            cart.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class CheckoutView(CartMixin, CreateView):
    """ View for checkout """

    template_name = 'cart/checkout.html'
    form_class = OrderForm
    success_url = reverse_lazy('customer-profile')

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_authenticated and request.user.customer):
            return redirect('customer-login')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get('cart_id', None)
        cart_products = CartProduct.objects.filter(cart=cart_id).select_related('cart', 'product')
        context['cart_products'] = cart_products.order_by('id')
        cart = Cart.objects.filter(id=cart_id).select_related('customer').last()
        if cart:
            context['final_price'] = cart.final_price
        form = OrderForm(initial={
            'ordered_by': cart.customer.full_name,
            'shipping_address': cart.customer.address,
            'phone': cart.customer.phone,
            'email': self.request.user.email,
        })
        context['form'] = form
        return context

    def form_valid(self, form):
        cart_id = self.request.session.get('cart_id', None)
        if cart_id:
            cart = Cart.objects.filter(id=cart_id).last()
            form.instance.cart = cart
            form.instance.subtotal = cart.final_price
            form.instance.discount = 0
            form.instance.total = cart.final_price
            form.instance.order_status = 'Order Received'
            del self.request.session['cart_id']
        else:
            return redirect('home')
        return super().form_valid(form)
