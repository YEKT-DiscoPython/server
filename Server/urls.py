from django.conf.urls import patterns, include, url
from MusicServer.views import index_view, sign_out_view, user_view, upload_track, logout_view, download_view

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', index_view, name='index'),
    url(r'^user/id=(?P<uid>\d+)$', user_view, name='user'),
    url(r'^sign_out', sign_out_view, name='sign_out'),
    url(r'^upload$', upload_track, name='upload'),
    url(r'^logout$', logout_view, name='logout'),
    url(r'^download/(?P<track_id>\d+)$', download_view, name='download'),

    url(r'^admin/', include(admin.site.urls)),
)
