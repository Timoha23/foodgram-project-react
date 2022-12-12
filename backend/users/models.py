from django.core import exceptions
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator


class User(AbstractUser):
    """Модель юзера"""
    username = models.CharField(
        'Логин',
        max_length=150,
        unique=True,
        help_text=('Required. 150 characters or fewer. Letters, '
                   'digits and @/./+/-/_ only.'),
        validators=[UnicodeUsernameValidator()],
        error_messages={
            'unique': ("A user with that username already exists."),
        },
    )
    email = models.EmailField(
        'Email адрес',
        max_length=254,
        unique=True,
    )

    first_name = models.CharField(
        'Имя',
        max_length=150,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
    )

    def __str__(self):
        return self.username


class Follow(models.Model):
    """Модель подписок"""
    author = models.ForeignKey(
        User,
        related_name='following',
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    user = models.ForeignKey(
        User,
        related_name='follower',
        on_delete=models.CASCADE,
        verbose_name='Подписчик'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Список подписок'
        constraints = [models.UniqueConstraint(fields=('user', 'author'),
                       name='Уникальные значения')]

    def clean(self):
        if self.author==self.user:
            raise exceptions.ValidationError(
                'Нельзя подписаться на самого себя'
            )

    def __str__(self):
        return f'А:{self.author.username} П:{self.user.username}'
