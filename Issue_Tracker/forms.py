from django import forms
from Issue_Tracker.models import *


from django.contrib.auth import get_user_model
User = get_user_model()


class IssueCreateForm(forms.ModelForm):
    assigned_to = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Assignat a"
    )
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Estat"
    )
    priority = forms.ModelChoiceField(
        queryset=Priority.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Prioritat"
    )

    severity = forms.ModelChoiceField(
        queryset=Severity.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Severitat"
    )
    type = forms.ModelChoiceField(
        queryset=Type.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Tipus"
    )

    class Meta:
        model = Issue
        fields = ['title', 'description', 'status', 'priority', 'assigned_to', 'deadline', 'severity', 'type']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Títol'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripció'}),
            'deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'title': 'Títol',
            'description': 'Descripció',
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
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Estat"
    )
    priority = forms.ModelChoiceField(
        queryset=Priority.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Prioritat"
    )

    severity = forms.ModelChoiceField(
        queryset=Severity.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Severitat"
    )
    type = forms.ModelChoiceField(
        queryset=Type.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Tipus"
    )

    class Meta:
        model = Issue
        fields = ['assigned_to', 'status', 'priority', 'severity', 'type', 'deadline']



class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ['file']

class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['id']
        widgets = {
            'id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom del status'}),
        }
        labels = {
            'id': 'Status',
        }


class PriorityForm(forms.ModelForm):
    class Meta:
        model = Priority
        fields = ['id']
        widgets = {
            'id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de la prioritat'}),
        }
        labels = {
            'id': 'Prioritat',

        }

class SeverityForm(forms.ModelForm):
    class Meta:
        model = Severity
        fields = ['id']
        widgets = {
            'id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de la severitat'}),
        }
        labels = {
            'id': 'Severitat',
        }

class TypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = ['id']
        widgets = {
            'id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom del tipus'}),
        }
        labels = {
            'id': 'Tipus',

        }