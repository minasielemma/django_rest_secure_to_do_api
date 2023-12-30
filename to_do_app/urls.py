from django.urls import path, include

from .views.plan_views import PlanView, PlanViewSet
from .views.task_view import TaskView, TaskViewSet,PlanTaskView
from .views.user_view import UserView

urlpatterns = [
	path("plan/create/", PlanView.as_view(), name="create_plan"),
    path("plan/<int:id>/", PlanView.as_view(), name="plan_modify"),
    path("", PlanViewSet.as_view(), name="all_plan"),

    path('task/create/', TaskView.as_view(), name="task_create"),
    path('task/<int:id>', TaskView.as_view(), name="task_modify"),
    path('tasks/', TaskViewSet.as_view(), name='task-list'),
    path('plans/<int:pid>/tasks/', PlanTaskView.as_view(), name='plan-task-list'),
    
    path('user/', UserView.as_view(), name="user_view")
]

