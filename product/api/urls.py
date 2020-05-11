from django.conf.urls import url, include 
from .views import ArticleListApiView, ProducerDetailApiView, ProducerListApiView, ArticleImportApiView, ArticleDetailApiView, ArticleImagesImportApiView

urlpatterns = [
    url(r'^articles/$', ArticleListApiView.as_view()),
    url(r'^articles/(?P<id>\d+)/$', ArticleDetailApiView.as_view(), name="article"),
    url(r'^producers/(?P<id>\d+)/$', ProducerDetailApiView.as_view(), name='detail'),
    url(r'^producers/$', ProducerListApiView.as_view()),
    url(r'^articles/import/$', ArticleImportApiView.as_view()),
    url(r'^articles/images/import/$', ArticleImagesImportApiView.as_view())
]