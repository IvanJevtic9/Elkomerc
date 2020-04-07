from django.contrib import admin
from django.conf.urls import url, include 

from django.contrib import admin
from django.conf.urls import url, include 

from .views import AuthView, RegisterAPIView, AccountListApiView, AccountDetailApiView

urlpatterns = [
    url(r'^auth/$', AuthView.as_view()),
    url(r'^auth/register/$', RegisterAPIView.as_view()),
    url(r'^account/$', AccountListApiView.as_view()),
    url(r'^account/(?P<id>\d+)/$', AccountDetailApiView.as_view())
]
