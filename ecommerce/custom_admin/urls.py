from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.CustomAdminLoginView.as_view(), name='custom-admin-login'),
    path('home/', views.CustomAdminHomeView.as_view(), name='custom-admin-home'),
    path('order/<int:pk>/', views.CustomAdminOrderDetailView.as_view(), name='custom-admin-order'),
    path(
        'order-status-change/<int:pk>/',
        views.CustomAdminOrderStatusView.as_view(),
        name='custom-admin-order-status'
    ),
    path('all-orders/', views.CustomAdminAllOrdersView.as_view(), name='custom-admin-all-orders'),
    path(
        'all-products/',
        views.CustomAdminAllProductsView.as_view(),
        name='custom-admin-all-products'
    ),
    path(
        'add-product/', views.CustomAdminAddProductView.as_view(), name='custom-admin-add-product'
    ),
    path(
        'edit-product/<int:pk>/',
        views.CustomAdminEditProductView.as_view(),
        name='custom-admin-edit-product'
    ),
    path(
        'delete-product/<int:pk>/',
        views.CustomAdminDeleteProductView.as_view(),
        name='custom-admin-delete-product'
    )
]
