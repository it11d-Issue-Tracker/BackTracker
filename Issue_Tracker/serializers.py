from django.db import IntegrityError
from rest_framework import serializers
from django.contrib.auth import get_user_model
from Issue_Tracker.models import *

User = get_user_model()

class CommentSerializer(serializers.ModelSerializer):
    #Created_at = serializers.DateTimeField(format="%d %b %Y %H:%M")
    Username = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id','issue','text', 'created_at', 'author', 'Username']
        read_only_fields = ['created_at', 'author', 'Username']

class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = '__all__'

class WatcherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Watcher
        fields = ['id', 'issue', 'user']
        read_only_fields = ['user', 'Username']

class IssueSerializer(serializers.ModelSerializer):
    class Meta:
            model = Issue
            fields = '__all__'

    def create(self, validated_data):
        try:
            issue = Issue.objects.create(**validated_data)
            return issue
        except IntegrityError as error:
            raise serializers.ValidationError({"error": str(error)})


class IssueDetailSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='author.username', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    status = serializers.CharField(source='status.id', read_only=True)
    priority = serializers.CharField(source='priority.id', read_only=True)
    severity = serializers.CharField(source='severity.id', read_only=True)
    type = serializers.CharField(source='type.id', read_only=True)



    class Meta:
        model = Issue
        fields = '__all__'




class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'

class PrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Priority
        fields = '__all__'

class SeveritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Severity
        fields = '__all__'

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'
