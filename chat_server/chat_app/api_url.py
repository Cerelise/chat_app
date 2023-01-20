from django.urls import path
from chat_app import api_views

urlpatterns = [
    path('login/', api_views.userLogin),
    path('userinfo/', api_views.Userinfo_view.as_view())
]
