from django.urls import path

from .views import PostCleaningJob


urlpatterns = [
    path(r'enter-path/', PostCleaningJob.as_view(), name='clean'),
]
