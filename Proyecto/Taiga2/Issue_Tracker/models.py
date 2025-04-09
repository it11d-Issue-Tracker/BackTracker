from django.db import models
from django.contrib.auth.models import User

import uuid


class Issue(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('ready_for_test', 'Ready for Test'),
        ('closed', 'Closed'),
        ('archived', 'Archived'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    id_issue = models.AutoField(primary_key=True, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='new')
    priority_id = models.CharField(max_length=100, choices=PRIORITY_CHOICES, default='normal')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='created_by', to_field='id', related_name='issues')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_issues', db_column='assigned_to')
    deadline = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = 'issue'


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
    issue_id = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'attachments'


class Watcher(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='watchers')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchers')

    class Meta:
        db_table = 'watchers'
        unique_together = ('issue', 'user')

