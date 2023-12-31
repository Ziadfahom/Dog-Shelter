# For filtering datetime objects in templates

from django import template
import datetime

register = template.Library()


@register.filter(name='format_datetime')
def format_datetime(value):
    if isinstance(value, datetime.datetime):
        # Format it directly
        formatted = value.strftime("%B %d, %Y %I:%M %p")  # e.g., "June 16, 2023 02:53 AM"
    elif isinstance(value, str):
        # If it's a string, parse and format it
        try:
            dt = datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
            formatted = dt.strftime("%B %d, %Y %I:%M %p")
        except ValueError as e:
            print(f"Date parsing error: {e}")
            return value  # Return the original value if parsing fails
    else:
        # If it's neither, return as is
        return value

    return formatted


@register.filter(name='format_time')
def format_time(value):
    if value is None:
        # If the value is None, return an empty string or a default time value
        return ""
    elif isinstance(value, datetime.time):
        # Format it directly
        formatted = value.strftime("%H:%M") # e.g., "14:30"
    elif isinstance(value, str):
        # If it's a string, parse and format it
        try:
            t = datetime.datetime.strptime(value, "%H:%M").time()
            formatted = t.strftime("%H:%M")
        except ValueError as e:
            print(f"Time parsing error: {e}")
            return value # Return the original value if parsing fails
    else:
        # If it's neither, return as is
        return value
    return formatted
