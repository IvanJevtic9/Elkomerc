from django.conf.urls import url, include 

from .views import (CoroselListApiView,
                    CoroselDetailApiView)

urlpatterns = [
    url(r'^corosel/$', CoroselListApiView.as_view()),
    url(r'^corosel/(?P<id>\d+)/$', CoroselDetailApiView.as_view(), name="detail")
]