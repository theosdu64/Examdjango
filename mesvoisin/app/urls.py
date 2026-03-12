from django.urls import path
from . import views

app_name = "app"
urlpatterns = [
    path("", views.home, name="home"),
    path("services/", views.services, name="services"),
    path("create-service/", views.create_service, name="create_service"),
    path("my-services/", views.my_services, name="my_services"),
    path("exchange/", views.exchange, name="exchange"),
    # Button OnClick
    path("postulez/<int:service_id>/", views.postulez, name="postulez"),
    path("delete-skill/<int:skill_id>/", views.deleteUserSkill, name="delete_skill"),
    path("add-skill/<int:skill_id>/", views.addUserSkill, name="add_skill"),
]