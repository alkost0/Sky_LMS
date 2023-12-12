from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.generics import RetrieveAPIView, DestroyAPIView, ListAPIView, UpdateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated

from education.models import Course, Lesson, Payment
from education.paginators import Pagination
from education.serializers import CourseSerializer, LessonSerializer, LessonDetailSerializer, CourseDetailSerializer, \
    LessonListSerializer, CourseListSerializer, PaymentListSerializer, PaymentSerializer, SubscriptionSerializer, \
    PaymentRetrieveSerializer, PaymentCreateSerializer
from education.tasks import send_mail_about_update
from users.permissions import IsBuyer, IsModerator


class CourseViewSet(viewsets.ModelViewSet):
    """ Viewset for course"""

    serializer_class = CourseDetailSerializer
    permission_classes = [IsAuthenticated]
    queryset = Course.objects.annotate(lessons_count=Count('lesson'))
    pagination_class = Pagination
    default_serializer = CourseSerializer
    serializers = {
        'list': CourseListSerializer,
        'retrieve': CourseDetailSerializer,
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.default_serializer)

    def update(self, request, *args, **kwargs):
        send_mail_about_update.delay(kwargs['pk'])
        return super().update(request, *args, **kwargs)


class LessonListView(ListAPIView):
    """ Lesson list API View """

    serializer_class = LessonListSerializer
    queryset = Lesson.objects.all()
    pagination_class = Pagination
    permission_classes = [IsAuthenticated]


class LessonDetailView(RetrieveAPIView):
    """ Lesson detail API View """

    serializer_class = LessonDetailSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsBuyer | IsModerator]


class LessonCreateView(CreateAPIView):
    """ Lesson create API View """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]


class LessonUpdateView(UpdateAPIView):
    """ Lesson update API View """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsBuyer | IsModerator]


class LessonDeleteView(DestroyAPIView):
    """ Lesson delete API View """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsBuyer, IsModerator]


class PaymentListView(ListAPIView):
    serializer_class = PaymentListSerializer
    queryset = Payment.objects.all()
    pagination_class = Pagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('paid_course', 'paid_lesson', 'payment_method')
    ordering_fields = ('payment_date',)
    permission_classes = [IsAuthenticated]


class PaymentDetailView(RetrieveAPIView):
    serializer_class = PaymentRetrieveSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated, IsModerator]


class PaymentCreateView(CreateAPIView):
    serializer_class = PaymentCreateSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated, IsBuyer, IsModerator]


class PaymentUpdateView(UpdateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated, IsModerator]


class PaymentDeleteView(DestroyAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated, IsModerator]


class SubscriptionCreateAPIView(CreateAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Lesson.objects.all()


class SubscriptionDestroyAPIView(DestroyAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Lesson.objects.all()
