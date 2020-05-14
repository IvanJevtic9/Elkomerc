from django.contrib import admin
from django.conf.urls import url, include 

from .views import (
                    AuthView,
                    RegisterAPIView,
                    AccountListApiView,
                    AccountDetailApiView,
                    AccountChangePassword,
                    PostCodeListView,
                    activate,
                    reset_password,
                    ChangePasswordViaEmailAPIView,
                    WishlistListApiView,
                    WishlistDetailApiView,
                    StarsListApiView,
                    StarsDetailApiView,
                    CommentsListApiView,
                    CommentsDetailApiView
)

urlpatterns = [
    url(r'^auth/$', AuthView.as_view()),
    url(r'^auth/register/$', RegisterAPIView.as_view()),
    url(r'^accounts/$', AccountListApiView.as_view()),
    url(r'^accounts/(?P<id>\d+)/$', AccountDetailApiView.as_view(), name='detail'),
    url(r'^accounts/change-password/(?P<id>\d+)/$', AccountChangePassword.as_view()),
    url(r'^accounts/activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', activate, name='activate'),
    url(r'^accounts/reset-password-via-email/$', ChangePasswordViaEmailAPIView.as_view()),
    url(r'^accounts/reset-password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', reset_password, name='reset_password'),
    url(r'^post-codes/$', PostCodeListView.as_view()),
    url(r'^accounts/wishlist/$', WishlistListApiView.as_view()),
    url(r'^accounts/wishlist/(?P<id>\d+)/$', WishlistDetailApiView.as_view(), name='wishlist'),
    url(r'^accounts/stars/$', StarsListApiView.as_view()),
    url(r'^accounts/stars/(?P<id>\d+)/$', StarsDetailApiView.as_view(), name='stars'),
    url(r'^accounts/comments/$', CommentsListApiView.as_view()),
    url(r'^accounts/comments/(?P<id>\d+)/$', CommentsDetailApiView.as_view(), name='comments'),
]
