from django.conf.urls.defaults import *
from divensis.portfolio import views as portfolio_views

urlpatterns = patterns('',
    url(r'^(?P<slug>[-\w]+)/$',
        view=portfolio_views.project_detail,
        name='portfolio_detail'),

    # TODO: add a portfolio_category_list view?

    url(r'^categories/(?P<slug>[-\w]+)/$',
        view=portfolio_views.category_detail,
        name='portfolio_category_detail'),

    url(r'^$',
        view=portfolio_views.project_list,
        name='portfolio_index'),
)
