from rest_framework import serializers

from lms.models import Course, Lesson, Payments, CourseSubscription
from lms.validators import LinkValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [LinkValidator(field='video_link')]


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(source='lesson', many=True, read_only=True)
    my_subscription = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_lessons_count(self, instance):
        course_lessons = instance.lesson.all()
        if course_lessons:
            return len(course_lessons)
        return 0

    def get_my_subscription(self, instance):
        request = self._context["request"]
        print(instance.__dict__)
        return CourseSubscription.objects.filter(user=request.user.id, course=instance.id).exists()


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'


class CourseSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSubscription
        fields = '__all__'

