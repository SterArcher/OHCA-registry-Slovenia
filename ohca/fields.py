from django import forms
from django.core.validators import RegexValidator
from django.forms import TimeInput


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

# https://nancylin.xyz/how-to-implement-date-time-picker-in-django-without-javascript/

from django import forms
from django.forms import MultiWidget, TimeInput


class DatePickerInput(forms.DateInput):
    input_type = 'date'

TimeWidgetSeconds = TimeInput(format='%H:%M:%S', attrs={'type': 'time', 'step' : 1})

class DateTimePickerInput(forms.DateTimeInput):
    input_type = 'datetime'

class TimePickerInputSeconds(forms.TimeInput):
    input_type = "time"

from datetime import datetime

class DateTimeSelector(forms.widgets.MultiWidget):
    def __init__(self, attrs=None):
        widgets = [
            DatePickerInput(attrs=attrs),
            TimePickerInputSeconds(format='%H:%M:%S', attrs={'type': 'time', 'step' : 1})
        ]
        super(DateTimeSelector, self).__init__(widgets, attrs)

    def decompress(self, value):
        if isinstance(value, datetime):
            return [value.day, value.month, value.year, value.hour, value.minute, value.second]
            # return [datetime(value.year, value.month, value.day, value.hour, value.minute, value.second)]
        return [None, None, None, None, None, None]

    def value_from_datadict(self, data, files, name):
        date, time = super(DateTimeSelector, self).value_from_datadict(data, files, name)
        return date + ' ' + time