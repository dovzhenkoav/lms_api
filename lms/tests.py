from rest_framework.test import APITestCase, APIClient

from lms.models import Course, Lesson, CourseSubscription
from users.models import User


class LessonTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='admin@ya.ru')
        self.user.set_password('1q2w3e')
        self.user.save()
        self.course = Course.objects.create(title='Course1',
                              description='Sample text',
                              owner=self.user)
        Lesson.objects.create(course=self.course, title="Lesson1", description="Sample text", owner=self.user, video_link='https://youtube.com/')
        Lesson.objects.create(course=self.course, title="Lesson2", description="Sample text", owner=self.user, video_link='https://youtube.com/')
        response = self.client.post('/users/token/', {'email': 'admin@ya.ru', 'password': '1q2w3e'})
        token = response.json()['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def test_1get_lesson_list(self):
        """Тестирование вывода списка уроков."""
        response = self.client.get('/lesson/')
        response = response.json()
        self.assertEqual(response, {
            'count': 2,
            'next': None,
             'previous': None,
             'results': [{'course': 1,
                          'description': 'Sample text',
                          'id': 1,
                          'owner': 1,
                          'preview': None,
                          'title': 'Lesson1',
                          'video_link': 'https://youtube.com/'},
                         {'course': 1,
                          'description': 'Sample text',
                          'id': 2,
                          'owner': 1,
                          'preview': None,
                          'title': 'Lesson2',
                          'video_link': 'https://youtube.com/'}]})

    def test_2get_lesson_create(self):
        data = {
            "title": "lesson3",
            "description": "Sample text",
            "video_link": "https://youtube.com/",
            "course": self.course.id,
            "owner": self.user.pk
        }
        response = self.client.post('/lesson/create/', data=data)
        self.assertEqual(response.json(), {'id': 5,
                                           'title': 'lesson3',
                                           'description': 'Sample text',
                                           'preview': None,
                                           'video_link': 'https://youtube.com/',
                                           'course': 2,
                                           'owner': 2})

        data = {
            "title": "lesson3",
            "description": "Sample text",
            "video_link": "https://vimeo.com/",
            "course": self.course.id,
            "owner": self.user.pk
        }
        response = self.client.post('/lesson/create/', data=data)
        self.assertEqual(response.json(), {'non_field_errors': ['Ссылка на материал должна начинаться с "https://youtube.com"']})

    def test_3lesson_retrieve(self):
        response = self.client.get('/lesson/7/')
        self.assertEqual(response.json(), {'id': 7, 'title': 'Lesson2', 'description': 'Sample text', 'preview': None, 'video_link': 'https://youtube.com/', 'course': 3, 'owner': 3})

    def test_4lesson_update(self):
        data = {
            "title": "lesson99",
            "description": "Sample text",
            "video_link": "https://youtube.com/",
            "course": self.course.id,
            "owner": self.user.pk
        }
        response = self.client.put('/lesson/update/8/', data=data)
        self.assertEqual(response.json(), {'id': 8, 'title': 'lesson99', 'description': 'Sample text', 'preview': None,
                                           'video_link': 'https://youtube.com/', 'course': 4, 'owner': 4})

    def test_5lesson_destroy(self):
        response = self.client.delete('/lesson/update/8/')
        self.assertTrue(not Lesson.objects.filter(pk=8).exists())


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='admin@ya.ru')
        self.user.set_password('1q2w3e')
        self.user.save()
        self.course = Course.objects.create(title='Course1',
                              description='Sample text',
                              owner=self.user)
        Lesson.objects.create(course=self.course, title="Lesson1", description="Sample text", owner=self.user, video_link='https://youtube.com/')
        Lesson.objects.create(course=self.course, title="Lesson2", description="Sample text", owner=self.user, video_link='https://youtube.com/')
        response = self.client.post('/users/token/', {'email': 'admin@ya.ru', 'password': '1q2w3e'})
        token = response.json()['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def test_1set_subscription(self):
        data = {
            "user": self.user.pk,
            "course": self.course.pk
        }
        response = self.client.post('/subscription/create/', data=data)
        self.assertEqual(response.json(), {'course': 6, 'id': 1, 'user': 6})

    def test_2delete_subscription(self):
        self.client.delete('/subscription/delete/1/')
        self.assertTrue(not CourseSubscription.objects.filter(pk=1).exists())


