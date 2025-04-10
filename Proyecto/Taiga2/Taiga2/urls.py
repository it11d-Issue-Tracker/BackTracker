
from django.contrib import admin

from django.urls import path, include
from Issue_Tracker.views import issues_page, issue_detail, custom_login_view, profile_view_id, edit_bio

urlpatterns = [
    # Admin site
    path('admin/', admin.site.urls),

    path('accounts/', include('allauth.urls')),

    path('login/', custom_login_view, name='custom-login'),
    path('api/custom-issues/', issues_page, name='custom-issues'),
    path('api/issue-detail/<int:issue_id>/', issue_detail, name='issue-detail'),

    path('profile/', profile_view_id, name='self-profile'),
    path('profile/<int:user_id>/', profile_view_id, name='profile'),

    path('profile/edit', edit_bio, name='edit_bio'),
]
