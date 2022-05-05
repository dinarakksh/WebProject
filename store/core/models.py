import os
from tabnanny import verbose
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError


ALLOWED_EXTENSIONS = ['.jpg', '.png']

def validate_extension(value):
    split_ext = os.path.splitext(value.name)
    if len(split_ext) > 1:
        ext = split_ext[1]
        if ext.lower() not in ALLOWED_EXTENSIONS:
            raise ValidationError(f'not allowed file, valid extensions: {ALLOWED_EXTENSIONS}')


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название категории")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self) -> str:
        return f'{self.name}'


class Product(models.Model):
    name = models.CharField(max_length=300, verbose_name="Название продукта")
    price = models.FloatField(verbose_name="Цена")
    in_stock = models.BooleanField(default=False, verbose_name='Есть в наличии?')
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    category = models.ForeignKey(Category, 
                                on_delete=models.DO_NOTHING,
                                related_name="products",
                                verbose_name="Категория",
                                blank=True,
                                null=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return f'{self.name}'


class ProductImage(models.Model):
    src = models.ImageField(upload_to='images/',
                            validators=[validate_extension, ])
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name="images",
                                verbose_name="Продукт",
                                blank=True,
                                null=True)

    class Meta:
        verbose_name = "Картинка продукта"
        verbose_name_plural = "Картинки продукта"

    def __str__(self):
        return f'Картинка {self.product.name}'


class UserPersonalCart(models.Model):
    owner = models.OneToOneField(User,
                                 on_delete=models.CASCADE,
                                 verbose_name='Владелец корзины',
                                 related_name='cart')
                                
    class Meta:
        verbose_name = 'Корзина пользователя'

    @property
    def total_price(self):
        total = 0
        for item in self.items.all():
            total += item.total_price
        return total
    
    @receiver(post_save, sender=User)
    def create_user_personal_cart(sender, instance, created, **kwargs):
        if created:
            UserPersonalCart.objects.create(owner=instance)


class CartItem(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name='carts',
                                verbose_name='Продукт')
    quantity = models.PositiveIntegerField(verbose_name='количество товара')
    cart = models.ForeignKey(UserPersonalCart,
                             on_delete=models.CASCADE,
                             related_name='items',
                             verbose_name='Корзина')

    class Meta:
        verbose_name = 'Запись корзины'
        verbose_name_plural = 'Записи корзины'

    @property
    def total_price(self):
        return self.product.price * self.quantity
