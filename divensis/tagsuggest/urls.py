from django.conf.urls.defaults import *
from divensis.tagsuggest import views as tagsuggest_views

urlpatterns = patterns('',
    url(r'^$',
        view=tagsuggest_views.search_tags,
        name='tagsuggest_search'),
)