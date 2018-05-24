from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^delete/(?P<id>\d+)$', views.delete),
    url(r'^editAccount$', views.editAccount),
    url(r'^like/(?P<id>\d+)$', views.like),
    url(r'^userQuotes/(?P<id>\d+)$', views.userQuotes),
    url(r'^addQuote$', views.addQuote),
    url(r'^logout$', views.logout),
    url(r'^quotes$', views.quotes),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^$', views.index),
]
