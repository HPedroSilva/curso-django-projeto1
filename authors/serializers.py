from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
