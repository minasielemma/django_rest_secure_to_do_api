from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Plan, Task

class UserSerializer(serializers.ModelSerializer):
    
    title = 'User Serializer'
    
    
    class Meta:
        model = User
        fields = ('id','username', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }
        

class PlanSerializer(serializers.ModelSerializer):
    
    
    title = 'Plan Serializer'
    owner_data = UserSerializer(read_only=True)
    
    
    class Meta:
        model = Plan
        fields = ['id','plan_name','owner','created_at','start_time','end_time','modified_at','owner_data']
    
    
    def create(self, validated_data):
        plan = Plan.objects.create(**validated_data)
        plan.save()
        return plan
    
    
    def update(self, instance, validated_data):
        instance.plan_name = validated_data["plan_name"]
        instance.start_time =validated_data["start_time"]
        instance.end_time = validated_data["end_time"]
        instance.save()
        return instance

class TaskSerializer(serializers.ModelSerializer):
    
    
    plan_data = PlanSerializer(read_only=False)
    title = 'Task Serializer'
    
    
    class Meta:
        model = Task
        fields = ["id","task_name", "plan","created_at", "modified_at", "start_time","end_time","plan_data"]
    
    
    def create(self, validated_data):
        plan_id = validated_data.pop("plan")
        try:
            plan = Plan.objects.get(id = plan_id)
        except Exception as exe:    
            raise serializers.ValidationError({"plan": "Please create plan. There is no plan with current plan id"}) from exe
        task = Task.objects.create(plan=plan, **validated_data)
        return task
    
    
    def update(self, instance, validated_data):
        instance.task_name = validated_data["task_name"]
        instance.start_time = validated_data["start_time"]
        instance.end_time = validated_data["end_time"]
        instance.save()
        return instance    