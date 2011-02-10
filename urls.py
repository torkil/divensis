import datetime

from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

from tumbleweed import views as tumbler_views
from haystack.query import SearchQuerySet

admin.autodiscover()

TUMBLEWEED_SEARCH_QUERY = SearchQuerySet().filter(is_public=True, pub_date__lte=datetime.datetime.now())

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^blog/', include('divensis.blog.urls')),
    (r'^projects/', include('divensis.portfolio.urls')),
    (r'^tagging_suggest/', include('divensis.tagsuggest.urls')),
    (r'^search/', include('haystack.urls')),

    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/page/(?P<page>\d{1,5})/$',
        view = tumbler_views.archive_day,
        name = 'tumble_archive_day_pagination',
        kwargs = {
            'searchqueryset': TUMBLEWEED_SEARCH_QUERY,
            'paginate_by': settings.TUMBLEWEED_ARCHIVE_RESULTS_PER_PAGE,
            'month_format': '%m'
        }
    ),

    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$',
        view = tumbler_views.archive_day,
        name = 'tumble_archive_day_pagination',
        kwargs = {
            'searchqueryset': TUMBLEWEED_SEARCH_QUERY,
            'paginate_by': settings.TUMBLEWEED_ARCHIVE_RESULTS_PER_PAGE,
            'month_format': '%m'
        }
    ),

    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/page/(?P<page>\d{1,5})/$',
        view = tumbler_views.archive_month,
        name = 'tumble_archive_month_pagination',
        kwargs = {
            'searchqueryset': TUMBLEWEED_SEARCH_QUERY,
            'paginate_by': settings.TUMBLEWEED_ARCHIVE_RESULTS_PER_PAGE,
            'month_format': '%m'
        }
    ),

    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$',
        view = tumbler_views.archive_month,
        name = 'tumble_archive_month',
        kwargs = {
            'searchqueryset': TUMBLEWEED_SEARCH_QUERY,
            'paginate_by': settings.TUMBLEWEED_ARCHIVE_RESULTS_PER_PAGE,
            'month_format': '%m'
        }
    ),

    url(r'^(?P<year>\d{4})/page/(?P<page>\d{1,5})/$',
        view = tumbler_views.archive_year,
        name = 'tumble_archive_year_paginated',
        kwargs = {
            'searchqueryset': TUMBLEWEED_SEARCH_QUERY,
            'paginate_by': settings.TUMBLEWEED_ARCHIVE_RESULTS_PER_PAGE
        }
    ),

    url(r'^(?P<year>\d{4})/$',
        view = tumbler_views.archive_year,
        name = 'tumble_archive_year',
        kwargs = {
            'searchqueryset': TUMBLEWEED_SEARCH_QUERY,
            'paginate_by': settings.TUMBLEWEED_ARCHIVE_RESULTS_PER_PAGE
        }
    ),

    url(r'^page/(?P<page>\d{1,5})/ajax/$',
        view = tumbler_views.tumble,
        name = 'tumble_index_paginated_ajax',
        kwargs = {
            'searchqueryset': TUMBLEWEED_SEARCH_QUERY,
            'template_name': "tumbleweed/tumble_ajax.html"
        }
    ),

    url(r'^page/(?P<page>\d{1,5})/$',
        view = tumbler_views.tumble,
        name = 'tumble_index_paginated',
        kwargs = {
            'searchqueryset': TUMBLEWEED_SEARCH_QUERY
        }
    ),

    url(r'^$',
        view = tumbler_views.tumble,
        name = 'tumble_index',
        kwargs = {
            'searchqueryset': TUMBLEWEED_SEARCH_QUERY
        }
    ),
)

from feeds import RssTumbleweedFeed, AtomTumbleweedFeed
urlpatterns += patterns('',
    (r'^feeds/all/rss/$', RssTumbleweedFeed()),
    (r'^feeds/all/atom/$', AtomTumbleweedFeed()),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (
            r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT,
            'show_indexes': True}
        ),
    )