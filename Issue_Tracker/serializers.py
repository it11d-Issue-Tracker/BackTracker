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
        fields = ['text', 'created_at', 'author', 'Username']

class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = '__all__'

class WatcherSerializer(serializers.ModelSerializer):
    Username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Watcher
        fields = ['user', 'Username']



class IssueSerializer(serializers.ModelSerializer):


    created_by = serializers.CharField(source='created_by.username', read_only=True)
    assigned_to = serializers.CharField(source='assigned_to.username', read_only=True)

    status = serializers.CharField(source='status.id', read_only=True)
    priority = serializers.CharField(source='priority.id', read_only=True)
    severity = serializers.CharField(source='severity.id', read_only=True)
    type = serializers.CharField(source='type.id', read_only=True)


    class Meta:
        model = Issue
        fields = [
            'title',
            'description',
            'status',
            'priority',
            'assigned_to',
            'deadline',
            'created_by',
            'created_at',
            'updated_at',

            'severity',
            'type',


        ]

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






