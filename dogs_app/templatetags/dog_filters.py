from django import template
from datetime import date


register = template.Library()

@register.filter
def handle_none(value):
    if value is None or value == "":
        return "-"
    else:
        return value

@register.filter
def gender_filter(value):
    if value == 'M':
        return "Male"
    elif value == 'F':
        return "Female"
    elif value is None or value == "":
        return "-"
    else:
        return value

@register.filter
def yes_no_filter(value):
    if value == 'Y':
        return "Yes"
    elif value == 'N':
        return "No"
    elif value is None or value == "":
        return "-"
    else:
        return value


# Calculates dog's age based on their date of birth, returns age in years
@register.filter
def calculate_age(birth_date):
    if birth_date is None or birth_date == "":
        return "-"
    else:
        today = date.today()
        age_in_years = today.year - birth_date.year
        age_in_months = (today.month - birth_date.month) / 12
        age_in_days = (today.day - birth_date.day) / 365
        age = age_in_years + age_in_months + age_in_days
        return round(age, 1)
