from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    """ Model Category """

    title = models.CharField(max_length=250, verbose_name=_('Title'))
    slug = models.SlugField(unique=True, verbose_name=_('Slug'))
    image = models.ImageField(
        upload_to='category_img/%Y/%m/%d/', blank=True, null=True, verbose_name=_('Image')
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Product(models.Model):
    """ Model Product """

    category = models.ForeignKey(
        Category, related_name='products', on_delete=models.PROTECT, verbose_name=_('Category')
    )
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    slug = models.SlugField(unique=True, verbose_name=_('Slug'))
    description = models.TextField(blank=True, null=True, verbose_name=_('Description'))
    warranty = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Warranty'))
    return_policy = models.CharField(
        max_length=255, blank=True, null=True, verbose_name=_('Return policy')
    )
    image = models.ImageField(
        upload_to='product_img/%Y/%m/%d/', blank=True, null=True, verbose_name=_('Image')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    market_price = models.DecimalField(
        max_digits=8, decimal_places=2, default=0, verbose_name=_('Market Price')
    )
    selling_price = models.DecimalField(
        max_digits=8, decimal_places=2, default=0, verbose_name=_('Selling Price')
    )
    view_count = models.PositiveIntegerField(default=0, verbose_name=_('View Count'))

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class ProductImage(models.Model):
    """ Model Images for Product """

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('Product'))
    image = models.ImageField(
        upload_to=f'products_images/%Y/%m/%d/', blank=True, null=True, verbose_name=_('Image')
    )

    def __str__(self):
        return f'Image_{self.id} for {self.product.title}'
