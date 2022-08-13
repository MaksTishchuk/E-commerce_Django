from django.core.paginator import Paginator


def pagination_context(queryset, page_number=1):
    paginator = Paginator(queryset, 8)
    page_obj = paginator.get_page(page_number)
    product_list = paginator.page(page_number)
    extra_context = {
        'product_list': product_list,
        'paginator': paginator,
        'page_obj': page_obj
    }
    return extra_context


def sort(get_params):
    sort_params = ''
    for k, v in get_params:
        if v and (k != 'page' or k != 'posts_number'):
            sort_params += f'{k}={v}&'
    return sort_params
