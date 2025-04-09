
from django.contrib import admin
from django.urls import path

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from Issue_Tracker.views import IssueViewSet
from Issue_Tracker.views import issue_detail



router = DefaultRouter()
router.register(r'issues', IssueViewSet, basename='issue')


custom_urlpatterns = [
    path('issues/bulk-create/',
         IssueViewSet.as_view({'post': 'bulk_create'}),
         name='issue-bulk-create'),
]

urlpatterns = [
    # Admin site
    path('admin/', admin.site.urls),

    # API Authentication
    path('api-auth/', include('rest_framework.urls')),

    # DRF Router URLs
    path('api/', include(router.urls)),

    # Custom endpoints
    path('api/', include(custom_urlpatterns)),

    path('issues/search/', IssueViewSet.as_view({'get': 'search_issues', 'post': 'search_issues'}), name='issue-search'),

    path('api/custom-issues/', IssueViewSet.issues_page, name='custom-issues'),
    path('api/issue-detail/<int:issue_id>/', issue_detail, name='issue-detail'),
]
