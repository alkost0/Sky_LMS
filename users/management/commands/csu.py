from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='tosha1703@mail.ru',
            first_name='test',
            last_name='test',
            role='moderator',
            is_superuser=True,
            is_staff=True,
            is_active=True

        )

        user.set_password('324214Kross!')
        user.save()
