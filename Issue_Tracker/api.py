from Issue_Tracker.serializers import *
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from Issue_Tracker.models import *
from rest_framework import generics
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


class IssuesView(generics.ListCreateAPIView):
    serializer_class = IssueSerializer

    def get_queryset(self, status=None):
        order_by = self.request.query_params.get('order_by')
        if order_by is not None:
            try:
                queryset = Issue.objects.all().order_by(order_by)
            except Issue.DoesNotExist:
                return Response({'error': 'No hay Issues'}, status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                queryset = Issue.objects.all()
            except Issue.DoesNotExist:
                return Response({'error': 'No hay Issues'}, status=status.HTTP_404_NOT_FOUND)

        q = self.request.query_params.get('q')
        if q is not None:
            queryset = queryset.filter(Q(Subject__icontains=q) | Q(Description__icontains=q))

        status = self.request.query_params.get('status')
        if status is not None:
            queryset = queryset.filter(Status__icontains=status)

        priority = self.request.query_params.get('priority')
        if priority is not None:
            queryset = queryset.filter(Priority__icontains=priority)

        creator = self.request.query_params.get('creator')
        if creator is not None:
            queryset = queryset.filter(Creator__username__icontains=creator)
        return queryset

    def delete(self, request):
        try:
            Issue.objects.all().delete()
        except Issue.DoesNotExist:
            return Response({'error': 'No hay Issues'}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_202_ACCEPTED)

    def post(self, request):
        user = request.user
        try:
            subject = request.data.get('Subject')
            description = request.data.get('Description')
            statuss = request.data.get('Status')
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        Issue.objects.create(
            title=subject,
            description=description,
            created_by=user,
            status= statuss
        )
        return Response(status=status.HTTP_201_CREATED)



class ViewIssue(APIView):
    def get(self, request, issue_id):
        try:
            issue = Issue.objects.get(pk=issue_id)
        except Issue.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = IssueDetailSerializer(issue)
        response_data = serializer.data
        return Response(response_data, status=status.HTTP_200_OK)

    def put(self, request, issue_id):
        try:
            issue = Issue.objects.get(pk=issue_id)
        except Issue.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = IssueDetailSerializer(issue, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, issue_id):
        try:
            issue = Issue.objects.get(pk=issue_id)
        except Issue.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        issue.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class DeleteIssues(APIView):

    def delete(self, request, issue_id):
        if request.method == 'DELETE':
            try:
                Issue.objects.filter(id=issue_id).delete()
            except Issue.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_200_OK)


class SettingsAPIView(APIView):
    authentication_classes(IsAuthenticated, )
    permission_classes(TokenAuthentication, )

    def get(self, request):
        statuses = Status.objects.all().order_by('orden')
        priorities = Priority.objects.all().order_by('orden')
        severities = Severity.objects.all().order_by('orden')
        types = Type.objects.all().order_by('orden')

        # Serialitzem les dades
        data = {
            'statuses': StatusSerializer(statuses, many=True).data,
            'priorities': PrioritySerializer(priorities, many=True).data,
            'severities': SeveritySerializer(severities, many=True).data,
            'types': TypeSerializer(types, many=True).data,
        }
        return Response(data, status=status.HTTP_200_OK)

class stausAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        statuses = Status.objects.all().order_by('orden')
        serializer = StatusSerializer(statuses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request):
        serializer = StatusSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class priorityAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        priorities = Priority.objects.all().order_by('orden')
        serializer = PrioritySerializer(priorities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request):
        serializer = PrioritySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class typeAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        types = Type.objects.all().order_by('orden')
        serializer = TypeSerializer(types, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request):
        serializer = TypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class severityAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        severities = Severity.objects.all().order_by('orden')
        serializer = SeveritySerializer(severities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request):
        serializer = SeveritySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


