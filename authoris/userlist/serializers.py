# userlist/serializers.py
from rest_framework import serializers
from .models import Users  # Импортируем вашу модель

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'  # Или укажите конкретные поля, например: ['id', 'username', 'email', 'first_name', 'last_name']