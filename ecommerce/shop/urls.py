from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('all-products/', views.AllProductsView.as_view(), name='all-products'),
    path('product/<slug:slug>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('category/<slug:slug>/', views.CategoryListView.as_view(), name='category-list'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact')
]
