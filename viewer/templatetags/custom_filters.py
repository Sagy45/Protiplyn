from django import template
from equipment.models import STATUS_CHOICES

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

@register.simple_tag
def allowed_statuses(current_status, allowed_dict):
    """
    Vrací dropdown položky: vždy aktuální status + povolené přechody.
    """
    pool = [current_status]
    for ns in allowed_dict.get(current_status, []):
        if ns not in pool:
            pool.append(ns)
    return [
        (choice, label)
        for choice, label in STATUS_CHOICES
        if choice in pool
    ]