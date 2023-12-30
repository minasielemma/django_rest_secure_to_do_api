from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.contrib.auth.models import User
from ..serializers import UserSerializer

class UserView(APIView):
    
    permission_classes = (IsAuthenticated, )
    serializer_class = UserSerializer
    
    def get(self, request):
        serializer = UserSerializer(request.user);
        return Response(serializer.data, status=status.HTTP_200_OK)
    