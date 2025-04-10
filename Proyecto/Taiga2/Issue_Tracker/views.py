from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib.auth.models import User
from .forms import CommentForm, IssueUpdateForm, IssueCreateForm



def issues_page(request):

        issues = Issue.objects.all().order_by('-created_at')
        users = User.objects.all().order_by('username')
        status = request.GET.get('status')
        priority_id = request.GET.get('priority_id')
        assigned_to = request.GET.get('assigned_to')
        created_by = request.GET.get('created_by')

        if status:
            issues = issues.filter(status=status)
        if priority_id:
            issues = issues.filter(priority_id=priority_id)
        if assigned_to:
            issues = issues.filter(assigned_to__id=assigned_to)
        if created_by:
            issues = issues.filter(created_by__id=created_by)


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
                            status="new",
                            priority_id="normal",
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

        return render(request, 'issues_page.html', {
            'issues': issues,
            'form': form,
            'users': users
        })


def issue_detail(request, issue_id):
    issue = get_object_or_404(Issue, id_issue=issue_id)

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
    users = User.objects.all()

    return render(request, 'issue_detail.html', {
        'issue': issue,
        'issue_form': issue_form,
        'comment_form': comment_form,
        'watchers': watchers,
        'users': users
    })

def custom_login_view(request):
    if request.user.is_authenticated:
        return redirect('custom-issues')
    return render(request, 'login.html')