
from django.conf.urls import patterns, url
from django.conf.urls import include

from rest_framework.urlpatterns import format_suffix_patterns
from core import views

urlpatterns = patterns('',
    url(r'^repositories/$', views.RepositoryList.as_view(), name='api-repository-list'),
    url(r'^repositories/(?P<pk>[0-9]+)/$', views.RepositoryDetail.as_view(), name='api-repository-detail'),
)

urlpatterns += patterns('',
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
)

urlpatterns = format_suffix_patterns(urlpatterns)
