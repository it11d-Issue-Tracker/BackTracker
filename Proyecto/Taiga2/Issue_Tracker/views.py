from django.urls import reverse
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib import messages
from .models import Issue
from django.shortcuts import render, redirect
from .serializers import IssueSerializer
from django.utils.timezone import now
from django_filters.rest_framework import DjangoFilterBackend


class IssueViewSet(viewsets.ModelViewSet):
    renderer_classes = [viewsets.ModelViewSet.renderer_classes[0], viewsets.ModelViewSet.renderer_classes[1]]
    queryset = Issue.objects.all().order_by('created_at')
    serializer_class = IssueSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsAuthenticated]
    filterset_fields = ['status', 'priority_id', 'assigned_to', 'created_by']

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
