from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission)
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Os usuários devem ter um nome de usuário')
        if email is None:
            raise TypeError('Os usuários devem ter um Email')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.is_verified = True
        user.save()
        return user

    def create_superuser(self, username, email, password=None):
        if password is None:
            raise TypeError('A senha não deve ser nenhuma')

        user = self.create_user(username=username, email=email,
                                password=password)
        user.is_superuser = True
        user.is_staff = True
        user.is_verified = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('Nome', max_length=255, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name='user_groups',
        related_query_name='user_group',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='user_permissions',
        related_query_name='user_permission',
    )


class CadastraoCartao(models.Model):
    numero = models.CharField(max_length=30)
    lote = models.CharField(max_length=8, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.numero


class LoteCartoes(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    nome = models.CharField(max_length=30, blank=True)
    data = models.CharField(max_length=8, blank=True)
    numero = models.CharField(max_length=8, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Lote de Cartões (Número: {self.numero})'
