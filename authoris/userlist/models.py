from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager, make_password


class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    class Meta:
        verbose_name = 'Персона'
        verbose_name_plural = 'Персоны'

class UserManager(BaseUserManager):
    """
    Кастомный менеджер пользователей, который использует email вместо username.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Создает и сохраняет пользователя с указанным email и паролем.
        """
        if not email:
            raise ValueError(_('Email должен быть указан'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Создает и сохраняет суперпользователя с указанным email и паролем.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Суперпользователь должен иметь is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Суперпользователь должен иметь is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

class User_employe(AbstractBaseUser, PermissionsMixin):
    """
    Кастомная модель пользователя, использующая email вместо username.
    """
    email = models.EmailField(_('Email'), unique=True)
    username = models.CharField(_('Имя пользователя'), max_length=30, blank=True)
    password_hash = models.CharField(_('Хэш пароля'), max_length=128, default=make_password(''))
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)
    is_active = models.BooleanField(_('Активный'), default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

    def __str__(self):
        return self.email

    def set_password(self, raw_password):
        self.password_hash = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password_hash)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'