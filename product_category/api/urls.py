from django.contrib import admin
from django.conf.urls import url, include 

from .views import CategoryListApiView, SubCategoryDetailApiView

urlpatterns = [
    url(r'^categories/$', CategoryListApiView.as_view()),
    url(r'^sub-categories/(?P<id>\d+)/$', SubCategoryDetailApiView.as_view(), name='detail'),
]