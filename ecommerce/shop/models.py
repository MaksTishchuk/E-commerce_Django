from django.db import models
from django.urls import reverse


class Category(models.Model):
    """ Model Category """

    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='category_img/%Y/%m/%d/', blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Product(models.Model):
    """ Model Product """

    category = models.ForeignKey(Category, related_name='products', on_delete=models.PROTECT)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    warranty = models.CharField(max_length=255, blank=True, null=True)
    return_policy = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='product_img/%Y/%m/%d/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    market_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    selling_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    view_count = models.PositiveIntegerField(default=0)

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

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=f'products_images/%Y/%m/%d/', blank=True, null=True)

    def __str__(self):
        return f'Image_{self.id} for {self.product.title}'
