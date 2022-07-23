# https://nancylin.xyz/how-to-implement-date-time-picker-in-django-without-javascript/

from django import forms
from django.forms import MultiWidget, TimeInput


class DatePickerInput(forms.DateInput):
    input_type = 'date'

class TimePickerInput(forms.TimeInput):
    input_type = 'time'
    
    format='%H:%M:%S'
    input_step = "1"

TimeWidgetSeconds = TimeInput(format='%H:%M:%S', attrs={'type': 'time', 'step' : 1})

class DateTimePickerInput(forms.DateTimeInput):
    input_type = 'datetime'

# wid = MultiWidget(widgets={"datum" : DatePickerInput, "čas" : TimePickerInput})
# wid.render("datetime", )
# TIME_FORMAT = '%I:%M %p'

from datetime import datetime

class DateTimeSelector(forms.widgets.MultiWidget):
    def __init__(self, attrs=None):
        widgets = [
            DatePickerInput(attrs=attrs),
            TimePickerInput(attrs=attrs)
        ]
        super(DateTimeSelector, self).__init__(widgets, attrs)

    def decompress(self, value):
        print(value)
        if isinstance(value, datetime):
            # return [value.day, value.month, value.year, value.hour, value.minute, value.second]
            return [datetime(value.year, value.month, value.day, value.hour, value.minute, value.second)]
        return [datetime(1,1,1,1,1)]

