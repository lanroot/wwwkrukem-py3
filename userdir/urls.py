from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^all/$', 'userdir.views.persons'),
    url(r'^get/(?P<person_id>\d+)/$', 'userdir.views.person'),
#    url(r'^search/$', 'userdir.views.autocomplete'),
    url(r'^search/autocomplete/$', 'userdir.views.autocomplete'),
    url(r'^search_persons/$', 'userdir.views.search_persons'),
    url(r'^search.php$', 'userdir.views.search_persons_cp1251'),
)
