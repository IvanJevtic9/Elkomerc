from rest_framework import generics, mixins, permissions

from django.http import JsonResponse

from account.api.permissions import IsAdminOrReadOnly
from rest_framework.reverse import reverse as api_reverse

from .serializers import CoroselListSerializer, CoroselDetailSerializer
from site_configurations.models import Corosel

def get_corosel_json_response(request):
    cor_list = Corosel.objects.all()
    response = []

    for cor in cor_list:
        obj = {
                "id": cor.id,
                "name": cor.name,
                "description": cor.description,
                "link": cor.link,
                "is_enabled": cor.is_enabled,
                "uri": api_reverse("site_configurations:detail", kwargs={"id": cor.id}, request=request)
            }
        if bool(cor.corosel_image.name):
            obj['corosel_image'] =  request.get_host() + cor.corosel_image.url

        response.append(obj)

    return JsonResponse(response, status=200, safe=False)


class CoroselListApiView(generics.ListAPIView,
                         generics.CreateAPIView):
    permission_classes = [IsAdminOrReadOnly, ]
    serializer_class = CoroselListSerializer
    pagination_class = None

    def get_queryset(self, *args, **kwargs):
        return Corosel.objects.all()
    
    def post(self, request, *args, **kwargs):
        return self.create(self, request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        request = request.request
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            name = serializer.validated_data.get('name', None)
            description = serializer.validated_data.get('description', None)
            link = serializer.validated_data.get('link', None)
            corosel_image = serializer.validated_data.get('corosel_image', None)
            is_enabled = serializer.validated_data.get('is_enabled', None)

            cor_obj = Corosel(name=name,description=description,link=link,is_enabled=is_enabled)         

            cor_obj.corosel_image = corosel_image
            cor_obj.save()

            return get_corosel_json_response(request)


class CoroselDetailApiView(mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin,
                           generics.RetrieveAPIView):
    permission_classes = [permissions.IsAdminUser, ]
    serializer_class = CoroselDetailSerializer
    pagination_class = None
    lookup_field = 'id'
    
    def get_queryset(self, *args, **kwargs):
        return Corosel.objects.all().order_by('id')

    def delete(self, request, *args, **kwargs):
        self.check_object_permissions(self.request, self.get_object())
        return self.destroy(request, *args, **kwargs)    

    def put(self, request, *args, **kwargs):
        self.check_object_permissions(self.request, self.get_object())
        return self.update(self, request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        request = request.request
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=False):
            cor_id = int(self.kwargs['id'])
            cor_obj = Corosel.objects.get(id=cor_id)

            name = serializer.validated_data.get('name', None)
            description = serializer.validated_data.get('description', None)
            link = serializer.validated_data.get('link', None)
            corosel_image = serializer.validated_data.get('corosel_image', None)
            is_enabled = serializer.validated_data.get('is_enabled', None)

            if name:
                cor_obj.name = name
            if description:
                cor_obj.description = description
            if corosel_image:
                cor_obj.corosel_image.delete(save=False)
                cor_obj.corosel_image = corosel_image
            if link:
                cor_obj.link = link
            if is_enabled:
                cor_obj.is_enabled = is_enabled

            cor_obj.save()

            return get_corosel_json_response(request.get_host())
    
                        
                