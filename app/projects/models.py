from django.db import models
from user.models import CustomUser

class Project(models.Model):
    name = models.CharField(max_length=100)
    client = models.CharField(max_length=150)  # Поле для заказчика
    curator = models.CharField(max_length=150)  # Поле для куратора
    leaders = models.ManyToManyField(CustomUser, related_name='led_projects')
    participants = models.ManyToManyField(CustomUser, related_name='participated_projects')
    purpose = models.TextField()
    description = models.TextField()
    start_date = models.DateField()  # Поле для даты начала
    end_date = models.DateField()    # Поле для даты окончания

    def __str__(self):
        return self.name

class Budget(models.Model):
    project = models.ForeignKey(Project, related_name='budgets', on_delete=models.CASCADE)
    year = models.PositiveIntegerField()  # Поле для года
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Поле для бюджета

    class Meta:
        unique_together = ('project', 'year')  # Уникальное ограничение на сочетание проекта и года

    def __str__(self):
        return f"{self.project.name} - {self.year}: {self.amount}"

class Risk(models.Model):
    project = models.ForeignKey(Project, related_name='risks', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  # Название риска
    description = models.TextField()  # Описание риска

    def __str__(self):
        return self.name

class Result(models.Model):
    project = models.ForeignKey(Project, related_name='results', on_delete=models.CASCADE)
    text = models.TextField()  # Результат в виде текста

    def __str__(self):
        return f"Result for {self.project.name}"

class Task(models.Model):
    project = models.ForeignKey(Project, related_name='tasks', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()  # Дата начала задачи
    end_date = models.DateField()    # Дата окончания задачи
    status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ], default='pending')

    def __str__(self):
        return self.name
