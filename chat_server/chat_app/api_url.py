from django.urls import path
from chat_app import api_views

urlpatterns = [
    path('dchat-login/', api_views.dchat_login),
    path('dchat-register/', api_views.dchat_register),
    path('dchat-logout/', api_views.dchat_logout),
    path('dchat-resetPwd/', api_views.dchat_reset_pwd),
    path('userinfo/', api_views.Userinfo_view.as_view())
]
