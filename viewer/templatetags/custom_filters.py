from django import template

register = template.Library()

@register.filter
def attr(obj, attr_name):
    return getattr(obj, attr_name)

@register.filter
def prettydate(value):
    if hasattr(value, 'strftime'):
        return value.strftime("%d.%m.%Y")
    return value or "-"

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_status(item, field):
    if hasattr(item, 'status_map'):
        return item.status_map.get(field, 'ok')
    return 'ok'

@register.filter
def get_status_class(item, field):
    status = get_status(item, field)
    return status