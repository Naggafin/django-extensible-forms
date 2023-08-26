from django import template
from django.forms import Form

from ..fields import _monkey_patch_field

__all__ = ("bootstrapify",)

register = template.Library()


@register.filter
def bootstrapify(form: Form):
	for field in form.fields.values():
		_monkey_patch_field(field)
	return form
