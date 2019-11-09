from django import template
register = template.Library()

def hundredth(value):
    return value/100

register.filter("hundredth", hundredth)

# The above could also have been done as:
# @register.filter(name="hundredth")
# def hundredth(value):
#     return value/100
