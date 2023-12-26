import datetime
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, FileExtensionValidator
from django.db import models
from django.dispatch import Signal
from django.urls import reverse
from django.utils import timezone
from django.utils.crypto import get_random_string


class Order(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)



class Product(models.Model):
    product_name = models.CharField(max_length=200, verbose_name='Название товара/услуги')
    description_product = models.CharField(max_length=3000, verbose_name='Описание')
    pub_date = models.DateTimeField('date published')
    product_img = models.ImageField(verbose_name='Картинка', upload_to='products/', blank=True, null=True,
                            validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])])
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.product_name

    def get_absolute_url(self):
        return reverse('detail', args=[str(self.id)])

class User(AbstractUser):
    username = models.CharField(max_length=200, verbose_name='Логин', unique=True, blank=False)
    avatar = models.ImageField(upload_to='avatars/', verbose_name='Аватар', blank=False,
                               null=True,
                               validators=[FileExtensionValidator(
                                   allowed_extensions=['png', 'jpg', 'jpeg'])])
    password = models.CharField(max_length=200, verbose_name='Пароль', blank=False)

    USERNAME_FIELD = 'username'

    def __str__(self):
        return str(self.username)


user_registrated = Signal()
