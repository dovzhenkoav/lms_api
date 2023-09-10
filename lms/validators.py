from rest_framework.serializers import ValidationError


class LinkValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        link: str = dict(value).get(self.field)
        if not link.startswith('https://youtube.com'):
            return ValidationError('Ссылка на материал должна начинаться с "https://youtube.com"')
