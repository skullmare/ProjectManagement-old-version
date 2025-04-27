from django.db import models
from django.contrib.auth import get_user_model  # Импортируем функцию для получения модели пользователя

# Получаем модель пользователя
User = get_user_model()

class Project(models.Model):
    name = models.CharField(max_length=100)
    client = models.CharField(max_length=150, blank=True, null=True)
    curator = models.CharField(max_length=150, blank=True, null=True)
    purpose = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    members = models.ManyToManyField(
        User,  # Используем непосредственно модель, а не строку
        through='ProjectMembership',
        through_fields=('project', 'user'),
        related_name='projects'
    )

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"

    def __str__(self):
        return self.name


class ProjectMembership(models.Model):
    ROLE_CHOICES = [
        ('leader', 'Руководитель'),
        ('participant', 'Участник'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Используем модель User
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.CharField(max_length=12, choices=ROLE_CHOICES)
    date_added = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата назначения"
    )

    class Meta:
        unique_together = ('user', 'project')
        verbose_name = "Доступ"
        verbose_name_plural = "Доступы"

    def __str__(self):
        return f'{self.user} - {self.project} - {self.role}'
    


class Budget(models.Model):
    project = models.ForeignKey(Project, related_name='budgets', on_delete=models.CASCADE)
    year = models.PositiveIntegerField()  # Поле для года
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Поле для бюджета

    class Meta:
        unique_together = ('project', 'year')  # Уникальное ограничение на сочетание проекта и года
        verbose_name = "Бюджет"  # единственное число
        verbose_name_plural = "Бюджеты"  # множественное число

    def __str__(self):
        return f"{self.project.name} - {self.year}: {self.amount}"


class Risk(models.Model):
    project = models.ForeignKey(Project, related_name='risks', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  # Название риска
    description = models.TextField()  # Описание риска
    class Meta:
        verbose_name = "Риск"  # единственное число
        verbose_name_plural = "Риски"  # множественное число
    def __str__(self):
        return self.name


class Result(models.Model):
    project = models.ForeignKey(Project, related_name='results', on_delete=models.CASCADE)
    text = models.TextField()  # Результат в виде текста
    class Meta:
        verbose_name = "Результат"  # единственное число
        verbose_name_plural = "Результаты"  # множественное число
    def __str__(self):
        return f"Result for {self.project.name}"


class Task(models.Model):
    project = models.ForeignKey(Project, related_name='tasks', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(
        blank=True, 
        null=True,
        verbose_name="Описание"
    )
    start_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Дата начала"
    )
    end_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Дата окончания"
    )
    status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ], default='pending')
    assigned_users = models.ManyToManyField(
        User,
        related_name='tasks',
        blank=True,
        verbose_name="Назначенные пользователи"
    )
    class Meta:
        verbose_name = "Задача"  # единственное число
        verbose_name_plural = "Задачи"  # множественное число
    def __str__(self):
        return self.name
