from django.core.exceptions import ValidationError

def validate_company_phone_number(value):
    if not value.isdigit():
        raise ValidationError('Company phone number must contain only English digits.')
    
    if len(value) != 8:
        raise ValidationError('Home phone number must be exactly 8 digits long.')
    
    return value