from django.forms.widgets import Textarea

from ..boundfield import ExtensibleBoundField

__all__ = ("Bootstrap5BoundField",)


class Bootstrap5BoundField(ExtensibleBoundField):
	def label_tag(self, contents=None, attrs=None, label_suffix=None, tag=None):
		attrs = attrs or {}
		attrs["class"] = set(attrs["class"].split()) if "class" in attrs else set()
		if getattr(self.field.widget, "input_type", None) == "checkbox":
			attrs["class"].add("form-check-label")
		else:
			attrs["class"].add("form-label")
		attrs["class"] = " ".join(attrs["class"])
		return super().label_tag(
			contents=contents, attrs=attrs, label_suffix=label_suffix, tag=tag
		)

	def css_classes(self, extra_classes=None):
		css = set(super().css_classes(extra_classes=extra_classes).split())
		widget = self.field.widget
		if hasattr(widget, "input_type"):
			match widget.input_type:
				case "select":
					css.add("form-select")
				case "checkbox":
					css.add("form-check-input")
				case "color":
					css.add("form-control-color")
				case "range":
					css.add("form-range")
				case _:
					css.add("form-control")
		elif isinstance(widget, Textarea):
			css.add("form-control")
		return " ".join(css)
