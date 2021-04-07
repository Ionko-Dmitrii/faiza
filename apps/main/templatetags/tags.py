from django import template

register = template.Library()


@register.filter
def get_next_category(arr, obj):
    category_index = list(arr).index(obj)
    next_category = (
        0 if (category_index + 1) > (len(arr) - 1) else category_index + 1)
    return arr[next_category]
