from rest_framework import serializers
from .models import Project, Budget, Risk, Result, Task
from user.models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name']

class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ['id', 'year', 'amount']

class RiskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Risk
        fields = ['id', 'name', 'description']

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ['id', 'text']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'status', 'start_date', 'end_date']

class LeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['leaders']

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['participants']

class ProjectSerializer(serializers.ModelSerializer):
    leaders = CustomUserSerializer(many=True, required=False)
    participants = CustomUserSerializer(many=True, required=False)
    budgets = BudgetSerializer(many=True, required=False)
    risks = RiskSerializer(many=True, required=False)
    results = ResultSerializer(many=True, required=False)
    tasks = TaskSerializer(many=True, required=False)

    class Meta:
        model = Project
        fields = ['id', 'name', 'client', 'curator', 'leaders', 'participants', 'purpose', 'description', 'start_date', 'end_date', 'budgets', 'risks', 'results', 'tasks']
