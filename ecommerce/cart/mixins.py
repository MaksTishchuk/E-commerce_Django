from django.views.generic import View

from .models import Cart


class CartMixin(object):
    def dispatch(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id")
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            if request.user.is_authenticated and request.user.customer:
                cart.customer = request.user.customer
                cart.save()
        return super().dispatch(request, *args, **kwargs)
