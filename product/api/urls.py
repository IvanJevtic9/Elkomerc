from django.conf.urls import url, include 
from .views import ProductListApiView, ArticleListApiView, ProducerDetailApiView, ProducerListApiView

urlpatterns = [
    url(r'^products/$', ProductListApiView.as_view()),
    url(r'^articles/$', ArticleListApiView.as_view()),
    url(r'^producers/(?P<id>\d+)/$', ProducerDetailApiView.as_view(), name='detail'),
    url(r'^producers/$', ProducerListApiView.as_view()),
]