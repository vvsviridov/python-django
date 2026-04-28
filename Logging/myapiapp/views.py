from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.mixins import ListModelMixin

from django.contrib.auth.models import Group

from .serializers import GroupSerializer


@api_view()
def hw_view(request: Request) -> Response:
    return Response({'message': 'Hello from REST!'})


class GroupListView(ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


# class GroupListView(GenericAPIView, ListModelMixin):
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer

#     def get(self, request: Request) -> Response:
#         return self.list(request)


# class GroupListView(APIView):
#     def get(self, request: Request) -> Response:
#         groups = Group.objects.all()
#         serialized = GroupSerializer(groups, many=True)
#         return Response({'groups': serialized.data})
