<template>
	<div id="page-box">
		<div id="logo">
			<img src="http://127.0.0.1:9000/upload/admin.jpg" alt="" />
			<h1>{{ text }}</h1>
		</div>

		<div id="unread">
			<div
				@click="openOtherChat(item)"
				v-for="(item, index) in unreadList"
				:key="index"
				class="unread-msg"
			>
				<img :src="'http://127.0.0.1:9000/upload/' + item.headImg" alt="" />
				<span>{{ item.data.length }}</span>
			</div>
		</div>

		<div id="message-list">
			<div v-for="(item, index) in msgList" :key="index">
				<div
					@click="openOtherChat(item)"
					v-if="userinfo.nickName != item.nickName"
					class="other message"
				>
					<img :src="'http://127.0.0.1:9000/upload/' + item.headImg" alt="" />
					<div class="nickname">{{ item.nickName }}</div>
					<div class="msgtext">{{ item.data[0].text }}</div>
				</div>

				<div v-else class="self message">
					<img :src="'http://127.0.0.1:9000/upload/' + item.headImg" alt="" />
					<div class="nickname">{{ item.nickName }}</div>
					<div class="msgtext">{{ item.data[0].text }}</div>
				</div>
			</div>
		</div>

		<div id="userinfo">
			<img :src="userinfo.headImg" alt="" />
			<span> {{ userinfo.nickName }} :</span>
		</div>

		<div id="text-input">
			<textarea
				@keydown.enter="enterSendMsg()"
				v-model="text_input"
				cols="30"
				rows="10"
			></textarea>
			<button @click="clickto">send</button>
		</div>
		<LoginBox :ShowBox="showbox" @changeLogin="changeLogin"></LoginBox>
		<PrivateChat
			:ShowBox="showOtherChat"
			:otherChatData="otherChatData"
			@changeOtherChat="changeOtherChat"
			@sendMessage="sendMessage"
			@pushSelfMsg="pushSelfMsg"
		></PrivateChat>
	</div>
</template>

<script>
import axios from 'axios'
import LoginBox from '../components/LoginBox'
import PrivateChat from '../components/PrivateChat'
// import store from '../store'
export default {
	data() {
		return {
			text: '',
			text_input: '',
			msgList: [],
			showbox: true,
			showOtherChat: false,
			// 私聊相关聊天数据
			otherChatData: {},
			// 未读消息列表
			unreadList: [],
		}
	},

	components: {
		LoginBox: LoginBox,
		PrivateChat: PrivateChat,
	},

	computed: {
		userinfo() {
			return this.$store.state.userinfo
		},
		token() {
			return this.$store.state.token
		},
	},

	watch: {
		token(newvalue) {
			console.log('聊天室token监听')
			console.log(newvalue)
			// this.$store.dispatch('tryAutoLogin', newvalue)
			if (newvalue) {
				this.initWebSocket()
			}
		},
	},

	mounted() {
		// this.autoLogin()

		this.getData()
		if (localStorage.getItem('token')) {
			this.initWebSocket()
		}
	},
	methods: {
		openOtherChat(other) {
			this.showOtherChat = true
			this.otherChatData = other
			// this.otherChatData.data = []

			this.unreadList.forEach((obj, index) => {
				if (obj == other) {
					this.unreadList.splice(index, 1)
				}
			})
		},
		pushSelfMsg(text) {
			this.otherChatData.data.push(text)
		},

		// 控制login窗口
		changeLogin(onoff) {
			this.showbox = onoff
		},
		// 控制私聊窗口
		changeOtherChat(onoff) {
			this.showOtherChat = onoff
		},
		// 快捷键发送信息 监听键盘输入
		enterSendMsg() {
			// 监听socket状态
			console.log(this.websocket)
			if (this.websocket.readyState == 3) {
				this.initWebSocket()
				return
			}
			let msg = {
				code: 200,
				message: {
					token: localStorage.getItem('token'),
					data: {
						text: this.text_input,
					},
				},
			}
			this.sendMessage(msg)
			this.text_input = ''
		},
		// 自动登录
		autoLogin() {
			// let userinfo = {
			// 	headImg: 'http://127.0.0.1:9000/upload/admin.jpg',
			// 	nickName: 'alienware',
			// }
			// this.$store.commit('saveUserinfo', userinfo)
			this.$store.dispatch('tryAutoLogin', localStorage.getItem('token'))
		},

		// 发送按钮
		clickto() {
			console.log(this.text_input)
			// this.msgList.push(this.text_input)

			let msg = {
				code: 200,
				message: {
					token: localStorage.getItem('token'),
					data: {
						text: this.text_input,
					},
				},
			}
			this.sendMessage(msg)
		},
		// 获取数据
		getData() {
			axios({
				method: 'get',
				url: 'http://127.0.0.1:9000/api/',
			}).then((res) => {
				console.log(res)
				this.text = res.data.test
			})
		},

		// 初始化WebSocket
		initWebSocket() {
			this.websocket = new WebSocket(
				'ws://127.0.0.1:9000/chat/myroom/' + this.userinfo.id + '/'
			)
			// console.log(this.websocket)
			this.websocket.onopen = this.onOpen
			this.websocket.onmessage = this.onMessage
			this.websocket.onerror = this.onError
			this.websocket.onclose = this.onClose
		},
		// 打开链接
		onOpen(e) {
			console.log('打开链接')
			console.log(e)

			let msg = {
				code: 100,
				message: {
					token: localStorage.getItem('token'),
					data: {
						text: '进入房间成功',
					},
				},
			}
			this.sendMessage(msg)
		},
		// 报错
		onError() {},
		// 接收信息
		onMessage(e) {
			// console.log(e)
			let message = JSON.parse(e.data).message
			console.log(message)

			if (message.code == 100 || message.code == 200) {
				this.showbox = false
				let msg_item = {
					nickName: message.nickName,
					headImg: message.headImg,
					data: [message.data],
					id: message.id,
				}
				this.msgList.push(msg_item)
				// 操作DOM
				let list_dom = document.getElementById('message-list')
				this.$nextTick(() => {
					list_dom.scrollTop = list_dom.scrollHeight
				})
			}

			if (message.code == 201) {
				if (this.showOtherChat) {
					// console.log(this.otherChatData)
					if (this.otherChatData.id == message.from) {
						this.otherChatData.data.push(message.data)
						// 操作DOM
						let list_dom = document.getElementById('message-list-private')
						this.$nextTick(() => {
							list_dom.scrollTop = list_dom.scrollHeight
						})
					}
				} else {
					if (this.unreadList.length == 0) {
						let msg_item = {
							nickName: message.nickName,
							headImg: message.headImg,
							data: [message.data],
							id: message.id,
							from: message.from,
						}
						this.unreadList.push(msg_item)
					} else {
						for (let i = 0; i < this.unreadList.length; i++) {
							if (this.unreadList[i].from == message.from) {
								this.unreadList[i].data.push(message.data)
								return
							}
						}
						let msg_item = {
							nickName: message.nickName,
							headImg: message.headImg,
							data: [message.data],
							id: message.id,
							from: message.from,
						}
						this.unreadList.push(msg_item)
					}
				}
			}
		},
		// 发送信息
		sendMessage(msg) {
			let text_data = JSON.stringify(msg)
			this.websocket.send(text_data)
		},
		// 关闭
		onClose(e) {
			console.log(e)
			this.showbox = true
		},
	},
}
</script>

<style scoped>
#page-box {
	width: 300px;
	/* height: 600px; */
	box-shadow: 0 2px 12px 0 #00000060;
	margin: 0 auto;
}

#logo {
	background: #00000080;
	color: white;
	font-size: 12px;
	text-align: center;
	padding: 10px;
	height: 130px;
}

#logo img {
	width: 80px;
	height: 80px;
}

#unread {
	height: 80px;
	background: #00000060;
	display: flex;
	justify-content: start;
	align-content: center;
	overflow-x: scroll;
}

#unread .unread-msg {
	position: relative;
	margin: 0 5px;
}

#unread img {
	height: 60px;
	height: 60px;
	border-radius: 30px;
	box-shadow: 0 2px 4px 0 #00000080;
}

#unread span {
	padding: 5px;
	background-color: #ff0000;
	color: #fff;
	border-radius: 30px;
	position: absolute;
	top: 0;
	right: 0;
}

.other {
	cursor: pointer;
}

#userinfo {
	display: flex;
	align-items: center;
	padding: 10px;
}

#userinfo img {
	width: 30px;
	border-radius: 15px;
}
</style>
