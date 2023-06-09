from django import template

register = template.Library()

@register.filter
def handle_none(value):
    if value is None:
        return ""
    else:
        return value

@register.filter
def gender_filter(value):
    if value == 'M':
        return "Male"
    elif value == 'F':
        return "Female"
    elif value is None:
        return ""
    else:
        return value

@register.filter
def yes_no_filter(value):
    if value == 'Y':
        return "Yes"
    elif value == 'N':
        return "No"
    elif value is None:
        return ""
    else:
        return value
