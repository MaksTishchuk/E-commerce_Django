from django.urls import path
from . import views

urlpatterns = [
    path('', views.MyCartView.as_view(), name='my-cart'),
    # path('add-to-cart/<int:prod_id>/', views.AddToCartView.as_view(), name='add-to-card'),
    path('add-to-cart-ajax', views.add_to_cart_ajax, name='add-to-cart-ajax'),
    # path('manage-cart/<int:cartprod_id>/', views.ManageCartView.as_view(), name='manage-cart'),
    path('manage-cart-ajax', views.manage_cart_ajax, name='manage-cart-ajax'),
    path('clear-cart/', views.ClearCartView.as_view(), name='clear-cart'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
]
