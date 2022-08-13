from django.urls import path
from . import views

urlpatterns = [
    path('', views.MyCartView.as_view(), name='my-cart'),
    path('add-to-cart/<int:prod_id>/', views.AddToCartView.as_view(), name='add-to-card'),
    path('manage-cart/<int:cartprod_id>/', views.ManageCartView.as_view(), name='manage-cart'),
    path('clear-cart/', views.ClearCartView.as_view(), name='clear-cart'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
]
