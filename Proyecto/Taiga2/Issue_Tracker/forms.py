from django import forms
from Issue_Tracker.models import Comment
from Issue_Tracker.models import Issue

from django.contrib.auth import get_user_model
User = get_user_model()


class IssueCreateForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['title', 'description', 'status', 'priority_id', 'assigned_to', 'deadline']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Títol'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripció'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'priority_id': forms.Select(attrs={'class': 'form-select'}),
            'assigned_to': forms.Select(attrs={'class': 'form-select'}),
            'deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'title': 'Títol',
            'description': 'Descripció',
            'status': 'Estat',
            'priority_id': 'Prioritat',
            'assigned_to': 'Assignat a',
            'deadline': 'Data límit',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Escriu un comentari...'}),
        }
        labels = {
            'text': 'Comentari',
        }





class IssueUpdateForm(forms.ModelForm):
    assigned_to = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Assignat a"
    )
    status = forms.ChoiceField(
        choices=Issue.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Estat"
    )

    class Meta:
        model = Issue
        fields = ['assigned_to', 'status']