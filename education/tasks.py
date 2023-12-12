from datetime import timedelta
from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail
from config import settings
from education.models import Course, Lesson, Subscription
from users.models import User


@shared_task
def send_mail_about_update(course_id):
    course = Course.objects.get(id=course_id)
    subscriptions = Subscription.objects.filter(status=True, course=course)

    if course.updated_at > timezone.now() - timedelta(hours=4):
        for subscription in subscriptions:
            subject = f'Обновление курса {course.title}'
            message = f'Вышло обновление курса!!!'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [subscription.user.email]

            send_mail(subject,
                      message,
                      from_email,
                      recipient_list

                      )


@shared_task
def check_user():
    now_date = timezone.now()
    one_month_ago = now_date - timedelta(days=30)
    inactive_user = User.objects.filter(last_login__lt=one_month_ago)
    inactive_user.update(is_active=False)
