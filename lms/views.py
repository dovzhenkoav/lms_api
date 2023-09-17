from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from lms.models import Course, Lesson, Payments, CourseSubscription
from lms.serializers import CourseSerializer, LessonSerializer, PaymentsSerializer, CourseSubscriptionSerializer
from lms.permissions import IsManager, IsNotManager, UserPermission, IsLessonOwner, IsCourseOwner
from lms.paginators import CoursePaginator, LessonPaginator

from lms import services
from lms.tasks import send_course_update_mail


class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = [UserPermission]
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CoursePaginator

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff or self.request.user.groups.filter(
                name="managers").exists():
            return Course.objects.all()

        return Course.objects.filter(course_owner=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        subs = CourseSubscription.objects.filter(course=instance)
        users_emails = [sub.user.email for sub in subs]
        send_course_update_mail.delay(course_title=instance.title, user_emails=users_emails)

        return super().update(request, *args, **kwargs)


class LessonCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsNotManager]
    serializer_class = LessonSerializer


class LessonListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = LessonPaginator

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff or self.request.user.groups.filter(
                name="managers").exists():

            return Lesson.objects.all()

        return Lesson.objects.filter(owner=self.request.user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsLessonOwner]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsLessonOwner]
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


class PaymentsCreateAPIView(APIView):
    def post(self, request):
        number = request.data['card_number']
        exp_month = request.data['card_exp_month']
        exp_year = request.data['card_exp_year']
        cvc = request.data['card_cvc']

        bill_id = services.create_payment(20000, 'usd')
        status = services.make_payment(bill_id, number, exp_month, exp_year, cvc)

        return Response({'status': status})


class CourseSubscriptionCreateAPIView(generics.CreateAPIView):
    serializer_class = CourseSubscriptionSerializer


class CourseSubscriptionDeleteAPIView(generics.DestroyAPIView):
    serializer_class = CourseSubscriptionSerializer
    queryset = CourseSubscription.objects.all()
