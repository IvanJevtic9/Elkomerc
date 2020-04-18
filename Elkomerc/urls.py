from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url

from account.api import urls
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'api/', include(('account.api.urls', 'account'), namespace='account')),
    path(r'api/product-category/', include(('product_category.api.urls', 'product-category'), namespace='product-category')),
    path(r'api/product/', include(('product.api.urls', 'product'), namespace='product')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
