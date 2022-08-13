from django import template

from shop.models import Category


register = template.Library()


def get_all_categories():
    """ Get all categories """

    return Category.objects.all().values('title', 'slug')


@register.inclusion_tag('include/tags/categories.html')
def get_categories():
    """ List of categories """

    category = get_all_categories()
    return {'category_list': category}
