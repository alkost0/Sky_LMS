import random
from django.core.management.base import BaseCommand
from users.models import User
from datetime import date
from education.models import Course, Lesson, Payment


class Command(BaseCommand):
    help = 'Create sample payment'

    def handle(self, *args, **options):
        users = User.objects.all()
        courses = Course.objects.all()
        lessons = Lesson.objects.all()
        payment_methods = ['Credit card', 'PayPal', 'Bank transfer']

        payments = []

        for i in range(3):
            user = random.choice(users)
            course = random.choice(courses)
            lesson = random.choice(lessons)
            payment_date = date.today()
            payment_amount = random.randint(1000, 100000)
            payment_method = random.choice(payment_methods)

            payment = Payment(
                user=user,
                payment_date=payment_date,
                paid_course=course,
                paid_lesson=lesson,
                payment_amount=payment_amount,
                payment_method=payment_method
            )

            payments.append(payment)

        Payment.objects.bulk_create(payments)

        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(payments)} payments'))
