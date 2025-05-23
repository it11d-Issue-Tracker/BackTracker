
from django.contrib import admin
from django.conf import settings
from django.http import HttpResponse
from django.conf.urls.static import static
from django.urls import re_path
from django.views.static import serve
from rest_framework import permissions
import yaml
import os
from Issue_Tracker import api
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.urls import path, include

from Issue_Tracker.views import *

# Custom view to serve api.yaml with Swagger UI
def serve_swagger_yaml(request):
    yaml_file_path = os.path.join(settings.BASE_DIR, 'api/api.yaml')
    try:
        with open(yaml_file_path, 'r') as file:
            yaml_content = yaml.safe_load(file)
    except FileNotFoundError:
        return HttpResponse("Error: api.yaml file not found", status=404)
    except yaml.YAMLError:
        return HttpResponse("Error: Invalid YAML format in api.yaml", status=400)

    # Create a schema view with the loaded YAML content
    schema_view = get_schema_view(
        openapi.Info(
            title=yaml_content.get('info', {}).get('title', 'Issue Tracker API'),
            default_version=yaml_content.get('info', {}).get('version', 'v1'),
            description=yaml_content.get('info', {}).get('description', 'API para gestionar issues'),
            terms_of_service="https://www.example.com/terms/",
            contact=openapi.Contact(email="daniel.espinalt@estudiantat.upc.edu"),
            license=openapi.License(name="MIT License"),
        ),
        public=True,
        permission_classes=(permissions.AllowAny,),
    )
    return schema_view.with_ui('swagger', cache_timeout=0)(request)
urlpatterns = [
    # Admin site
    path('admin/', admin.site.urls),

    path('accounts/', include('allauth.urls')),
    path('swagger/', serve_swagger_yaml, name='schema-swagger-ui'),

    path('login', custom_login_view, name='custom-login'),
    path('login/', custom_login_view, name='custom-login'),
    path('issues/', api.IssuesView.as_view(), name='all-issues'),
    path('issues/<int:issue_id>/', api.ViewIssue.as_view(), name='issue-detail'),
    path('issues/bulk-insert/', api.IssueBulkInsertAPIView.as_view(), name='bulk-insert'),

    path('comments/', api.CommentView.as_view(), name='comments'),
    path('comments/<int:comment_id>/', api.CommentDetailView.as_view(), name='comment-detail'),
    path('attachments/', api.AttachmentView.as_view(), name='attachments'),
    path('attachments/<int:attachment_id>/', api.AttachmentDetailView.as_view(), name='attachment-detail'),
    path('watchers/', api.WatcherView.as_view(), name='watchers'),
    path('watchers/<int:watcher_id>/', api.WatcherDetailView.as_view(), name='watcher-detail'),


    path('profile/', profile_view_id, name='self-profile'),
    path('profile/<int:userid>/', api.UserApiView.as_view(), name='profile'),
    path('profile/<int:userid>/token/', api.TokenPorfileApiView.as_view(), name='token'),

    path('profile/edit', edit_bio, name='edit_bio'),




    path('settings/', api.SettingsAPIView.as_view(), name='settings'),
    path('settings/status/', api.stausAPIView.as_view(), name='status'),
    path('settings/priority/', api.priorityAPIView.as_view(), name='priority'),
    path('settings/severity/', api.severityAPIView.as_view(), name='severity'),
    path('settings/type/', api.typeAPIView.as_view(), name='type'),

    path('settings/delete_status/<str:status_id>/', api.deleteStatusAPIView.as_view(), name='delete_status'),
    path('settings/delete_priority/<str:priority_id>/', api.deletePriorityAPIView().as_view(), name='delete_priority'),



    path('settings/delete_severity/<str:severity_id>/', api.deleteSeverityAPIView.as_view(), name='delete_severity'),
    path('settings/delete_type/<str:type_id>/', api.deleteTypeAPIView.as_view(), name='delete_type'),

    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
