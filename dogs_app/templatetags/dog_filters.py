import pytz
from django import template
from datetime import date, time
from django.utils import timezone


register = template.Library()

@register.filter
def handle_none(value):
    if value is None or value == "" or value == "N/A":
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


# Calculate the value for sessionDurationInMins using minutes, hours and days
@register.filter
def format_duration(value):
    minutes = value % 60
    hours = (value // 60) % 24
    days = (value // 60) // 24

    if days > 0:
        return f"{days}d {hours}h {minutes}m"
    elif hours > 0:
        return f"{hours}h {minutes}m"
    else:
        return f"{minutes}m"

# Better display for dateTime value
@register.filter
def format_european_datetime(value):
    if value is None:
        return "-"

    # Convert to local timezone
    local_tz = pytz.timezone('Asia/Jerusalem')
    local_time = timezone.localtime(value, local_tz)

    date_str = local_time.strftime("%d-%m-%Y")
    time_str = local_time.strftime("%H:%M:%S")

    return f"{date_str} at {time_str}"


# Better display for Time value
@register.filter(name='format_time_24hr')
def format_time_24hr(value):
    if isinstance(value, time):
        return value.strftime("%H:%M:%S")
    else:
        return value