from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated

from lms.models import Course, Lesson, Payments
from lms.serializers import CourseSerializer, LessonSerializer, PaymentsSerializer
from lms.permissions import IsManager, IsNotManager, UserPermission, IsLessonOwner, IsCourseOwner


class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = [UserPermission]
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff or self.request.user.groups.filter(
                name="managers").exists():
            return Course.objects.all()

        return Course.objects.filter(course_owner=self.request.user)


class LessonCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsNotManager]
    serializer_class = LessonSerializer


class LessonListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff or self.request.user.groups.filter(
                name="managers").exists():

            return Lesson.objects.all()

        return Lesson.objects.filter(lesson_owner=self.request.user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsLessonOwner]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsManager, IsLessonOwner]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDestroyAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsNotManager]
    queryset = Lesson.objects.all()


class PaymentsListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'payment_method')
    ordering_fields = ('date',)
