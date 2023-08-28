# Description
`django-extensible-forms` is a form functionality extension for django that introduces the well established `Meta` class API for form construction. It allows customizing field widget rendition attributes and CSS on an individual level, without having to write custom HTML.

## Examples
You're using AlpineJS. You want to use its `x-model` feature without having to manually write it out in HTML for each field. You also want custom CSS, without it being a pain in the ass to do. This can be done with the following:

`python
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
`

Instantiating this form and rendering it produces the following HTML:

`html
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
`

Take notice of how our CSS is properly included ("required" is added automatically, though this can be customized on the form class definition) and our attributes were added accordingly. The `username` input has `x-model="username"` and the `autofocus` attributes, while the `password` input has `x-model="password"` and the `autocomplete="new-password"` attributes.
