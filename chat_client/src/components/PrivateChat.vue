<template>
	<div v-if="ShowBox" id="page">
		<div id="chatbox">
			<div @click="exitChat" id="close">X</div>
			<div id="otherinfo">
				<img
					:src="'http://127.0.0.1:9000/upload/' + otherChatData.headImg"
					alt=""
				/>
				<span>{{ otherChatData.nickName }}</span>
			</div>

			<div id="message-list-private">
				<div v-for="(item, index) in otherChatData.data" :key="index">
					<div v-if="item.to" class="other message">
						<img
							:src="'http://127.0.0.1:9000/upload/' + otherChatData.headImg"
							alt=""
						/>
						<div class="nickname">{{ otherChatData.nickName }}</div>
						<div class="msgtext">{{ item.text }}</div>
					</div>

					<div v-else class="self message">
						<img :src="userinfo.headImg" alt="" />
						<div class="nickname">{{ userinfo.nickName }}</div>
						<div class="msgtext">{{ item.text }}</div>
					</div>
				</div>
			</div>

			<div id="text-input">
				<textarea
					@keydown.enter="enterSendMsg()"
					v-model="text_input"
					cols="30"
					rows="10"
				></textarea>
				<button>send</button>
			</div>
		</div>
	</div>
</template>

<script>
export default {
	props: {
		ShowBox: Boolean,
		otherChatData: Object,
	},
	data() {
		return {
			text_input: '',
		}
	},
	computed: {
		userinfo() {
			return this.$store.state.userinfo
		},
	},
	methods: {
		enterSendMsg() {
			let msg = {
				code: 201,
				message: {
					token: localStorage.getItem('token'),
					data: {
						to: this.otherChatData.id,
						text: this.text_input,
					},
				},
			}
			this.$emit('sendMessage', msg)
			this.$emit('pushSelfMsg', { text: this.text_input })

			// 操作DOM
			let list_dom = document.getElementById('message-list-private')
			this.$nextTick(() => {
				list_dom.scrollTop = list_dom.scrollHeight
			})
			this.text_input = ''
			// console.log(this.otherChatData)
		},
		exitChat() {
			this.$emit('changeOtherChat', false)
		},
	},
}
</script>

<style scoped>
#page {
	width: 100vw;
	height: 100vh;
	background: #00000060;
	position: absolute;
	top: 0;
	left: 0;
	display: flex;
	justify-content: center;
	align-items: center;
}

#chatbox {
	width: 600px;
	/* height: 400px; */
	background: #fff;
	position: relative;
}

#otherinfo {
	background: #00000080;
	height: 80px;
	display: flex;
	justify-content: center;
	align-items: center;
}

#otherinfo img {
	width: 60px;
	height: 60px;
	border-radius: 30px;
}

#otherinfo span {
	font-size: 20px;
	font-weight: 700;
	color: #fff;
}

#close {
	width: 60px;
	height: 60px;
	background-color: #ccc;
	color: #fff;
	font-size: 40px;
	font-weight: 700;
	border-radius: 30px;
	text-align: center;
	line-height: 60px;
	position: absolute;
	right: 0;
	cursor: pointer;
}

#message-list-private {
	height: 370px;
	background: #00000030;
	padding: 10px;
	overflow-y: scroll;
}

.message {
	/* width: 120px; */
	background: #f5cb13;
	text-align: center;
	margin-top: 10px;
	padding: 5px;
	border-radius: 10px;
	font-size: 18px;
	font-weight: 700;
	color: #00000080;
	word-break: break-all;
	/* word-wrap: break-word; */
}

.message img {
	width: 30px;
	height: 30px;
	border-radius: 15px;
	float: left;
	margin: 5px;
}

.nickname {
	text-align: left;
}

.msgtext {
	text-align: left;
}

.self {
	background: #5acf23;
}

.self img {
	float: right;
}

.self .nickname {
	text-align: right;
}

.self .msgtext {
	text-align: right;
}

#text-input {
	height: 70px;
	background: #00000010;
	display: flex;
	justify-content: center;
	align-items: center;
}

#text-input textarea {
	width: 100%;
	height: 60px;
}

#text-input button {
	width: 100px;
	height: 70px;
	background: #f5cb13;
	border: none;
	border-radius: 15px;
	font-size: 18px;
	font-weight: 700;
	color: #00000080;
}

#text-input button:hover {
	background: #836f15;
}
</style>
