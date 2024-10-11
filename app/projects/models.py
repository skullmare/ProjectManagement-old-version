from django.db import models
from user.models import CustomUser

class Project(models.Model):
    name = models.CharField(max_length=100)
    client = models.CharField(max_length=150, blank=True, null=True)
    curator = models.CharField(max_length=150, blank=True, null=True)
    purpose = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name


class ProjectMembership(models.Model):
    ROLE_CHOICES = [
        ('leader', 'Руководитель'),
        ('participant', 'Участник'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.CharField(max_length=12, choices=ROLE_CHOICES)

    class Meta:
        unique_together = ('user', 'project')

    def __str__(self):
        return f'{self.user} - {self.project} - {self.role}'
    


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
