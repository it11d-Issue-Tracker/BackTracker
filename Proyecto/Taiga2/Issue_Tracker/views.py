from django.urls import reverse
from rest_framework import viewsets, status
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib import messages
from .models import Issue
from .models import User
from .models import Comment
from django.shortcuts import render, redirect, get_object_or_404
from .serializers import IssueSerializer
from .serializers import IssueDetailSerializer
from .serializers import CommentSerializer

from django.utils.timezone import now
from django_filters.rest_framework import DjangoFilterBackend
from Issue_Tracker.models import Comment
from Issue_Tracker.forms import CommentForm, IssueUpdateForm, IssueCreateForm


class IssueViewSet(viewsets.ModelViewSet):
    renderer_classes = [viewsets.ModelViewSet.renderer_classes[0], viewsets.ModelViewSet.renderer_classes[1]]
    queryset = Issue.objects.all().order_by('created_at')
    serializer_class = IssueSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsAuthenticated]
    filterset_fields = ['status', 'priority_id', 'assigned_to', 'created_by']
    search_fields = ['title', 'description']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


    @action(detail=False, methods=['get', 'post'], url_name= 'bulk_create', url_path='bulk_create')
    def bulk_create(self, request, *args, **kwargs):
        if request.method == 'GET':
            return render(request, 'bulk_create.html')
        titles_text = request.data.get("titles", "").strip()
        titles = [title.strip() for title in titles_text.split("\n") if title.strip()]

        if not titles:
            messages.error(request, 'Debes ingresar al menos un título.')
            return render(request, 'bulk_create.html', {"error": "Debes ingresar al menos un título"}, status=400)
        issues = [
            Issue(
                title=title,
                description=None,
                status="new",
                priority_id="normal",
                created_by=request.user,
                assigned_to=None,
                deadline=now()
            )
            for title in titles
        ]

        Issue.objects.bulk_create(issues)


        # Falta hacer redirect a api/issues
        return Response(
            {"message": f"{len(issues)} issues creados correctamente"},
            status=status.HTTP_201_CREATED
        )



    def perform_bulk_create(self, serializer):
            return serializer.save()

    @action(detail=False, methods=['get', 'post'], url_path='search', url_name='search')
    def search_issues(self, request):
        if request.method == 'GET':
            return render(request, 'search.html')

        search_term = request.POST.get('search_term').strip()

        if not search_term:
            return render(request, 'search.html',
                          {'error': 'Debes ingresar un término de búsqueda'})
        issues = Issue.objects.filter(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term)
        ).order_by('-created_at')

        return render(request, 'search_results.html',
                      {'issues': issues, 'search_term':search_term})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.created_by != self.request.user:
            return Response(
                {"error: You are not allowed to delete this issue"},
                status=status.HTTP_403_FORBIDDEN
            )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filtro por título
        title = self.request.query_params.get('title', None)
        if title:
            queryset = queryset.filter(abctitle__icontains=title)
        return queryset


def issues_page(request):

        issues = Issue.objects.all().order_by('-created_at')
        users = User.objects.all().order_by('username')
        # Filtros desde GET parameters
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

        # Bulk Create (similar a la acción DRF)
        if request.method == 'POST':
            if 'bulk_titles' in request.POST:  # Si es un bulk create
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
            else:  # Si es un create normal
                form = IssueCreateForm(request.POST)
                if form.is_valid():
                    new_issue = form.save(commit=False)
                    new_issue.created_by = request.user
                    new_issue.save()
                    return redirect('custom-issues')
        else:
            form = IssueCreateForm()

        # Retornar el contexto al template
        return render(request, 'issues_page.html', {
            'issues': issues,
            'form': form,
            'users': users
        })


def issue_detail(request, issue_id):
    issue = get_object_or_404(Issue, id_issue=issue_id)

    if request.method == 'POST':
        if 'update_issue' in request.POST:
            issue_form = IssueUpdateForm(request.POST, instance=issue)
            if issue_form.is_valid():
                issue_form.save()
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

    return render(request, 'issue_detail.html', {
        'issue': issue,
        'issue_form': issue_form,
        'comment_form': comment_form
    })