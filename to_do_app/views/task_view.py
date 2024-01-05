from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status

import datetime
from ..permissions import IsOwnerOfTask
from ..serializers import PlanSerializer, TaskSerializer
from ..models import Plan, Task

class TaskView(APIView):
    
    
    title = "Task View"
    permission_classes = (IsAuthenticated,IsOwnerOfTask)
    serializer_class = TaskSerializer
    
    
    def post(self, request,format=None):
        try:
            if request.method == "POST":
                json_data = JSONParser().parse(request)
                pid = json_data["pid"]
                try:
                    plan = Plan.objects.get(owner=request.user, id = pid)
                except Plan.DoesNotExist:
                    return HttpResponse(status=status.HTTP_403_FORBIDDEN)
                start_time = datetime.datetime.strptime(json_data['start_time'],  '%Y-%m-%dT%H:%M:%S.%f')
                end_time = datetime.datetime.strptime(json_data['end_time'], '%Y-%m-%dT%H:%M:%S.%f')
                check_case_1 = Task.objects.filter(plan__owner=request.user, start_time__lte=start_time, end_time__gte=start_time)
                if check_case_1.exists():
                    return Response(data={"error":"There is another task on time given"}, status=status.HTTP_400_BAD_REQUEST)
                check_case_2 = Task.objects.filter(plan__owner=request.user, start_time__lte=end_time, end_time__gte=end_time)
                if check_case_2.exists():
                    return Response(data={"error":"There is another task on time given"}, status=status.HTTP_400_BAD_REQUEST)
                check_case_3 = Task.objects.filter(plan__owner=request.user, start_time__gte=start_time, end_time__lte=end_time)
                if check_case_3.exists():
                    return Response(data={"error":"There is another task on time given"}, status=status.HTTP_400_BAD_REQUEST)
                serializer = TaskSerializer(data=json_data, context={"plan":plan} )
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
                    task = Task.objects.get(id= id , plan__owner = request.user)
                except Task.DoesNotExist:
                    return HttpResponse(status =  status.HTTP_403_FORBIDDEN)
                serializer = TaskSerializer(task) 
                return Response(data=serializer.data)
            return HttpResponse(status= status.HTTP_405_METHOD_NOT_ALLOWED)
        except Exception as exe:
            print(exe)
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
    def put(self, request, id,format=None):
        try:
            if request.method == "PUT":
                try:
                    task = Task.objects.get(id= id , plan__owner = request.user)
                except Task.DoesNotExist:
                    return HttpResponse(status =  status.HTTP_403_FORBIDDEN)
                data = JSONParser().parse(request)
                serializer = TaskSerializer(instance=task,data=data)
                if serializer.is_valid():
                    serializer.update(task,data)
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
                    task = Task.objects.get(id= id , plan__owner = request.user)
                except Task.DoesNotExist:
                    return HttpResponse(status =  status.HTTP_403_FORBIDDEN)
                plan.delete()
                return HttpResponse(status=status.HTTP_200_OK)
            return HttpResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        except Exception as exe:
            print(exe)
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
         
         
                
class TaskViewSet(APIView):
    
    
    title = "Task View Set"
    permission_classes = (IsAuthenticated,IsOwnerOfTask)
    serializer_class = TaskSerializer
    
    
    def get(self, request):
        queryset = Task.objects.filter(plan__owner=request.user)
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data)
    
class PlanTaskView(APIView):
    
    title = "All task under plan"
    permission_classes = (IsAuthenticated,IsOwnerOfTask)
    serializer_class = TaskSerializer
    
    def get(self, request, pid):
        plan = get_object_or_404(Plan, id=pid)
        queryset = Task.objects.filter(plan=plan, plan__owner=request.user)
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data)