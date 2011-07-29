from django.conf.urls.defaults import *
from tag_puller.views import pull

urlpatterns = patterns('',
    url(r'(?P<tagnames>[\w-]+)/', pull, name='tag-puller-link'),
)

