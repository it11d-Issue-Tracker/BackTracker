from django.db import models
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
    created_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, db_column='created_by', to_field='id', related_name='issues')
    assigned_to = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='assigned_issues', db_column='assigned_to')
    deadline = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = 'issue'
