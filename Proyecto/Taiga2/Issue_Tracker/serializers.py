from django.db import IntegrityError
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Issue

User = get_user_model()

class BulkInsertSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        result = [self.child.create(attrs) for attrs in validated_data]
        try:
            self.child.Meta.model.objects.bulk_create(result)
        except IntegrityError as e:
            raise serializers.ValidationError(e)
        return result
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

    status = serializers.ChoiceField(choices=Issue.STATUS_CHOICES)
    priority_id = serializers.ChoiceField(choices=Issue.PRIORITY_CHOICES)

    class Meta:
        model = Issue
        fields = [
            'title',
            'description',
            'status',
            'priority_id',
            'assigned_to',
            'deadline',
            'created_by',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at']
        list_serializer_class = BulkInsertSerializer

        def validate_assigned_to(self, value):
            if value and not value.is_active:
                raise serializers.ValidationError('User is not active')
            return value

