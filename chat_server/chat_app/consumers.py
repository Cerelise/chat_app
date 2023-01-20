import json
from asgiref.sync import async_to_sync, sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework.authtoken.models import Token
from chat_app.models import Userinfo


class ChatConsumer(AsyncWebsocketConsumer):
    # 异步
    async def connect(self):
        # 获取房间路由
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.userinfo_id = self.scope["url_route"]["kwargs"]["userid"]
        # print(self.scope)
        # 开设私聊通道
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.channel_layer.group_add(self.userinfo_id, self.channel_name)
        await self.accept()

    async def disconnet(self, close_code):
        # 离开房间
        await self.channel_layer.group_discard(self.room_name,
                                               self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        # client onOpen-msg
        # content = text_data_json["message"]

        token_str = text_data_json['message']['token']

        userinfo = await getUserinfo(token_str)
        content = getResponseData(userinfo, text_data_json)

        if content['code'] == 201:
            await self.channel_layer.group_send(str(content['data']['to']), {
                "type": "chat_message",
                "message": content
            })
            return

        # Send message to room group 组内消息发送
        await self.channel_layer.group_send(self.room_name, {
            "type": "chat_message",
            "message": content
        })

    async def chat_message(self, event):

        content = event["message"]

        await self.send(text_data=json.dumps({"message": content}))


@sync_to_async
def getUserinfo(token_str):
    token_obj = Token.objects.get(key=token_str).user
    userinfo = Userinfo.objects.get(belong=token_obj)

    return userinfo


def getResponseData(userinfo, text_data):
    if text_data['code'] == 201:
        resp_data = {
            "code": text_data['code'],
            "id": userinfo.id,
            "nickName": userinfo.nickName,
            "headImg": str(userinfo.headImg),
            "data": text_data['message']['data'],
            "from": userinfo.id
        }
        return resp_data

    resp_data = {
        "code": text_data['code'],
        "id": userinfo.id,
        "nickName": userinfo.nickName,
        "headImg": str(userinfo.headImg),
        "data": text_data['message']['data'],
    }
    return resp_data