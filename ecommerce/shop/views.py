from django.db.models import F, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.views.generic import TemplateView, ListView, DetailView

from cart.mixins import CartMixin
from .models import Category, Product, ProductImage
from .utils import pagination_context, sort
from .filters import ProductsFilter


class HomeView(CartMixin, ListView):
    """ View Home Page """

    model = Product
    template_name = 'home.html'

    def get_queryset(self):
        return Product.objects.all().select_related('category').order_by('-view_count')[:8]


class AllProductsView(CartMixin, ListView):
    """ View All Products """

    model = Product
    template_name = 'shop/products.html'

    def get_queryset(self):
        return Product.objects.all().select_related('category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = ProductsFilter(self.request.GET, queryset=self.get_queryset()).qs
        page_number = int(1 if not self.request.GET.get('page') else self.request.GET.get('page'))
        extra_context = pagination_context(queryset, page_number)
        context.update(extra_context)
        context['sort'] = sort(self.request.GET.items())
        context['form'] = ProductsFilter(self.request.GET, queryset=self.get_queryset()).form
        return context


class CategoryListView(AllProductsView):
    """ View Category Products """

    def get_queryset(self):
        return Product.objects.filter(
            category__slug=self.kwargs.get('slug')
        ).select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['this_cat'] = get_object_or_404(Category, slug=self.kwargs.get('slug')).title
        return context


class ProductDetailView(CartMixin, DetailView):
    """ View Detail Information About Product """

    model = Product
    slug_field = 'slug'
    template_name = 'shop/product_detail.html'

    def get_queryset(self):
        slug = self.kwargs.get('slug', '')
        product = super().get_queryset().filter(slug=slug).select_related('category')
        product.update(view_count=F('view_count') + 1)
        return product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug', '')
        product = Product.objects.filter(slug=slug).first()
        if self.request.user.customer in product.favourite.all():
            context['customer_favourite'] = True
        context['favourite_count'] = product.get_favourite_count()
        context['product_image'] = ProductImage.objects.filter(
            product=product
        ).order_by('-id')[:6]
        return context


def add_favourite_product(request):
    """ Add product to favourite """

    if request.method == 'POST':
        product_id = int(request.POST.get('prod_id'))
        product = get_object_or_404(Product, id=product_id)
        if request.user.customer in product.favourite.all():
            product.favourite.remove(request.user.customer)
        else:
            product.favourite.add(request.user.customer)
        if request.user.customer in product.favourite.all():
            customer_favourite = True
        else:
            customer_favourite = False
        favourite_count = product.get_favourite_count()
        return JsonResponse(
            {'html': render_to_string(
                    'shop/include/favourite.html',
                    {'customer_favourite': customer_favourite, 'favourite_count': favourite_count}
            )}
        )


class SearchView(CartMixin, ListView):
    """ Search products view """

    model = Product
    template_name = 'shop/products.html'

    def get_queryset(self):
        return Product.objects.all().select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('query')
        product_list = self.get_queryset().filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
        page_number = int(1 if not self.request.GET.get('page') else self.request.GET.get('page'))
        extra_context = pagination_context(product_list, page_number)
        context['query'] = query
        context.update(extra_context)
        return context


class AboutView(CartMixin, TemplateView):
    """ View of About Us Page """

    template_name = 'about.html'


class ContactView(CartMixin, TemplateView):
    """ View of Contact Page """

    template_name = 'contact.html'
