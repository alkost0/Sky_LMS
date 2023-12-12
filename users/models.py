from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy

NULLABLE = {'blank': True, 'null': True}


class UserRoles(models.TextChoices):
    visitor = 'visitor', gettext_lazy('visitor')
    moderator = 'moderator', gettext_lazy('moderator')


class User(AbstractUser):
    username = None

    email = models.EmailField(max_length=250, unique=True, verbose_name='Адрес электронной почты')
    first_name = models.CharField(max_length=100, **NULLABLE, verbose_name='Имя')
    last_name = models.CharField(max_length=100, **NULLABLE, verbose_name='Фамилия')
    avatar = models.ImageField(upload_to='users/', **NULLABLE, verbose_name='Аватар')
    comment = models.TextField(**NULLABLE, verbose_name='Описание')
    is_active = models.BooleanField(default=True, verbose_name='Активность пользователя')
    role = models.CharField(max_length=20, **NULLABLE, choices=UserRoles.choices)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def str(self):
        return f'{self.first_name} {self.last_name}: {self.email}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
