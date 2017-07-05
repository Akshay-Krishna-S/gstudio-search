from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.get_search, name='index'),
    url(r'^advanced/',views.advanced_search,name='advanced_search')
]
