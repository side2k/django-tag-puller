from django.conf.urls.defaults import *
from tag_puller.core import pull

urlpatterns = patterns('',
    url(r'(?P<tagnames>[\w-]+)/', pull),
)

