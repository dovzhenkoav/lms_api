from django.core.management import BaseCommand
from users.models import User

class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email='ofaxt@ofa.ru',
            first_name='Admin',
            last_name='OFA',
            is_staff=True,
            is_superuser=True
        )

        user.set_password('1q2w3e')
        user.save()
