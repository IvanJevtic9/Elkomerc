from django.conf.urls import url, include 
from .views import ArticleListApiView, ProducerDetailApiView, ProducerListApiView, ArticleImportApiView

urlpatterns = [
    url(r'^articles/$', ArticleListApiView.as_view()),
    url(r'^producers/(?P<id>\d+)/$', ProducerDetailApiView.as_view(), name='detail'),
    url(r'^producers/$', ProducerListApiView.as_view()),
    url(r'^articles/import/$', ArticleImportApiView.as_view()),
]