from django.conf.urls import url

from .views import *

app_name = 'stream'
urlpatterns = [
    url(r'^$', cross, name='connect'),
    # url(r'^stream/upload/$', upload, name='upload'),
    # url(r'^stream/download/$', download, name='download'),
]
