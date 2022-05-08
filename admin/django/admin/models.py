import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MinLengthValidator, MaxValueValidator


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Delivery(models.TextChoices):
    EMAIL = 'email', _('Почта')
    SMS = 'sms', _('СМС')
    TABOO = 'taboo', _('Отписка')
    WEBSOCKET = 'websocket', _('Веб-сокет')


class NotificationStatuses(models.TextChoices):
    CANCEL = 'cancel', _('Отмена')
    FAIL = 'fail', _('Неудача')
    PLAN = 'plan', _('План')
    SUCCESS = 'success', _('Удача')
    QUEUE = 'queue', _('Очередь')


class Template(models.TextChoices):
    WELCOME = 'welcome', _('Welcome-письмо')
    TIP = 'tip', _('Новый фильм')
    STATISTICS = 'statistics', _('Статистика')
    SELECTION = 'selection', _('Рекомендация')
    CLEAN = 'clean', _('От команды')
    BOOKMARKS = 'bookmarks', _('Новая серия')


class Frequency(models.TextChoices):
    MON = 'mon', _('Понедельник')
    TUE = 'tue', _('Вторник')
    WED = 'wed', _('Среда')
    THU = 'thu', _('Четверг')
    FRI = 'fri', _('Пятница')
    SAT = 'sat', _('Суббота')
    SUN = 'sun', _('Воскресенье')
    MONTH = 'month', _('Месяц')
    DAILY = 'daily', _('Ежедневно')


class Priority(models.TextChoices):
    HIGH = 'high', 'Немедленно'
    MEDIUM = 'medium', 'В порядке очереди'
    LOW = 'low', 'Завтра'


class Movie(TimeStampedModel):
    id = models.UUIDField(primary_key=True, editable=False)
    title = models.CharField(_('Название'), max_length=255)
    description = models.TextField(_('Описание'), blank=True)
    rating = models.FloatField(_('Рейтинг'), validators=[MinValueValidator(0), MaxValueValidator(10)], default=0.0)
    genres = models.TextField(_('Жанры'), blank=True)

    class Meta:
        verbose_name = _('Фильм')
        verbose_name_plural = _('Фильмы')
        db_table = '"content"."movie"'
        managed = False

    def __str__(self):
        return self.title


class Recipient(TimeStampedModel):
    id = models.UUIDField(primary_key=True, editable=False)
    login = models.CharField(_('Login'), max_length=100, unique=True)
    first_name = models.CharField(_('Имя'), max_length=100)
    second_name = models.CharField(_('Отчество'), max_length=100)
    last_name = models.CharField(_('Фамилия'), max_length=100)
    title = models.CharField(_('Обращение'), max_length=100)
    email = models.EmailField(_('Email'), max_length=255, unique=True)
    birthdate = models.DateField(_('День рождения'), blank=True, null=True)
    status = models.BooleanField(_('Confirmed'), default=False)
    likes_count = models.IntegerField(_('Количество лайков'), default=0)
    likes_sum = models.IntegerField(_('Сумма по лайкам'), default=0)
    ego = models.FloatField(_('Эго'), validators=[MinValueValidator(0), MaxValueValidator(10)], default=0.0)
    bookmarks = models.ManyToManyField(Movie, through='Bookmarks', name='bookmarks')
    delivery = models.CharField(_('Тип'), max_length=20, choices=Delivery.choices)
    redirect_url = models.CharField(_('Редирект'), default='http://127.0.0.1')

    class Meta:
        verbose_name = _('Подписчик')
        verbose_name_plural = _('Подписчики')
        db_table = '"content"."recipient"'
        managed = False

    def __str__(self):
        return self.title


class Bookmarks(TimeStampedModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    recipient = models.ForeignKey('Recipient', on_delete=models.CASCADE, to_field='id', db_column='recipient_id')
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE, to_field='id', db_column='movie_id')
    series = models.IntegerField(_('Серия'), default=1)

    class Meta:
        indexes = [models.Index(fields=['recipient_id', 'movie_id'], name='bookmarks')]
        verbose_name = _('Закладка')
        verbose_name_plural = _('Закладки')
        db_table = '"content"."bookmarks"'
        managed = False

        def __str__(self):
            return str(f'{self.recipient} - {self.movie}')


class Notification(TimeStampedModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    recipient = models.ManyToManyField(Movie, through='Recipient', name='recipient')
    status = models.CharField(_('Статус'), max_length=20, choices=NotificationStatuses.choices)
    subject = models.CharField(_('Тема письма'), blank=False, max_length=255)
    body = models.TextField(_('Письмо'), blank=False)
    priority = models.CharField(_('Приоритет'), max_length=20, choices=Priority.choices)

    class Meta:
        verbose_name = _('Уведомление')
        verbose_name_plural = _('Уведомления')
        db_table = '"content"."notification"'
        managed = False

    def __str__(self):
        return self.title


class NotificationRecipient(TimeStampedModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    recipient = models.ForeignKey('Recipient', on_delete=models.CASCADE, to_field='id', db_column='recipient_id')
    notification = models.ForeignKey(
        'Notification',
        on_delete=models.CASCADE,
        to_field='id',
        db_column='notification_id'
    )

    class Meta:
        indexes = [models.Index(fields=['recipient_id', 'notification_id'], name='notification_recipient')]
        verbose_name = _('Уведомление получателя')
        verbose_name_plural = _('Уведомления получателей')
        db_table = '"content"."notification_recipient"'
        managed = False

        def __str__(self):
            return str(f'{self.recipient} - {self.notification}')


class Scheduler(TimeStampedModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    template = models.CharField(_('Шаблон'), max_length=20, choices=Template.choices)
    recipient = models.ForeignKey('Recipient', on_delete=models.CASCADE, to_field='id', db_column='recipient_id')
    when = models.CharField(_('Периодичность'), max_length=20, choices=Frequency.choices)
    priority = models.CharField(_('Приоритет'), max_length=20, choices=Priority.choices)

    class Meta:
        verbose_name = _('Шаблон')
        verbose_name_plural = _('Шаблоны')
        db_table = '"content"."scheduler"'
        managed = False

    def __str__(self):
        return self.title
