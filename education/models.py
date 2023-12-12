from django.db import models

from users.models import NULLABLE, User


class Course(models.Model):
    title = models.CharField(max_length=100, verbose_name='название')
    preview = models.ImageField(upload_to='education/', **NULLABLE, verbose_name='превью')
    description = models.TextField(**NULLABLE, verbose_name='описание')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE, verbose_name='Покупатель курса')
    price = models.IntegerField(default=10000, verbose_name='стоимость курса')
    updated_at = models.DateTimeField(verbose_name='время обновления', **NULLABLE)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=100, verbose_name='название')
    description = models.TextField(**NULLABLE, verbose_name='описание')
    preview = models.ImageField(upload_to='education/', **NULLABLE, verbose_name='превью')
    link = models.URLField(verbose_name='ссылка на видео')
    course_lesson = models.ForeignKey(Course, **NULLABLE, on_delete=models.CASCADE, verbose_name='Урок курса')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE, verbose_name='Покупатель урока')

    def __str__(self):
        return f'{self.title}: {self.link}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Payment(models.Model):
    CARD = "Безналичный"
    CASH = "Наличные"

    PAYMENT_METHOD = [
        (CARD, "Безналичный"),
        (CASH, "Наличные"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    payment_date = models.DateField(**NULLABLE, verbose_name='Дата оплаты')
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, **NULLABLE, verbose_name='Оплаченный курс')
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, **NULLABLE, verbose_name='Оплаченный урок')
    payment_amount = models.PositiveIntegerField(verbose_name='Сумма оплаты')
    payment_method = models.CharField(choices=PAYMENT_METHOD, default=CARD, max_length=100, **NULLABLE,
                                      verbose_name='Способ оплаты')
    is_paid = models.BooleanField(default=False, verbose_name="оплачено")
    payment_intent_id = models.CharField(default='NULL', max_length=100, verbose_name="id_платежа")

    def __str__(self):
        return f'{self.user}: {self.paid_course} - {self.payment_amount}'

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'


class Subscription(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    status = models.BooleanField(default=True, verbose_name='Статус подписки')

    def __str__(self):
        return f'{self.user} - {self.course}'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
