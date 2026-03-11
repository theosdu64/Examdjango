from django.urls import path
from . import views

app_name = "app"
urlpatterns = [
    path("", views.home, name="home"),
    path("services/", views.services, name="services"),
    path("create-service/", views.create_service, name="create_service"),
    path("my-services/", views.my_services, name="my_services"),
]