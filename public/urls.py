

from django.conf.urls import patterns, url
from django.conf.urls import include

urlpatterns = patterns('public.views',    
    url(r'login/$', 'login', name="public_login"),
    url(r'logout/$', 'logout', name="public_logout"),
    url(r'(?P<username>[a-zA-Z0-9]+)/repositories/create/$', 'create_repository', name="public_create_repository"),
    url(r'(?P<username>[a-zA-Z0-9]+)/repositories/$', 'user_repositories', name="public_user_repositories"),
    url(r'(?P<username>[a-zA-Z0-9]+)/repositories/(?P<repository_id>\d+)/$', 'view_repository', name="public_view_repository"),
    url(r'(?P<username>[a-zA-Z0-9]+)/repositories/(?P<repository_id>\d+)/packages/create/$', 'create_package', name="public_create_package"),
    url(r'(?P<username>[a-zA-Z0-9]+)/repositories/(\d+)/packages/(?P<package_id>\d+)/$', 'view_package', name="public_view_package"),
    url(r'^$', 'main', name='public_main'),
)
