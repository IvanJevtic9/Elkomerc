from django.contrib import admin
from django.conf.urls import url, include 

from .views import CategoryListApiView, SubCategoryListApiView

urlpatterns = [
    url(r'^categories/$', CategoryListApiView.as_view()),
    url(r'^sub-categories/$', SubCategoryListApiView.as_view()),
]