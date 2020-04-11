from django.contrib import admin
from django.conf.urls import url, include 

from django.contrib import admin
from django.conf.urls import url, include 

from .views import AuthView, RegisterAPIView, AccountListApiView, AccountDetailApiView, AccountChangePassword, activate

urlpatterns = [
    url(r'^auth/$', AuthView.as_view()),
    url(r'^auth/register/$', RegisterAPIView.as_view()),
    url(r'^account/$', AccountListApiView.as_view()),
    url(r'^account/(?P<id>\d+)/$', AccountDetailApiView.as_view()),
    url(r'^account/change-password/(?P<id>\d+)/$', AccountChangePassword.as_view()),
    url(r'^account/activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', activate, name='activate'),
]
