# https://nancylin.xyz/how-to-implement-date-time-picker-in-django-without-javascript/

from django import forms

TIME_FORMAT = '%I:%M %p'

class DatePickerInput(forms.DateInput):
    input_type = 'date'

class TimePickerInput(forms.TimeInput):
    input_type = 'time'
    input_step = "1"

class DateTimePickerInput(forms.DateTimeInput):
    input_type = 'datetime'