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
            queryset = queryset.filter(Q(title__icontains=q) | Q(description__icontains=q))

        status = self.request.query_params.get('status')
        if status is not None:
            queryset = queryset.filter(status=status)

        priority = self.request.query_params.get('priority')
        if priority is not None:
            queryset = queryset.filter(priority=priority)

        created_by = self.request.query_params.get('created_by')
        if created_by is not None:
            queryset = queryset.filter(created_by=created_by)

        assigned_to = self.request.query_params.get('assigned_to')
        if assigned_to is not None:
            queryset = queryset.filter(assigned_to=assigned_to)

        type = self.request.query_params.get('type')
        if type is not None:
            queryset = queryset.filter(type=type)

        severity = self.request.query_params.get('severity')
        if severity is not None:
            queryset = queryset.filter(severity=severity)
        return queryset




    def delete(self, request):
        try:
            Issue.objects.all().delete()
        except Issue.DoesNotExist:
            return Response({'error': 'No hay Issues'}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_202_ACCEPTED)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ViewIssue(APIView):
    def get(self, request, issue_id):
        try:
            issue = Issue.objects.get(pk=issue_id)
        except Issue.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = IssueDetailSerializer(issue)
        issue_data = serializer.data

        # Afegeix els comentaris
        comments = Comment.objects.filter(issue=issue)
        issue_data['comments'] = CommentSerializer(comments, many=True).data

        # Afegeix els watchers
        watchers = Watcher.objects.filter(issue=issue)
        issue_data['watchers'] = WatcherSerializer(watchers, many=True).data

        # Afegeix els attachments
        attachments = Attachment.objects.filter(issue=issue)
        issue_data['attachments'] = AttachmentSerializer(attachments, many=True).data

        return Response(issue_data, status=status.HTTP_200_OK)

    def put(self, request, issue_id):
        try:
            issue = Issue.objects.get(pk=issue_id)
        except Issue.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = IssueSerializer(issue, data=request.data, partial=True)
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


class CommentView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Comment.objects.all().order_by('-created_at')
        issue_id = self.request.query_params.get('issue_id')
        if issue_id:
            queryset = queryset.filter(issue__id_issue=issue_id)
        return queryset

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            issue_id = serializer.validated_data['issue'].id_issue
            if not Issue.objects.filter(id_issue=issue_id).exists():
                return Response({"error": "El issue especificado no existe."}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if comment.author != request.user:
            return Response({"error": "No puedes editar un comentario que no creaste."}, status=status.HTTP_403_FORBIDDEN)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if comment.author != request.user:
            return Response({"error": "No puedes eliminar un comentario que no creaste."}, status=status.HTTP_403_FORBIDDEN)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AttachmentView(generics.ListCreateAPIView):
    serializer_class = AttachmentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Attachment.objects.all()
        issue_id = self.request.query_params.get('issue_id')
        if issue_id:
            queryset = queryset.filter(issue__id_issue=issue_id)
        return queryset

    def post(self, request):
        serializer = AttachmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AttachmentDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, attachment_id):
        attachment = get_object_or_404(Attachment, attachment_id=attachment_id)
        serializer = AttachmentSerializer(attachment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, attachment_id):
        attachment = get_object_or_404(Attachment, attachment_id=attachment_id)
        attachment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class WatcherView(generics.ListCreateAPIView):
    serializer_class = WatcherSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Watcher.objects.all()
        issue_id = self.request.query_params.get('issue_id')
        if issue_id:
            queryset = queryset.filter(issue__id_issue=issue_id)
        return queryset

    def post(self, request):
        serializer = WatcherSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(user=request.user)
            except IntegrityError:
                return Response({"error": "Este usuario ya está observando este issue."}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WatcherDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, watcher_id):
        watcher = get_object_or_404(Watcher, id=watcher_id)
        serializer = WatcherSerializer(watcher)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, watcher_id):
        watcher = get_object_or_404(Watcher, id=watcher_id)
        if watcher.user != request.user:
            return Response({"error": "No puedes eliminar a otro usuario como watcher."}, status=status.HTTP_403_FORBIDDEN)
        watcher.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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

class deleteStatusAPIView(APIView):
    def delete(self, request, status_id):
        try:
            sstatus = Status.objects.get(pk=status_id)
            default_status = Issue._meta.get_field('status').get_default()
            if sstatus.id == default_status:
                return Response({"error": "No puedes eliminar el estado por defecto."}, status=status.HTTP_400_BAD_REQUEST)
        except Status.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        sstatus.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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

class deletePriorityAPIView(APIView):
    def delete(self, request, priority_id):
        try:
            priority = Priority.objects.get(pk=priority_id)
            default_priority = Issue._meta.get_field('priority').get_default()
            if priority.id == default_priority:
                return Response({"error": "No puedes eliminar la prioridad por defecto."}, status=status.HTTP_400_BAD_REQUEST)
        except Priority.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        priority.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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

class deleteTypeAPIView(APIView):
    def delete(self, request, type_id):
        try:
            type = Type.objects.get(pk=type_id)
            default_type = Issue._meta.get_field('type').get_default()
            if type.id == default_type:
                return Response({"error": "No puedes eliminar el tipo por defecto."}, status=status.HTTP_400_BAD_REQUEST)
        except Type.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        type.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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

class deleteSeverityAPIView(APIView):
    def delete(self, request, severity_id):
        try:
            severity = Severity.objects.get(pk=severity_id)
            default_severity = Issue._meta.get_field('severity').get_default()
            if severity.id == default_severity:
                return Response({"error": "No puedes eliminar la severidad por defecto."}, status=status.HTTP_400_BAD_REQUEST)
        except Severity.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        severity.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    def get(self, request,userid):
        user = get_object_or_404(User, id=userid)
        assigned_issues = Issue.objects.filter(assigned_to=user)
        watched_issues = Issue.objects.filter(watchers__user=user)
        comentaris = Comment.objects.filter(author_id=userid)
        perfil = get_object_or_404(Perfil, user_id=userid)
        perfil_bio_str = str(perfil.bio)
        perfil_url = str(perfil.avatar_url)


        data = {
            'id': user.id,
            'perfil': perfil_bio_str,
            'url': perfil_url,
            'assigned_issues': IssueSerializer(assigned_issues, many=True).data,
            'watched_issues': IssueSerializer(watched_issues, many=True).data,
            'comments': CommentSerializer(comentaris, many=True).data,
            'assigned_count': assigned_issues.count(),
            'watched_count': watched_issues.count(),
            'comments_count': comentaris.count()



        }
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request,userid):
        if request.user.id != userid:
            return Response({"error": "No puedes editar este usuario."}, status=status.HTTP_403_FORBIDDEN)
        bio = request.data.get('bio')
        url = request.data.get('url')
        perfil = get_object_or_404(Perfil, user_id=userid)
        if bio:
            perfil.bio = bio
        if url:  # and is_valid_image_url(avatar_url):
            perfil.avatar_url = url
        perfil.save()
        return Response({"message": "Perfil actualizado correctamente."}, status=status.HTTP_200_OK)


# Python
class IssueBulkInsertAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        issues_data = request.data.get('issues', [])
        if not issues_data:
            return Response({"error": "No se proporcionaron datos de issues."}, status=status.HTTP_400_BAD_REQUEST)

        created_issues = []
        for issue_data in issues_data:
            serializer = IssueSerializer(data=issue_data, partial=True)
            if serializer.is_valid():
                serializer.save(created_by=request.user)  # Asigna el usuario autenticado
                created_issues.append(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(created_issues, status=status.HTTP_201_CREATED)


class TokenPorfileApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request,userid):
        user = get_object_or_404(User, id=userid)
        token = user.auth_token.key

        data = {
            'id': user.id,
            'token': token
        }
        return Response(data, status=status.HTTP_200_OK)