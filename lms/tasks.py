from celery import shared_task
from django.core.mail import send_mail

from django.conf import settings


@shared_task
def send_course_update_mail(course_title: str, user_emails: list[str]):
    send_mail(
        'Обновление курса',  # Заголовок
        f'Ваш курс {course_title} обновился! Заходите на сайт посмотреть.',
        settings.EMAIL_HOST_USER,
        user_emails
    )
    print('Письмо отправлено')
