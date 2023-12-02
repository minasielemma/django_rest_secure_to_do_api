from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from .views import RegisterView

urlpatterns = [
	path('token/',jwt_views.TokenObtainPairView.as_view(),name ='token_obtain_pair'),
	path('token/refresh/', jwt_views.TokenRefreshView.as_view(),name ='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
]
