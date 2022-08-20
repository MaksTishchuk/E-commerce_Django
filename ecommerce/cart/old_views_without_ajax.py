# class AddToCartView(CartMixin, View):
#     """ Add to cart view """
#
#     def get(self, request, *args, **kwargs):
#         product_id = self.kwargs['prod_id']
#         product = get_object_or_404(Product, id=product_id)
#         cart_id = self.request.session.get('cart_id', None)
#         if cart_id:
#             cart = Cart.objects.filter(id=cart_id).last()
#             this_cart_product = cart.cartproduct_set.filter(product=product)
#             if this_cart_product.exists():
#                 cart_product = this_cart_product.last()
#                 cart_product.quantity += 1
#                 cart_product.subtotal = cart_product.quantity * product.selling_price
#                 cart_product.save()
#                 cart.final_price += product.selling_price
#                 cart.save()
#             else:
#                 cart_product = CartProduct.objects.create(
#                     cart=cart, product=product, rate=product.selling_price, quantity=1,
#                     subtotal=product.selling_price
#                 )
#                 cart.final_price += product.selling_price
#                 cart.save()
#         else:
#             cart = Cart.objects.create(final_price=0)
#             self.request.session['cart_id'] = cart.id
#             cart_product = CartProduct.objects.create(
#                 cart=cart, product=product, rate=product.selling_price, quantity=1,
#                 subtotal=product.selling_price
#             )
#             cart.final_price += product.selling_price
#             cart.save()
#         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# class ManageCartView(CartMixin, View):
#     """ Manage cart products """
#
#     def get(self, request, *args, **kwargs):
#         cart_product_id = self.kwargs['cartprod_id']
#         action = request.GET.get('action')
#         cart_product = CartProduct.objects.filter(
#             id=cart_product_id).select_related('cart', 'product').last()
#         cart = cart_product.cart
#         if action == 'increment':
#             cart_product.quantity += 1
#             cart_product.subtotal += cart_product.rate
#             cart_product.save()
#             cart.final_price += cart_product.rate
#             cart.save()
#         elif action == 'decrement':
#             cart_product.quantity -= 1
#             cart_product.subtotal -= cart_product.rate
#             cart_product.save()
#             cart.final_price -= cart_product.rate
#             cart.save()
#             if cart_product.quantity < 1:
#                 cart_product.delete()
#         elif action == 'remove':
#             cart.final_price -= cart_product.subtotal
#             cart.save()
#             cart_product.delete()
#         else:
#             raise Http404()
#         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
