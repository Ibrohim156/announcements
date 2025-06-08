from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('buyer', 'Покупатель'),
        ('seller', 'Продавец'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'
        ordering = ['user__username']

class Property(models.Model):
    DEAL_CHOICES = (
        ('sale', 'Продажа'),
        ('rent', 'Аренда'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='Пользователь', related_name='properties')
    title = models.CharField(max_length=255, verbose_name='Название', help_text='Введите название объекта недвижимости')
    description = models.TextField(verbose_name='Описание', help_text='Опишите объект недвижимости')
    deal_type = models.CharField(max_length=10, choices=DEAL_CHOICES, verbose_name='Тип сделки', help_text='Выберите тип сделки (Продажа или Аренда)')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена ($)', help_text='Укажите цену в долларах США')
    rooms = models.IntegerField(choices=[(i, f"{i} комн.") for i in range(1, 10)], verbose_name='Количество комнат',)
    area = models.FloatField(verbose_name='Площадь (м²)', help_text='Укажите площадь в квадратных метрах')
    address = models.CharField(max_length=255, verbose_name='Адрес', help_text='Введите полный адрес объекта недвижимости')
    image1 = models.ImageField(upload_to='properties/', null=True, blank=True, verbose_name='Изображение 1', help_text='Загрузите главное изображение объекта недвижимости')
    image2 = models.ImageField(upload_to='properties/', null=True, blank=True, verbose_name='Изображение 2', help_text='Загрузите дополнительное изображение объекта недвижимости')
    image3 = models.ImageField(upload_to='properties/', null=True, blank=True, verbose_name='Изображение 3', help_text='Загрузите еще одно дополнительное изображение объекта недвижимости')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', help_text='Дата и время создания объявления')
    
    def __str__(self):
        return f"{self.title} ({self.deal_type})"

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-created_at']


class Request(models.Model):
    property = models.ForeignKey('Property', on_delete=models.CASCADE, related_name='requests')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests')
    message = models.TextField(blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Заявка от {self.buyer.username} на {self.property.title}"

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']

class LeaveRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, verbose_name='Объявление')
    reason = models.TextField(verbose_name='Причина удаления', blank=True, null=True)
    status_choices = [
        ('pending', 'Ожидает рассмотрения'),
        ('approved', 'Одобрено'),
        ('rejected', 'Отклонено'),
    ]
    status = models.CharField(max_length=10, choices=status_choices, default='pending', verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата подачи заявки')

    def __str__(self):
        return f'Заявка на удаление объявления {self.property} от {self.user.username}'
    
    class Meta:
        verbose_name = 'Заявка на удаление объявления'
        verbose_name_plural = 'Заявки на удаление объявлений'
        ordering = ['-created_at']