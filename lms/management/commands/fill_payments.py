from django.core.management import BaseCommand
from django.db.utils import IntegrityError

from lms.models import Course, Lesson, Payments
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        try:
            course = Course.objects.create(id=1, title="Course1", description="Sample text")
        except IntegrityError:
            course = Course.objects.get(id=1)
        try:
            lesson = Lesson.objects.create(id=1, course=course, title="Lesson1", description="Sample text", video_link="https://")
        except IntegrityError:
            lesson = Lesson.objects.get(id=1)

        User = get_user_model()
        user = User.objects.get(pk=1)

        Payments.objects.create(user=user, course=course, total=111, payment_method='cash')
        Payments.objects.create(user=user, course=course, total=222, payment_method='transfer')
        Payments.objects.create(user=user, lesson=lesson, total=333, payment_method='cash')
        Payments.objects.create(user=user, lesson=lesson, total=444, payment_method='transfer')


