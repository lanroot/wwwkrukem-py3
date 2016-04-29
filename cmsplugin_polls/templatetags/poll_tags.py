from django import template
from math import ceil

register = template.Library()


@register.filter()
def in_compare_to(value, total):
    return str(int(ceil(float(value) / float(total) * 100)))

@register.simple_tag
def get_choice_rate(poll, choice):
    return "%d%%" % poll.getrate(choice)
