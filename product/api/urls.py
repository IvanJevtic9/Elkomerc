from django.conf.urls import url, include 
from .views import ArticleListApiView, ProducerDetailApiView, ProducerListApiView

urlpatterns = [
    url(r'^articles/$', ArticleListApiView.as_view()),
    url(r'^producers/(?P<id>\d+)/$', ProducerDetailApiView.as_view(), name='detail'),
    url(r'^producers/$', ProducerListApiView.as_view()),
]