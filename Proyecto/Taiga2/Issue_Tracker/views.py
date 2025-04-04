from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Issue
from .serializers import IssueSerializer
from django_filters.rest_framework import DjangoFilterBackend


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all().order_by('created_at')
    serializer_class = IssueSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsAuthenticated]
    filterset_fields = ['status', 'priority_id', 'assigned_to']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filtro por título
        title = self.request.query_params.get('title', None)
        if title:
            queryset = queryset.filter(abctitle__icontains=title)
        return queryset
