from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from education.models import Course, Lesson
from users.models import UserRoles, User
from rest_framework_simplejwt.tokens import RefreshToken


class LessonTestCase(APITestCase):

    def setUp(self):
        """Заполнение первичных данных"""

        self.user = User.objects.create(
            email='admin@mail.ru',
            is_staff=True,
            is_superuser=True,
            is_active=True,
            role=UserRoles.moderator,
        )
        self.user.set_password('qwerty123456')
        self.user.save()

        token = RefreshToken.for_user(self.user)
        self.access_token = str(token.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.course = Course.objects.create(
            title='OOP',
        )

        self.lesson = Lesson.objects.create(
            title='lesson 1',
            course_lesson=self.course
        )

    def test_get_list(self):
        """Тест получения списка уроков"""

        response = self.client.get(
            reverse('education:lesson_list')
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "pk": self.lesson.id,
                        "title": self.lesson.title,
                        "preview": self.lesson.preview,
                        "link": self.lesson.link,
                        "course_lesson": self.lesson.course_lesson.title,
                        "buyer": self.lesson.buyer
                    }
                ]
            }
        )

    def test_lesson_create(self):
        """Тест создания уроков"""

        response = self.client.post('/lesson/create/',
                                    {'title': 'test lesson', 'description': 'test lesson 1',
                                     'link': 'https://www.youtube.com/testlesson', 'buyer': 1})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_lesson_update(self):
        """ Тест обновления урока """
        self.client.force_authenticate(user=self.user)

        response = self.client.patch(reverse('education:lesson_update', args=[self.lesson.pk]),
                                     {'title': 'test lesson', 'description': 'test lesson 1',
                                      'link': 'https://www.youtube.com/testlesson', 'buyer': 1})

        self.assertEqual(
            response.status_code, status.HTTP_200_OK,
        )

        self.assertTrue(
            Lesson.objects.all().exists()
        )

    def test_lesson_delete(self):

        """ Тест удаления урока """

        self.client.force_authenticate(user=self.user)

        response = self.client.delete(reverse('education:lesson_delete', args=[self.lesson.pk]))

        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT,
        )
        self.assertFalse(
            Lesson.objects.all().exists(),
        )

    def tearDown(self) -> None:
        self.user.delete()
        self.course.delete()
        self.lesson.delete()


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        """Заполнение первичных данных"""

        self.user = User.objects.create(
            email='test@test.ru',
            is_staff=False,
            is_superuser=False,
            is_active=True,
            role=UserRoles.visitor,
        )
        self.user.set_password('qwerty123456')
        self.user.save()

        token = RefreshToken.for_user(self.user)
        self.access_token = str(token.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.course = Course.objects.create(
            title='OOP'
        )

        self.lesson = Lesson.objects.create(
            title='lesson 1',
            course_lesson=self.course
        )

    def test_create_subscription(self):
        response = self.client.post('/subscription/create/',
                                    {'course': self.course.id, 'user': self.user.id, 'status': False})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
