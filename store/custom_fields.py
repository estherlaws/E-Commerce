from django.db import models

class FormattedPhoneNumberField(models.CharField):
    description = "A phone number field that automatically formats the input"

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 14  # Length of formatted phone number (including dashes and parentheses)
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        # Convert the input value to the formatted phone number
        if value is None:
            return value
        if len(value) == 10:  # Assuming the input is a 10-digit number
            return f"({value[0:3]}) {value[3:6]}-{value[6:]}"
        return value