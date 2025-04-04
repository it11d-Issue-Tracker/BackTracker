from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Issue

User = get_user_model()

class IssueSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(
        read_only=True,  # No se permite modificar manualmente
        default=serializers.CurrentUserDefault()  # Auto-asigna el usuario actual
    )
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,  # Para permitir null (opcional)
        allow_null=True,
    )

    class Meta:
        model = Issue
        fields = '__all__'

        extra_kwargs = {
            'id_issue': {'read_only': True},  # Auto-generado
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True}
        }

