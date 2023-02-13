from rest_framework import serializers
from chat_app.models import Userinfo


class Userinfo_data(serializers.ModelSerializer):
    class Meta:
        model = Userinfo
        fields = ['nickName', 'headImg', 'id']
        # fields = "__all__"
