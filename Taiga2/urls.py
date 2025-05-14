
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path
from django.views.static import serve
from Issue_Tracker import api


from django.urls import path, include

from Issue_Tracker.views import *

urlpatterns = [
    # Admin site
    path('admin/', admin.site.urls),

    path('accounts/', include('allauth.urls')),

    path('login', custom_login_view, name='custom-login'),
    path('login/', custom_login_view, name='custom-login'),
    path('api/issues/', api.IssuesView.as_view(), name='all-issues'),
    path('api/issues/<int:issue_id>/', api.ViewIssue.as_view(), name='issue-detail'),

    path('api/comments/', api.CommentView.as_view(), name='comments'),
    path('api/comments/<int:comment_id>/', api.CommentDetailView.as_view(), name='comment-detail'),
    path('api/attachments/', api.AttachmentView.as_view(), name='attachments'),
    path('api/attachments/<int:attachment_id>/', api.AttachmentDetailView.as_view(), name='attachment-detail'),
    path('api/watchers/', api.WatcherView.as_view(), name='watchers'),
    path('api/watchers/<int:watcher_id>/', api.WatcherDetailView.as_view(), name='watcher-detail'),


    path('profile/', profile_view_id, name='self-profile'),
    path('profile/<int:userid>/', profile_view_id, name='profile'),

    path('profile/edit', edit_bio, name='edit_bio'),


    path('settings/', api.SettingsAPIView.as_view(), name='settings'),
    path('settings/status/', api.stausAPIView.as_view(), name='status'),
    path('settings/priority/', api.priorityAPIView.as_view(), name='priority'),
    path('settings/severity/', api.severityAPIView.as_view(), name='severity'),
    path('settings/type/', api.typeAPIView.as_view(), name='type'),

    path('settings/delete_status/<str:status_id>/', delete_status, name='delete_status'),
    path('settings/delete_priority/<str:priority_id>/', delete_priority, name='delete_priority'),



    path('settings/delete_severity/<str:severity_id>/', delete_severity, name='delete_severity'),
    path('settings/delete_type/<str:type_id>/', delete_type, name='delete_type'),

    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
