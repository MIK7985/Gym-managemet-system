import datetime
from django import template

register = template.Library()

@register.filter(name='age')
def age(dob):
    """
    Template filter that converts a date of birth to age.
    """
    today = datetime.date.today()
    try:
        birthday = dob.replace(year=today.year)
    except ValueError:  # raised when birth date is February 29 and the current year is not a leap year
        birthday = dob.replace(year=today.year, month=dob.month + 1, day=1)
    
    if birthday > today:
        return today.year - dob.year - 1
    else:
        return today.year - dob.year
