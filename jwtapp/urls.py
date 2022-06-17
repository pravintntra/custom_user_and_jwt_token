from django.urls import path
from jwtapp.views import Dashboard, MyTokenObtainPairView

urlpatterns = [
    path("", Dashboard.as_view(), name="dashboard"),
    path("login/", MyTokenObtainPairView().as_view(), name="login"),
]
