from django import forms
from django.core.validators import RegexValidator

class InterventionWidget(forms.widgets.MultiWidget):
    def __init__(self, attrs=None):
        widgets = [forms.TextInput(),
                   forms.TextInput()]
        super(InterventionWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [str(value[i:i+1] for i in range(0, len(value), 1))]
        else:
            return ['' for _ in range(12)]

class InterventionField(forms.MultiValueField):
    widget = InterventionWidget

    def __init__(self, *args, **kwargs):
        list_fields = [forms.fields.CharField(max_length=1, validators=[RegexValidator('^[0-9]$')]) for _ in range(12)]
        super(InterventionField, self).__init__(list_fields, *args, **kwargs)

    def compress(self, values):                                                
        return ''.join(values)