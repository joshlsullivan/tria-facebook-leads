from django.conf.urls import include, url
from .views import WebhookView

app_name = 'webhook'
urlpatterns = [
    url(r'^17804a29424631dcd57517ec7989d126f3c8d00cce1a22494a/$', WebhookView.as_view()),
]