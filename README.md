# Description
`django-extensible-forms` is a form functionality extension for django that introduces the well established `Meta` class API for form construction. It allows customizing field widget rendition attributes and CSS on an individual level, without having to write custom HTML.

## Installation
Install from pypi with `pip install django-extensible-forms` or install directly with `git clone https://github.com/Naggafin/django-extensible-forms.git && cd django-extensible-forms/ && pip install .`

Once the package is installed, add it to your project by including the following in your `settings.py`:

```python
INSTALLED_APPS = [
	"django_extensible_forms",
	"django_extensible_forms.bootstrap5",  # if you want Bootstrap5 niceities
	
	...
	
	# goes last
	"django.forms",
]

FORM_RENDERER = "django_extensible_forms.renderers.TemplatesSetting"
```


## Examples
You're using AlpineJS. You want to use its `x-model` feature without having to manually write it out in HTML for each field. You also want custom CSS, without it being a pain in the ass to do. This can be done with the following:

```python
import django_extensible_forms as forms

class MyForm(forms.Form):
	username = forms.CharField(autofocus=True)
	password = forms.CharField(autocomplete="new-password", strip=False)

	class Meta:
		css = {
			'fields': {
				'username': ["form-control"],
				'password': ["form-control"],
			}
		}
		attrs = {
			'fields': {
				'username': {'x-model': "username"},
				'password': {'x-model': "password"},
			}
		}
```

Instantiating this form and rendering it produces the following HTML:

```html
<div>
	<label for="id_username" class="required">Username:</label>
	<input type="text" name="username" required autofocus x-model="username" id="id_username" class="form-control required">
	<div id="id_usernameFeedback" class="errorlist" style="display: none;"></div>
</div>
<div>
	<label for="id_password" class="required">Password:</label>
	<input type="text" name="password" required autocomplete="new-password" x-model="password" id="id_password" class="form-control required">
	<div id="id_passwordFeedback" class="errorlist" style="display: none;"></div>
</div>
```

Take notice of how our CSS is properly included ("required" is added automatically, though this can be customized on the form class definition) and our attributes were added accordingly. The `username` input has `x-model="username"` and the `autofocus` attributes, while the `password` input has `x-model="password"` and the `autocomplete="new-password"` attributes. Attributes and CSS can be added either directly as keywoed arguments to the field or through `Meta` definitions.

# Usage
I apologize in advance for the brevity of the documentation here. I plan to write more detailed API docs, but for now, I am unfortunately far too busy. I hope this suffices for now.

## Define attributes through Meta definitions
The preferred way to define custom attributes is through the `Meta` class interface. The following fields are available for customization in the `Meta` API: `template_name`, `template_name_label`, `css`, `attrs`, `help_texts`, `error_class`, `field_error_class`, `localized_fields`, `field_order`. I'll go into detail what they're for and how to use each now.

`template_name` [`str`] sets the template for the form to use. You can still set the template the old way as well by defining it directly on the form. If you do that, the declaration on the form itself takes precedence over the declaration within the `Meta` class.

`template_name_label` [`str`] sets the template for labels for fields to use. You can still set the template the old way as well by defining it directly on the form. If you do that, the declaration on the form itself takes precedence over the declaration within the `Meta` class.

`error_class` [`object`] defines what class to use to render non-field errors.

`field_error_class` [`object`] defines what class to use to render field errors.

`field_order` [`Iterable`] defines what order the fields should appear in. This has no effect if this is manually declared within your HTML template for the form.

`localized_fields` [`Iterable | str`] defines which fields should use i18n localization for presentation. Specify `'__all__'` to include all fields. Otherwise, an iterable of field names to localize should be used.

`css` [`dict`] defines the CSS for the form. The `dict` specified should be structured like so, with any given key-value pair being optional to include:

```python
css = {
	'form': {
		'error_css_class': "custom-error-class",
		'required_css_class': "custom-required-class",
		'non_field_errors_css_class': "custom-nonfield-errors-section-class",
	},
	'fields': {
		'__all__': "css-applied-to-all-inputs",
		'<field_name_here>': "custom-input-css",
	},
	'labels': {
		'__all__': "css-applied-to-all-labels",
		'<field_name_here>': "custom-label-css",
	},
	'field_errors': {
		'__all__': "css-applied-to-all-field-errors-tag",
		'<field_name_here>': "custom-error-css",
	},
	'separators': {
		'__all__': "css-applied-to-all-field-separator-tags",
		'<field_name_here>': "custom-separator-css",
	},
	'help_texts': {
		'__all__': "css-applied-to-all-field-help-texts",
		'<field_name_here>': "custom-help-text-css",
	}
}
```

`attrs` [`dict`] defines the attributes for the form. The `dict` specified should be structured like so, with any given key-value pair being optional to include:

```python
attrs = {
	'fields': {
		'__all__': {'data-example-attr': "customValue"},
		'<field_name_here>': {'data-example-attr': "customValue"},
	},
	'labels': {
		'__all__': {'data-example-attr': "customValue"},
		'<field_name_here>': {'data-example-attr': "customValue"},
	},
	'help_texts': {
		'__all__': {'data-example-attr': "customValue"},
		'<field_name_here>': {'data-example-attr': "customValue"},
	},
}
```

## Define attributes through field definitions
Any attribute you could specify in `Meta` can be done directly within the field definition. The available extra parameters are `css`, `label_css` , `error_css`, `separator_css`, `help_text_css`, `attrs`, `label_attrs`, `separator_attrs`, `help_text_attrs`, `bf_class`, and `template_name`. **Any extra keyword argument which does not match an argument in the field's `__init__()` function spec will be applied as an HTML attribute.** This is why setting `autofocus=True` on the `CharField` for `username` in the example produced the result it did. The same result could've been achieved by passing `attrs={'autofocus': True}` instead.
I'll detail what each keyword argument is for now:

`css` [`str | Iterable`] defines what shall appear in the HTML `class` property on the `input` tag. If there is a conflicting `Meta` defintion, this definition takes precedence.

`label_css` [`str | Iterable`] defines what shall appear in the HTML `class` property on the `label` tag. If there is a conflicting `Meta` defintion, this definition takes precedence.

`error_css` [`str | Iterable`] defines what shall appear in the HTML `class` property on the `div` tag containing field errors. If there is a conflicting `Meta` defintion, this definition takes precedence.

`separator_css` [`str | Iterable`] defines what shall appear in the HTML `class` property on the `div` tag containing the field as a whole (input, label, help text, errors). If there is a conflicting `Meta` defintion, this definition takes precedence.

`help_text_css` [`str | Iterable`] defines what shall appear in the HTML `class` property on the `div` tag containing the help text. If there is a conflicting `Meta` defintion, this definition takes precedence.

`attrs` [`dict`] defines what custom attributes should appear in the HTML for the `input` tag. If there is a conflicting `Meta` defintion, the declarations within the field definition combine with the declarations in the `Meta` definition, with those defined in the field taking precedence.

`label_attrs` [`dict`] defines what custom attributes should appear in the HTML for the `label` tag. If there is a conflicting `Meta` defintion, the declarations within the field definition combine with the declarations in the `Meta` definition, with those defined in the field taking precedence.

`separator_attrs` [`dict`] defines what custom attributes should appear in the HTML for the `div` tag containing the field as a whole (input, label, help text, errors). If there is a conflicting `Meta` defintion, the declarations within the field definition combine with the declarations in the `Meta` definition, with those defined in the field taking precedence.

`help_text_attrs` [`dict`] defines what custom attributes should appear in the HTML for the `div` tag containing the help text. If there is a conflicting `Meta` defintion, the declarations within the field definition combine with the declarations in the `Meta` definition, with those defined in the field taking precedence.

`bf_class` [`object`] defines what class to use as this field's BoundField class for rendering.

`template_name` [`str`] defines what template to use to render the field as a whole, which includes the separator element, the widget, any errors, and help text. This is not to be confused with the widget template; it does not override that.
