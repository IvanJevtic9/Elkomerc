from django.conf.urls import url, include 
from .views import (ArticleListApiView,
                    ProducerDetailApiView,
                    ProducerListApiView,
                    ArticleImportApiView,
                    ArticleDetailApiView,
                    ArticleImagesImportApiView,
                    ProducerImagesImportApiView,
                    ArticleGroupListApiView,
                    ArticleGroupDetailApiView,
                    PaymentOrderCreateApiView,
                    PaymentOrderDetailApiView,
                    PaymentOrderListApiView)

urlpatterns = [
    url(r'^articles/$', ArticleListApiView.as_view()),
    url(r'^articles/(?P<id>\d+)/$', ArticleDetailApiView.as_view(), name="article"),
    url(r'^article-groups/$', ArticleGroupListApiView.as_view()),
    url(r'^article-groups/(?P<id>\d+)/$', ArticleGroupDetailApiView.as_view(),name="article_group"),
    url(r'^producers/(?P<id>\d+)/$', ProducerDetailApiView.as_view(), name='detail'),
    url(r'^producers/$', ProducerListApiView.as_view()),
    url(r'^articles/import/$', ArticleImportApiView.as_view()),
    url(r'^articles/images/import/$', ArticleImagesImportApiView.as_view()),
    url(r'^producers/images/import/$', ProducerImagesImportApiView.as_view()),
    
    url(r'^payment-orders/create/$', PaymentOrderCreateApiView.as_view()),
    url(r'^payment-orders/$', PaymentOrderListApiView.as_view()),
    url(r'^payment-orders/(?P<id>\d+)/$', PaymentOrderDetailApiView.as_view())
]