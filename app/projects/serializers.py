from rest_framework import serializers
from .models import Project
from user.models import CustomUser

class ProjectSerializer(serializers.ModelSerializer):
    leaders = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        many=True,
        required=False
    )
    participants = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        many=True,
        required=False
    )
    class Meta:
        model = Project
        fields = ['id', 'name', 'leaders', 'participants']