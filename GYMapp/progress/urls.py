from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .views import member_progress_chart, member_progress_view  # Import views here

urlpatterns = [
    #path('api/member-progress-chart/<int:member_id>/', MemberProgressChartView.as_view(), name='member-progress-chart'),  # Add 'api/' prefix here
    path('progress', member_progress_view, name='progress'),  # Function-based view
    path('member-progress-chart/<int:member_id>/', member_progress_chart, name='member_progress_chart'),
]

# Serve media files during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
