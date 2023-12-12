from django.urls import path
from rest_framework.routers import DefaultRouter
from education.apps import EducationConfig
from education.views import CourseViewSet, LessonListView, LessonDetailView, LessonCreateView, LessonUpdateView, \
    LessonDeleteView, PaymentListView, PaymentDetailView, PaymentUpdateView, PaymentDeleteView, \
    SubscriptionCreateAPIView, SubscriptionDestroyAPIView, PaymentCreateView

app_name = EducationConfig.name

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
                  path('lesson/', LessonListView.as_view(), name='lesson_list'),
                  path('lesson/<int:pk>/', LessonDetailView.as_view(), name='lesson_detail'),
                  path('lesson/update/<int:pk>/', LessonUpdateView.as_view(), name='lesson_update'),
                  path('lesson/create/', LessonCreateView.as_view(), name='lesson_create'),
                  path('lesson/delete/<int:pk>/', LessonDeleteView.as_view(), name='lesson_delete'),
                  path('payment/', PaymentListView.as_view(), name='payment_list'),
                  path('payment/<int:pk>/', PaymentDetailView.as_view(), name='payment_detail'),
                  path('payment/update/<int:pk>/', PaymentUpdateView.as_view(), name='payment_update'),
                  path('payment/create/', PaymentCreateView.as_view(), name='payment_create'),
                  path('payment/delete/<int:pk>/', PaymentDeleteView.as_view(), name='payment_delete'),
                  path('subscription/create/', SubscriptionCreateAPIView.as_view(), name='subscription_create'),
                  path('subscription/delete/<int:pk>/', SubscriptionDestroyAPIView.as_view(),
                       name='subscription_delete'),

              ] + router.urls
