from django.db import models

from users.models import User


NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    title = models.CharField(max_length=100, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    preview = models.ImageField(upload_to='course/', verbose_name='превью', **NULLABLE)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lesson')

    title = models.CharField(max_length=100, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    preview = models.ImageField(upload_to='lesson/', verbose_name='превью', **NULLABLE)
    video_link = models.CharField(max_length=200, verbose_name='видео_ссылка')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class Payments(models.Model):
    PAYMENT_CHOICES = [
        ('cash', 'наличные'),
        ('transfer', 'перевод')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, verbose_name='дата оплаты')

    course = models.ForeignKey(Course, on_delete=models.CASCADE, **NULLABLE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, **NULLABLE)

    total = models.IntegerField(verbose_name='сумма оплаты')
    payment_method = models.CharField(max_length=8, choices=PAYMENT_CHOICES, verbose_name='способ оплаты')

    def __str__(self):
        return f'{self.course if self.course else self.lesson} {self.date} {self.total}'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'


