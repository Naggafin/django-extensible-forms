from django import template

register = template.Library()


@register.filter
def pop(stack: list):
	return stack.pop()
