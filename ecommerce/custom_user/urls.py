from django.urls import path
from . import views

urlpatterns = [
    path('registration/', views.CustomerRegistrationView.as_view(), name='customer-registration'),
    path('login/', views.CustomerLoginView.as_view(), name='customer-login'),
    path('logout/', views.CustomerLogoutView.as_view(), name='customer-logout'),
    path(
        'forgot-password/',
        views.CustomerForgotPasswordView.as_view(),
        name='customer-forgot-password'
    ),
    path(
        'reset-password/<email>/<token>/',
        views.CustomerResetPasswordView.as_view(),
        name='customer-reset-password'
    ),
    path('logout/', views.CustomerLogoutView.as_view(), name='customer-logout'),
    path('my-profile/', views.CustomerProfileView.as_view(), name='customer-profile'),
    path(
        'update-profile/<int:pk>/',
        views.CustomerUpdateProfileView.as_view(),
        name='customer-update-profile'
    ),
    path(
        'my-profile/order/<int:pk>', views.CustomerOrderDetailView.as_view(), name='order-detail'
    ),
    path('make-order-pdf/<int:pk>/', views.make_order_pdf, name='customer-make-pdf'),
]
