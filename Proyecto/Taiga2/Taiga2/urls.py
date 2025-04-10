
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from django.urls import path, include
from Issue_Tracker.views import *

urlpatterns = [
    # Admin site
    path('admin/', admin.site.urls),

    path('accounts/', include('allauth.urls')),

    path('login/', custom_login_view, name='custom-login'),
    path('api/custom-issues/', issues_page, name='custom-issues'),
    path('api/issue-detail/<int:issue_id>/', issue_detail, name='issue-detail'),

    path('settings/', settings_view, name='settings'),
    path('settings/delete_status/<str:status_id>/', delete_status, name='delete_status'),
    path('settings/delete_priority/<str:priority_id>/', delete_priority, name='delete_priority'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
