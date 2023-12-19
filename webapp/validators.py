from django.core.exceptions import ValidationError


def validate_title(value):
    if 'badword' in value.lower():
        raise ValidationError('Заголовок не должен содержать запрещенное слово "badword".')


def validate_description(value):
    if 'badword' in value.lower():
        raise ValidationError('Полное описание не должно содержать запрещенное слово "badword".')
