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

class Property(models.Model):
    DEAL_CHOICES = (
        ('sale', 'Продажа'),
        ('rent', 'Аренда'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    deal_type = models.CharField(max_length=10, choices=DEAL_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rooms = models.IntegerField(choices=[(i, f"{i} комн.") for i in range(1, 6)])
    area = models.FloatField()
    address = models.CharField(max_length=255)
    image1 = models.ImageField(upload_to='properties/', null=True, blank=True)
    image2 = models.ImageField(upload_to='properties/', null=True, blank=True)
    image3 = models.ImageField(upload_to='properties/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.deal_type})"




class Request(models.Model):
    property = models.ForeignKey('Property', on_delete=models.CASCADE, related_name='requests')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests')
    message = models.TextField(blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Заявка от {self.buyer.username} на {self.property.title}"


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