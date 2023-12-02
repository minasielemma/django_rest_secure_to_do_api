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

import datetime
from ..permissions import IsOwnerOfPlan
from ..serializers import PlanSerializer, TaskSerializer
from ..models import Plan, Task

class PlanView(APIView):
    
    title = "Plan View"
    permission_classes = (IsAuthenticated,IsOwnerOfPlan)
    serializer_class = PlanSerializer
    
    
    def post(self, request,format=None):
        try:
            if request.method == "POST":
                json_data = JSONParser().parse(request)
                start_time = datetime.datetime.strptime(json_data['start_time'],  "%Y-%m-%dT%H:%M:%S")
                end_time = datetime.datetime.strptime(json_data['end_time'], "%Y-%m-%dT%H:%M:%S")
                check_case_1 = Plan.objects.filter( owner=request.user, start_time__lte=start_time, end_time__gte=start_time)
                if check_case_1.exists():
                    return Response(data={"error":"There is another plan on time given"}, status=status.HTTP_400_BAD_REQUEST)
                check_case_2 = Plan.objects.filter( owner=request.user, start_time__lte=end_time, end_time__gte=end_time)
                if check_case_2.exists():
                    return Response(data={"error":"There is another plan on time given"}, status=status.HTTP_400_BAD_REQUEST)
                check_case_3 = Plan.objects.filter( owner=request.user, start_time__gte=start_time, end_time__lte=end_time)
                if check_case_3.exists():
                    return Response(data={"error":"There is another plan on time given"}, status=status.HTTP_400_BAD_REQUEST)
                user = get_object_or_404(User, username = request.user.username)
                json_data["owner"] = user.id
                serializer = PlanSerializer(data=json_data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(data=serializer.data, status=status.HTTP_201_CREATED) 
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return HttpResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        except Exception as e:
            print(e)
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get(self, request, id,format=None):
        try:
            if request.method == "GET":
                try:
                    plan = Plan.objects.get(id=id, owner = request.user)
                except Plan.DoesNotExist:
                    return HttpResponse(status = status.HTTP_403_FORBIDDEN)
                serializer = PlanSerializer(plan) 
                return Response(data=serializer.data)
            return HttpResponse(status= status.HTTP_405_METHOD_NOT_ALLOWED)
        except Exception as exe:
            print(exe)
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request, id,format=None):
        try:
            if request.method == "PUT":
                try:
                    plan = Plan.objects.get(id= id, owner = request.user)
                except Plan.DoesNotExist:
                    return HttpResponse(status = status.HTTP_403_FORBIDDEN)
                data = JSONParser().parse(request)
                serializer = PlanSerializer(instance=plan,data=data)
                if serializer.is_valid():
                    serializer.update(plan,data)
                    return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
                return Response(data=serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)
            return HttpResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        except Exception as exe:
            print(exe)
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self, request, id,format=None):
        try:
            if request.method == "DELETE":
                try:
                    plan = Plan.objects.get(id= id, owner = request.user)
                except Plan.DoesNotExist:
                    return HttpResponse(status = status.HTTP_403_FORBIDDEN)
                plan.delete()
                return HttpResponse(status=status.HTTP_200_OK)
            return HttpResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        except Exception as exe:
            print(exe)
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
class PlanViewSet(APIView):
    
    title = "Plan View Set"
    permission_classes = (IsAuthenticated,IsOwnerOfPlan)
    serializer_class = PlanSerializer
    
    
    def get(self, request):
        queryset = Plan.objects.filter(owner=request.user)
        serializer = PlanSerializer(queryset, many=True)
        return Response(serializer.data)
    
