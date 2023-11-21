from ..models import *  # NOQA
from ..models import BaseExtensibleModelForm, ExtensibleModelFormMetaclass
from ..models import ModelChoiceField as ExtensibleModelChoiceField
from ..models import ModelMultipleChoiceField as ExtensibleModelMultipleChoiceField
from ..models import extensible_formfield_callback
from ..models import modelform_factory as extensible_modelform_factory
from .fields import Bootstrap5FieldMixin, _monkey_patch_field
from .forms import Bootstrap5FormMetaclass


def bootstrap5_formfield_callback(field, **kwargs):
	formfield = extensible_formfield_callback(field, **kwargs)
	return _monkey_patch_field(formfield)


class Bootstrap5ModelFormMetaclass(
	Bootstrap5FormMetaclass, ExtensibleModelFormMetaclass
):
	formfield_callback = bootstrap5_formfield_callback

	def bases_check(mcs, bases):
		return bases == (BaseExtensibleModelForm,)


class ModelForm(BaseExtensibleModelForm, metaclass=Bootstrap5ModelFormMetaclass):
	pass


class ModelChoiceField(Bootstrap5FieldMixin, ExtensibleModelChoiceField):
	pass


class ModelMultipleChoiceField(
	Bootstrap5FieldMixin, ExtensibleModelMultipleChoiceField
):
	pass


def modelform_factory(*args, form=ModelForm, **kwargs):
	return extensible_modelform_factory(*args, form=form, **kwargs)
