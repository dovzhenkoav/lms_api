from celery import shared_task

from users.models import User


@shared_task
def ban_users_if_no_activity():
    queryset = User.objects.filter(is_active=True, last_login__day__gt=30)

    for user in queryset:
        user.is_active = True
        user.save()
