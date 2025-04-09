# Issue_Tracker/apps.py
from django.apps import AppConfig

class IssueTrackerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Issue_Tracker'

    def ready(self):
        import Issue_Tracker.signals