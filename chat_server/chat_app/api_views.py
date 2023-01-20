from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from chat_app.models import Userinfo
from chat_app.serializers import Userinfo_data
from django.contrib.auth.hashers import check_password

HostUrl = 'http://127.0.0.1:9000/upload/'


@api_view(['POST'])
def userLogin(request):
    # print(request.POST)
    # 读取输入
    username = request.POST['username']
    password = request.POST['password']
    # 查询用户名以判断是否存在 返回一个用户列表
    user = User.objects.filter(username=username)
    if user:
        # 判断密码是否匹配
        # print(user[0])
        isnotUser = check_password(password, user[0].password)
        # print(isnotUser)
        if isnotUser:
            # 创建或更新Token
            token = Token.objects.update_or_create(user=user[0])
            token = Token.objects.get(user=user[0]).key
            return Response(token)
        else:
            return Response('pwd err')
    else:
        return Response('user none')


@api_view(['POST'])
def userinfo(request):
    token = request.POST['token']
    # 获取用户表
    user = Token.objects.get(key=token).user
    userinfo = Userinfo.objects.get(belong=user)

    userinfo_data = {
        "nickName": userinfo.nickName,
        "headImg": HostUrl + str(userinfo.headImg)
    }
    return Response(userinfo_data)


class Userinfo_view(APIView):
    def get(self, request, format=None):
        return Response('userinfo-get')

    def post(self, request, format=None):
        token = request.POST['token']
        if token:
            # 获取token
            token_str = Token.objects.filter(key=token)
            # print(token_data)
            # 得到token后才继续执行数据序列化
            if token_str:
                user = token_str[0].user
                userinfo = Userinfo.objects.filter(belong=user)

                userinfo_data = Userinfo_data(userinfo, many=True).data[0]
            else:
                userinfo_data = {
                    "nickName": "未登录",
                    "headImg": "upload/admin.jpg"
                }
            # if userinfo_data.is_valid():
            #     return Response(userinfo_data.data)
            # else:
            #     return Response(userinfo_data.errors)

            # userinfo_data = {
            #     "nickName": userinfo.nickName,
            #     "headImg": HostUrl + str(userinfo.headImg)
            # }
        else:
            userinfo_data = {"nickName": "未登录", "headImg": "upload/admin.jpg"}
        return Response(userinfo_data)
