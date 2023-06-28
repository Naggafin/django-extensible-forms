from django.forms.utils import ErrorDict, ErrorList, RenderableMixin

__all__ = ("FieldErrorList", "FieldErrorDict")


class RenderableFieldMixin(RenderableMixin):
	def as_field_group(self):
		return self.render()

	def as_hidden(self):
		raise NotImplementedError(
			"Subclasses of RenderableFieldMixin must provide an as_hidden() method."
		)

	def as_widget(self):
		raise NotImplementedError(
			"Subclasses of RenderableFieldMixin must provide an as_widget() method."
		)

	def __str__(self):
		"""Render this field as an HTML widget."""
		if self.field.show_hidden_initial:
			return self.as_widget() + self.as_hidden(only_initial=True)
		return self.as_widget()

	__html__ = __str__


class FieldErrorMixin:
	def __init__(self, *args, boundfield=None, **kwargs):
		super().__init__(*args, **kwargs)
		assert boundfield is not None, "`boundfield` must be specified"
		self.boundfield = boundfield

	def get_context(self):
		context = super().get_context()
		context["field"] = self.boundfield
		return context


class FieldErrorList(FieldErrorMixin, ErrorList):
	template_name = "django_extensible_forms/forms/errors/list/field_default.html"


class FieldErrorDict(FieldErrorMixin, ErrorDict):
	template_name = "django_extensible_forms/forms/errors/dict/field_default.html"
