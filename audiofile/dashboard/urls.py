from .views import AudioFileViewset
from django.urls import re_path

urlpatterns = [
    # path for update and retrive operation
    re_path(r'^audio/(?P<type_of_audio>[\w-]+)/(?P<pk>.+)',
            AudioFileViewset.as_view(
             {'get': 'retrieve', 'put': 'update', 'delete': 'delete'}),
            name='audiofile_by_id'),
    # path for list and create operation
    re_path(r'^audio/(?P<type_of_audio>[\w-]+)/$',
            AudioFileViewset.as_view({'get': 'list', 'post': 'create'}),
            name='audiofile')
    ]
