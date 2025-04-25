from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

class Recipe(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    steps = models.TextField(verbose_name='Шаги приготовления')
    preparation_time = models.PositiveIntegerField(verbose_name='Время приготовления (в минутах)')
    image = models.ImageField(upload_to='recipes/', null=True, blank=True, verbose_name='Изображение')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    ingredients = models.TextField(verbose_name='Ингредиенты', blank=True)
    categories = models.ManyToManyField(Category, related_name='recipes', blank=True, verbose_name='Категории')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-created_at']

    def __str__(self):
        return self.title