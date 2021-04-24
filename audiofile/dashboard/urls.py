from rest_framework.routers import DefaultRouter
from .views import AudioFileViewset
from django.urls import re_path, path

urlpatterns = [
    # path for update and retrive operation 
    re_path(r'^audio/(?P<type_of_audio>[\w-]+)/(?P<pk>.+)', AudioFileViewset.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'delete'})),
    # path for list and create operation
    re_path(r'^audio/(?P<type_of_audio>[\w-]+)/$', AudioFileViewset.as_view({'get': 'list', 'post': 'create'}))
    ]
