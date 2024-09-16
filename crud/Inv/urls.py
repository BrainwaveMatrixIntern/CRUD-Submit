from django.urls import path
from Inv import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("signup/", views.RegView.as_view(), name="signup"),
    path("dashboard/", views.DashBoard.as_view(), name="dashboard"),
    path("addItem/", views.ItemAdd.as_view(), name="addItem"),
    path("deleteItem/<int:pk>/", views.ItemDelete.as_view(), name="deleteItem"),
    path("updateItem/<int:pk>", views.ItemEdit.as_view(), name="updateItem"),
    path("login/", auth_views.LoginView.as_view(template_name="Inv/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="Inv/logout.html"), name="logout"),
]