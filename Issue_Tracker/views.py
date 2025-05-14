
from django.contrib.sites import requests

from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib.auth.models import User
from .forms import *
from .utils import reorden


@login_required()

def issues_page(request):

        issues = Issue.objects.all().order_by('-created_at')
        users = User.objects.all().order_by('username')
        status = request.GET.get('status')
        priority = request.GET.get('priority')
        assigned_to = request.GET.get('assigned_to')
        created_by = request.GET.get('created_by')

        severity = request.GET.get('severity')
        type = request.GET.get('type')


        if status:
            issues = issues.filter(status=status)
        if priority:
            issues = issues.filter(priority_id=priority)
        if assigned_to:
            issues = issues.filter(assigned_to__id=assigned_to)
        if created_by:
            issues = issues.filter(created_by__id=created_by)
        if severity:
            issues = issues.filter(severity=severity)
        if type:
            issues = issues.filter(type=type)



        search_term = request.GET.get('search', '').strip()
        if search_term:
            issues = issues.filter(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term)
            )

        if request.method == 'POST':
            if 'bulk_titles' in request.POST:
                titles_text = request.POST.get("bulk_titles", "").strip()
                titles = [title.strip() for title in titles_text.split("\n") if title.strip()]

                if not titles:
                    messages.error(request, 'Debes ingresar al menos un título.')
                else:
                    issues = [
                        Issue(
                            title=title,
                            created_by=request.user,
                            deadline=now()
                        )
                        for title in titles
                    ]
                    Issue.objects.bulk_create(issues)
                    messages.success(request, f'Se crearon {len(issues)} issues.')
                    return redirect('custom-issues')
            else:
                form = IssueCreateForm(request.POST)
                if form.is_valid():
                    new_issue = form.save(commit=False)
                    new_issue.created_by = request.user
                    new_issue.save()
                    return redirect('custom-issues')
        else:
            form = IssueCreateForm()

        sort_by = request.GET.get('sort', '-updated_at')

        return render(request, 'issues_page.html', {
            'issues': issues.order_by(sort_by),
            'form': form,
            'users': users
        })


@login_required

def issue_detail(request, issue_id):
    issue = get_object_or_404(Issue, id_issue=issue_id)
    attachment_form = AttachmentForm()
    if request.method == 'POST':
        if 'delete_issue' in request.POST:
            issue.delete()
            messages.success(request, 'L\'issue s\'ha esborrat correctament.')
            return redirect('custom-issues')
        elif 'update_issue' in request.POST:
            issue_form = IssueUpdateForm(request.POST, instance=issue)
            if issue_form.is_valid():
                issue_form.save()
                return redirect('issue-detail', issue_id=issue_id)
        if 'file' in request.FILES:
            attachment_form = AttachmentForm(request.POST, request.FILES)
            if attachment_form.is_valid():
                attachment = attachment_form.save(commit=False)
                attachment.issue = issue
                attachment.save()
                print("✅ Archivo subido a:", attachment.file.url)
                return redirect('issue-detail', issue_id=issue_id)
        if 'delete_attachment' in request.POST:
            attachment_id = request.POST.get('attachment_id')
            attachment = Attachment.objects.get(attachment_id=attachment_id)
            attachment.delete()
            return redirect('issue-detail', issue_id=issue_id)

        elif 'action' in request.POST:
            action = request.POST.get('action')
            user_id = request.POST.get('user_id')
            user = get_object_or_404(User, id=user_id)

            if action == 'add':
                Watcher.objects.get_or_create(issue=issue, user=user)
            elif action == 'remove':
                Watcher.objects.filter(issue=issue, user=user).delete()

            return redirect('issue-detail', issue_id=issue_id)
        else:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.issue = issue
                comment.author = request.user
                comment.save()
                return redirect('issue-detail', issue_id=issue_id)
    else:
        issue_form = IssueUpdateForm(instance=issue)
        comment_form = CommentForm()

    watchers = Watcher.objects.filter(issue=issue)
    attachments = issue.attachments.all()
    users = User.objects.all()

    return render(request, 'issue_detail.html', {
        'issue': issue,
        'issue_form': issue_form,
        'comment_form': comment_form,
        'watchers': watchers,
        'users': users,
        'attachments': attachments,
        'attachment_form': attachment_form

    })

def custom_login_view(request):
    if request.user.is_authenticated:
        return redirect('custom-issues')
    return render(request, 'login.html')



def settings_view(request):
    statuses = Status.objects.all().order_by('orden')
    priorities = Priority.objects.all().order_by('orden')

    severities = Severity.objects.all().order_by('orden')
    types = Type.objects.all().order_by('orden')

    status_form = StatusForm()
    priority_form = PriorityForm()
    severity_form = SeverityForm()
    type_form = TypeForm()

    if request.method == 'POST':
        orden = request.POST.get('orden')
        orden = int(orden)
        if 'add_status' in request.POST:
            status_form = StatusForm(request.POST)
            try:
                reorden('Status', orden)
            except (TypeError, ValueError):
                print(f"orden no valido")
            if status_form.is_valid():
                status_form.save()
                return redirect('settings')

        elif 'add_priority' in request.POST:
            priority_form = PriorityForm(request.POST)
            try:
                reorden('Priority', orden)
            except (TypeError, ValueError):
                print(f"orden no valido")
            if priority_form.is_valid():
                priority_form.save()
                return redirect('settings')

        elif 'add_severity' in request.POST:
            severity_form = SeverityForm(request.POST)
            try:
                reorden('Severity', orden)
            except (TypeError, ValueError):
                print(f"orden no valido")
            if severity_form.is_valid():
                severity_form.save()
                return redirect('settings')
        elif 'add_type' in request.POST:
            type_form = TypeForm(request.POST)
            try:
                reorden('Type', orden)
            except (TypeError, ValueError):
                print(f"orden no valido")
            if type_form.is_valid():
                type_form.save()
                return redirect('settings')

    return render(request, 'settings.html', {
        'statuses': statuses,
        'priorities': priorities,

        'severities': severities,
        'types': types,

        'status_form': status_form,
        'priority_form': priority_form,
        'severity_form': severity_form,
        'type_form': type_form,
    })

def delete_status(request, status_id):
    Status.objects.filter(id=status_id).delete()
    return redirect('settings')

def delete_priority(request, priority_id):
    Priority.objects.filter(id=priority_id).delete()
    return redirect('settings')

def delete_severity(request, severity_id):
    Severity.objects.filter(id=severity_id).delete()
    return redirect('settings')

def delete_type(request, type_id):
    Type.objects.filter(id=type_id).delete()
    return redirect('settings')

@login_required
def profile_view_id(request, userid=None):
    if userid is not None:
        user = get_object_or_404(User, id=userid)
    else:
        user = request.user

    perfil = user.perfil

    active_tab = request.GET.get('tab', 'assigned')

    assigned_issues = Issue.objects.filter(assigned_to=user)
    watched_issues = Issue.objects.filter(watchers__user=user)
    user_comments = user.comments.select_related('issue')

    sort_by = request.GET.get('sort', '-updated_at')


    user_avatar_url = perfil.avatar_url or 'https://www.ole.com.ar/images/2024/10/28/58Ww_RX2d_400x400__1.jpg'

    context = {
        'user':user,
        'perfil': perfil,
        'full_name': f"{user.first_name} {user.last_name}",
        'user_avatar_url': user_avatar_url,
        'active_tab': active_tab,
        'assigned_count': assigned_issues.count(),
        'watched_count': watched_issues.count(),
        'comments_count': user_comments.count(),
    }
    if active_tab == 'assigned':
        context['issues'] = assigned_issues.order_by(sort_by)
    elif active_tab == 'watched':
        context['issues'] = watched_issues.order_by(sort_by)
    elif active_tab == 'comments':
        context['comments'] = user_comments.order_by('-created_at')
    return render(request, 'profile.html', context)

@login_required
def edit_bio(request):
    if request.method == 'POST':
        bio = request.POST.get('bio')
        avatar_url = request.POST.get('avatar_url')

        perfil = request.user.perfil
        if bio:
            perfil.bio = bio
        if avatar_url: # and is_valid_image_url(avatar_url):
            perfil.avatar_url = avatar_url
        perfil.save()

        return redirect('self-profile')


#requests hace petición a internet, no abusar mucho de ella, en un futuro cambiar
#comprueba si una url es válida y si es una imagen
def is_valid_image_url(url):
    try:
        response = requests.get(url, stream=True, timeout=5)
        content_type = response.headers.get('Content-Type', '')
        return response.status_code == 200 and 'image' in content_type
    except:
        return False

