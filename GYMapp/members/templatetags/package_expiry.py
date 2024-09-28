# payment/templatetags/packageexpiry.py

from django import template

register = template.Library()

@register.filter(name='package_status')
def package_status(remaining_days):
    if remaining_days <= 0:
        return "Expired"
    return f"{remaining_days} days remaining"

