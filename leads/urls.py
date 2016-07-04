from django.conf.urls import url
from . import views

app_name = 'leads'
urlpatterns = [
    url(r'^$', views.index, name='list'),
    url(r'^(?P<get_leadgen_id>[0-9]+)/$', views.detail, name='detail'),
]