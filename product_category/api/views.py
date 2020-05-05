from rest_framework.response import Response
from rest_framework import generics, mixins, permissions
from rest_framework_jwt.settings import api_settings

from django.db.models import Q
from django.contrib.auth import authenticate

from .serializers import CategorySerializer, SubCategorySerializer
from product_category.models import Category, SubCategory

class CategoryListApiView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = CategorySerializer
    pagination_class = None

    def get_queryset(self, *args, **kwargs):
        queryset_list = Category.objects.all()
        category_name_query = self.request.GET.get('category_name')
        
        if category_name_query:
            queryset_list = queryset_list.filter(
                Q(category_name__icontains=category_name_query)
            ).distinct()

        return queryset_list


class SubCategoryDetailApiView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = SubCategorySerializer
    lookup_field = 'id'

    def get_queryset(self, *args, **kwargs):
        return SubCategory.objects.all()