from rest_framework import serializers
from rest_framework.fields import SerializerMethodField, IntegerField
from rest_framework.relations import SlugRelatedField

from education.models import Course, Lesson, Payment, Subscription
from education.services import retrieve_payment, create_payment, make_payment
from education.validators import VideoValidator
from users.models import User


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('title', 'preview', 'description', 'updated_at')

    def get_is_subscribed(self, instance):
        user = self.context['request'].user

        if user.is_authenticated:
            if Subscription.objects.filter(user=user, course=instance).exists():
                return True
        return False


class CourseListSerializer(serializers.ModelSerializer):
    lessons_count = IntegerField()

    class Meta:
        model = Course
        fields = ('pk', 'title', 'description', 'lessons_count', 'updated_at')


class CourseDetailSerializer(serializers.ModelSerializer):
    this_course_lessons = SerializerMethodField()

    def get_this_course_lessons(self, course):
        return [lesson.title for lesson in Lesson.objects.filter(course_lesson=course)]

    class Meta:
        model = Course
        fields = ('pk', 'title', 'preview', 'description', 'this_course_lessons')


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        validators = [VideoValidator(field='link')]
        fields = ('pk', 'title', 'preview', 'link', 'course_lesson', 'buyer')


class LessonListSerializer(serializers.ModelSerializer):
    course_lesson = SlugRelatedField(slug_field='title', queryset=Course.objects.all())
    buyer = SlugRelatedField(slug_field='email', queryset=User.objects.all())

    class Meta:
        model = Lesson
        validators = [VideoValidator(field='link')]
        fields = ('pk', 'title', 'preview', 'link', 'course_lesson', 'buyer')


class LessonDetailSerializer(serializers.ModelSerializer):
    course_lesson = SlugRelatedField(slug_field='title', queryset=Course.objects.all())
    count_lesson_with_same_course = SerializerMethodField()

    def get_count_lesson_with_same_course(self, lesson):
        return Lesson.objects.filter(course_lesson=lesson.course_lesson).count()

    class Meta:
        model = Lesson
        validators = [VideoValidator(field='link')]
        fields = ('pk', 'title', 'preview', 'description', 'link', 'course_lesson', 'count_lesson_with_same_course')


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class PaymentListSerializer(serializers.ModelSerializer):
    payment_status = serializers.SerializerMethodField()
    user = SlugRelatedField(slug_field='email', queryset=User.objects.all())
    paid_course = SlugRelatedField(slug_field='title', queryset=Course.objects.all())
    paid_lesson = SlugRelatedField(slug_field='title', queryset=Lesson.objects.all())

    def get_payment_status(self, instance):
        return retrieve_payment(instance.payment_intent_id)

    class Meta:
        model = Payment
        fields = '__all__'


class PaymentRetrieveSerializer(serializers.ModelSerializer):
    payment_status = serializers.SerializerMethodField()

    def get_payment_status(self, instance):
        return retrieve_payment(instance.payment_intent_id)

    class Meta:
        model = Payment
        fields = "__all__"


class PaymentCreateSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['payment_intent_id'] = create_payment(int(validated_data.get('payment_amount')))
        payment = Payment.objects.create(**validated_data)
        return payment

    class Meta:
        model = Payment
        fields = "__all__"


class PaymentUpdateSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        payment = make_payment(instance.payment_intent_id)
        if payment == 'succeeded':
            instance.is_paid = True
            instance.save()
            return instance
        else:
            return instance

    class Meta:
        model = Payment
        fields = "__all__"


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
