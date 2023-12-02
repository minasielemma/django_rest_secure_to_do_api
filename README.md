# django_rest_secure_to_do_api
Plan endpoints:-

PlanView class:

This class handles the HTTP methods for creating, retrieving, updating, and deleting individual plans.
The permission_classes attribute is set to a tuple containing IsAuthenticated and IsOwnerOfPlan, which means that the user must be authenticated and the owner of the plan to perform these actions.
The serializer_class attribute is set to PlanSerializer, which is responsible for serializing and deserializing the Plan model.
The post method handles the HTTP POST request for creating a new plan. It receives the request data, validates it, and saves the plan if it is valid.
The get method handles the HTTP GET request for retrieving a specific plan. It retrieves the plan based on the provided ID and owner, serializes it, and returns the serialized data.
The put method handles the HTTP PUT request for updating a specific plan. It retrieves the plan based on the provided ID and owner, updates it with the request data, and returns the updated serialized data.
The delete method handles the HTTP DELETE request for deleting a specific plan. It retrieves the plan based on the provided ID and owner and deletes it.


PlanViewSet class:

This class handles the HTTP GET request for retrieving all plans associated with the authenticated user.
It defines the same permission_classes and serializer_class attributes as the PlanView class.
The get method retrieves all plans that belong to the authenticated user, serializes them, and returns the serialized data.

Task endpoints:- 

TaskView class:

This class is derived from APIView from the Django REST Framework.
It handles the HTTP methods for creating, retrieving, updating, and deleting individual tasks.
The permission_classes attribute is set to a tuple containing IsAuthenticated and IsOwnerOfTask, which means that the user must be authenticated and the owner of the task to perform these actions.
The serializer_class attribute is set to TaskSerializer, which is responsible for serializing and deserializing the Task model.
The post method handles the HTTP POST request for creating a new task. It receives the request data, validates it, and saves the task if it is valid.
The get method handles the HTTP GET request for retrieving a specific task. It retrieves the task based on the provided ID and owner, serializes it, and returns the serialized data.
The put method handles the HTTP PUT request for updating a specific task. It retrieves the task based on the provided ID and owner, updates it with the request data, and returns the updated serialized data.
The delete method handles the HTTP DELETE request for deleting a specific task. It retrieves the task based on the provided ID and owner and deletes it.

TaskViewSet class:

This class is derived from APIView from the Django REST Framework.
It handles the HTTP GET request for retrieving all tasks associated with the authenticated user.
It has the same permission_classes and serializer_class attributes as the TaskView class.
The get method retrieves all tasks that belong to the authenticated user, serializes them, and returns the serialized data.

PlanTaskView class:

This class is derived from APIView from the Django REST Framework.
It handles the HTTP GET request for retrieving all tasks under a specific plan associated with the authenticated user.
The permission_classes and serializer_class attributes are set the same way as in the previous classes.
The get method retrieves the plan based on the provided ID, filters tasks associated with that plan and the authenticated user, serializes them, and returns the serialized data.

