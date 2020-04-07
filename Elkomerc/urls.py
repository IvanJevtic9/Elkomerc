from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url

from account.api import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'api/', include('account.api.urls'))
]
