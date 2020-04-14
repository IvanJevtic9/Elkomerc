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

    def get_queryset(self, *args, **kwargs):
        queryset_list = Category.objects.all()
        category_name_query = self.request.GET.get('category_name')
        
        if category_name_query:
            queryset_list = queryset_list.filter(
                Q(category_name__icontains=category_name_query)
            ).distinct()

        return queryset_list


class SubCategoryListApiView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = SubCategorySerializer

    def get_queryset(self, *args, **kwargs):
        queryset_list = SubCategory.objects.all()
        sub_category_name_query = self.request.GET.get('sub_category_name')
        category_name_query = self.request.GET.get('category_name')
        
        if category_name_query:
            queryset_list = queryset_list.filter(
                Q(category_id__category_name__iexact=category_name_query)                
            ).distinct()
        if sub_category_name_query:
            queryset_list = queryset_list.filter(
                Q(sub_category_name__iexact=sub_category_name_query)
            ).distinct()    

        return queryset_list

