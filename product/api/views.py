from rest_framework.response import Response
from rest_framework import generics, mixins, permissions
from rest_framework_jwt.settings import api_settings

from django.db.models import Q
from django.contrib.auth import authenticate

from .serializers import ArticleSerializer, ProducerSerializer, ProducerListSerializer 
from product.models import Article, Producer

class ArticleListApiView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ArticleSerializer

    def get_queryset(self, *args, **kwargs):
        queryset_list = Article.objects.all()

        return queryset_list

class ProducerDetailApiView(generics.RetrieveAPIView): 
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ProducerSerializer
    lookup_field = 'id'

    def get_queryset(self, *args, **kwargs):
        return Producer.objects.all()

class ProducerListApiView(generics.ListAPIView): 
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ProducerListSerializer

    def get_queryset(self, *args, **kwargs):
        return Producer.objects.all()

    def get_serializer_context(self):
        return {'request': self.request}     