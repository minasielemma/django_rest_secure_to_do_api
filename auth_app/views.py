from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny


from .serializers import RegisterSerializer



class RegisterView(generics.CreateAPIView):
    
    title = "Sign Up"
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer