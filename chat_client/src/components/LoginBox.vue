<template>
	<div v-if="ShowBox" id="login-box">
		<div id="form">
			<h1>登录</h1>
			<div class="form-item">
				<input v-model="username" type="text" placeholder="Username" />
			</div>
			<div class="form-item">
				<input v-model="password" type="text" placeholder="Password" />
			</div>
			<div class="form-item">
				<button @click="userLogin">登录</button>
			</div>
		</div>
	</div>
</template>

<script>
import axios from 'axios'
import Qs from 'qs'
import swal from 'sweetalert'
export default {
	name: 'LoginBox',
	props: {
		ShowBox: Boolean,
	},
	data() {
		return {
			username: '',
			password: '',
			showBox: false,
		}
	},

	mounted() {},

	methods: {
		userLogin() {
			console.log(this.username + ' ' + this.password)
			axios({
				method: 'post',
				url: 'http://127.0.0.1:9000/api-json/login/',
				data: Qs.stringify({
					username: this.username,
					password: this.password,
				}),
			}).then((res) => {
				console.log(res.data)
				if (res.data == 'user none') {
					alert('用户名不存在')
				}
				if (res.data == 'pwd err') {
					alert('密码错误')
				}
				localStorage.setItem('token', res.data)
				// alert('登录成功')
				// 11
				swal({
					title: '成功',
					content: '',
					icon: 'success',
					buttons: {
						confirm: {
							text: '确定',
							value: true,
							visible: true,
						},
						cancel: {
							text: '取消',
							value: true,
							visible: false,
						},
					},
				}).then((willHidden) => {
					if (willHidden) {
						// this.ShowBox = false
						// 事件
						this.$emit('changeLogin', false)
						// 控制BOM刷新页面
						// window.location.reload()
						// 方法
						this.$store.commit('setToken', res.data)
						return
					}
				})
			})
		},
	},
}
</script>

<style scoped>
#login-box {
	width: 100vw;
	height: 100vh;
	background: #00000080;
	position: fixed;
	top: 0;
	left: 0;
	display: flex;
	justify-content: center;
	align-items: center;
}

#form {
	width: 300px;
	text-align: center;
	background: #979797;
	padding: 10px;
	box-shadow: 0 2px 12px 0 #00000020;
}

#form h1 {
	color: #fff;
}
.form-item {
	margin-top: 5px;
}
.form-item button {
	width: 120px;
	height: 30px;
	font-size: 18px;
	font-weight: 700;
	color: #fff;
	background: #f5cb13;
	border: none;
	border-radius: 10px;
}
</style>
