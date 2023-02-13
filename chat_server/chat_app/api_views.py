from collections import OrderedDict
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from chat_app.models import Userinfo
from chat_app.serializers import Userinfo_data
from django.contrib.auth.hashers import check_password, make_password

HostUrl = 'http://127.0.0.1:9000/upload/'


# 登录
@api_view(['POST'])
def dchat_login(request):
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


# 退出登录
@api_view(['POST'])
def dchat_logout(request):
    token = request.POST['token']
    user_token = Token.objects.get(key=token)
    user_token.delete()
    return Response('logout')


# 注册
@api_view(['POST'])
def dchat_register(request):
    username = request.POST['username']
    password = request.POST['password']
    # repassword = request.POST['repassword']
    user = User.objects.filter(username=username)
    if user:
        return Response('repeat')
    else:
        new_password = make_password(password, username)
        newUser = User(username=username, password=new_password)
        newUser.save()

    token = Token.objects.get_or_create(user=newUser)
    token = Token.objects.get(user=newUser)
    # print(token)
    # headImg類型限制 上傳有報錯 展示正常
    userinfo = Userinfo.objects.get_or_create(nickName=username, belong=newUser)
    userinfo = Userinfo.objects.get(belong=newUser)

    userinfo_data = {
        'token': token.key,
        'nickName': str(userinfo.nickName),
        "headImg": 'admin.jpg'
    }
    print(userinfo_data)

    # if userinfo_data.nickName == "":
    #     userinfo_data = {"nickName": "未设置", "headImg": "upload/admin.jpg"}
    return Response(userinfo_data)


# 重置密码
@api_view(['POST'])
def dchat_reset_pwd(request):
    username = request.POST['username']
    password = request.POST['password']
    user = User.objects.filter(username=username)
    if not user:
        return Response('user not exist')
    else:
        new_password = make_password(password, username)
        # print(new_password)
        User.objects.filter(username=username).update(password=new_password)
        new_user = User.objects.filter(username=username)
        # print(new_user)
        return Response('ok')


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
                print('before', userinfo_data)

                # for k, v in userinfo_data.items():
                #     if k == "headImg":
                #         if v == None:
                #             v = "admin.jpg"
                #     print("userinfo", k, v)
                # for k, v in userinfo_data.items():
                #     print("userinfo", k, v)
                if userinfo_data['headImg'] == None:
                    userinfo_data['headImg'] = '/upload/admin.jpg'
                # userinfo_data = OrderedDict([
                #     (k, "/upload/admin.jpg") if k == 'headImg' else (k, v)
                #     for k, v in userinfo_data.items()
                # ])

                print('after', userinfo_data)
                # print('头像地址：', userinfo_data.get("headImg"))
            else:
                userinfo_data = {
                    "nickName": "未登录",
                    "headImg": "/upload/admin.jpg"
                }
        else:
            userinfo_data = {"nickName": "未登录", "headImg": "/upload/admin.jpg"}
        return Response(userinfo_data)
