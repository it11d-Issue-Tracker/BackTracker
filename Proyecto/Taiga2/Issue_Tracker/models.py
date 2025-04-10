from django.db import models
from django.contrib.auth.models import User

import uuid


class Status(models.Model):
    id = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.id

    class Meta:
        db_table = 'status'


class Priority(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    orden = models.PositiveIntegerField(unique=True)
    color = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.id

    class Meta:
        db_table = 'priority'
        ordering = ['orden']




class Issue(models.Model):
        id_issue = models.AutoField(primary_key=True, editable=False)
        title = models.CharField(max_length=200)
        description = models.TextField()
        status = models.ForeignKey('Status', on_delete=models.SET_NULL, null=True, related_name='issues')
        priority = models.ForeignKey('Priority', on_delete=models.SET_NULL, null=True, related_name='issues')
        created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='created_by', to_field='id',
                                       related_name='issues')
        assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_issues',
                                        db_column='assigned_to')
        deadline = models.DateField(null=True, blank=True)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

        class Meta:
            db_table = 'issue'

        @property
        def priority_color(self):
            return self.priority.color if self.priority else 'gray'


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comments'
        ordering = ['-created_at']

class Attachment(models.Model):
    attachment_id = models.AutoField(primary_key=True)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name

    class Meta:
        db_table = 'attachments'


class Watcher(models.Model):
    id = models.AutoField(primary_key=True)
    issue = models.ForeignKey('Issue', on_delete=models.CASCADE, db_column='issue_id', related_name='watchers')
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id', related_name='watching_issues')

    class Meta:
        db_table = 'watchers'
        unique_together = ('issue', 'user')
        indexes = [
            models.Index(fields=['issue'], name='watchers_issue_i_a06e44_idx'),
            models.Index(fields=['user'], name='watchers_user_id_1d8812_idx'),
        ]

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    avatar_url = models.URLField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    username = models.CharField(max_length=100, unique=True)

