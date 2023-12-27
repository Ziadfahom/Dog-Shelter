# For filtering datetime objects in templates

from django import template
import datetime

register = template.Library()


@register.filter(name='format_datetime')
def format_datetime(value):
    # Debug: Print the type of the value received
    print(f"Original value type: {type(value)} - {value}")

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

    # Debug: Print the formatted value
    print(f"Formatted value: {formatted}")
    return formatted
