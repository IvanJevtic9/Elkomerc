from django.conf.urls import url, include 
from .views import ArticleListApiView, ProducerDetailApiView, ProducerListApiView, ArticleImportApiView, ArticleDetailApiView, ArticleImagesImportApiView, ProducerImagesImportApiView, PaymentItemDetailApiView, PaymentItemCreateApiView, PaymentOrderListApiView, PaymentOrderCreateApiView

urlpatterns = [
    url(r'^articles/$', ArticleListApiView.as_view()),
    url(r'^articles/(?P<id>\d+)/$', ArticleDetailApiView.as_view(), name="article"),
    url(r'^producers/(?P<id>\d+)/$', ProducerDetailApiView.as_view(), name='detail'),
    url(r'^producers/$', ProducerListApiView.as_view()),
    url(r'^articles/import/$', ArticleImportApiView.as_view()),
    url(r'^articles/images/import/$', ArticleImagesImportApiView.as_view()),
    url(r'^producers/images/import/$', ProducerImagesImportApiView.as_view()),
    url(r'^payments/item/(?P<id>\d+)/$', PaymentItemDetailApiView.as_view(), name='item_detail'),
    url(r'^payments/item/$', PaymentItemCreateApiView.as_view()),
    url(r'^payments/order/$', PaymentOrderListApiView.as_view()),
    url(r'^payments/order/create/$', PaymentOrderCreateApiView.as_view()),
]