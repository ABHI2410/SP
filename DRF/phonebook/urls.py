from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from . import views

urlpatterns = [
    path("",views.redirecttologin,name="baseview"),
    path('register/',views.RegisterView.as_view(),name="register"),
    path('login/',views.LoginAPIView.as_view(),name="login"),
    path('logout/', views.LogoutAPIView.as_view(), name="logout"),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('phonebook/list/', views.list,name="list"),
    path('phonebook/add/', views.add,name="add"),
    path('phonebook/deleteByName/', views.deleteByName,name="deletebyName"),
    path('phonebook/deleteByNumber/', views.deleteByNunber,name="deletebyNumber"),
]