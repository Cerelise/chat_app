<template>
	<div id="reg-bg">
		<div id="reg-box">
			<div class="header">
				新用户注册
				<el-divider></el-divider>
			</div>
			<el-form :label="labelPosition" label-width="70px">
				<el-form-item label="用户名" size="default">
					<el-input
						v-model="username"
						placeholder="create your account"
					></el-input>
				</el-form-item>
				<el-form-item label="密码" size="default">
					<el-input
						v-model="password"
						placeholder="input your password"
					></el-input>
				</el-form-item>
				<el-form-item label="重复密码" size="default">
					<el-input
						v-model="repassword"
						placeholder="repeat your password"
					></el-input>
				</el-form-item>
				<el-form-item label="">
					<el-button type="primary" @click="userRegister()">注册</el-button>
					<el-button type="warning" @click="toLogin"
						>已有账号？去登录</el-button
					>
				</el-form-item>
			</el-form>
		</div>
	</div>
</template>

<script>
import axios from 'axios'
import Qs from 'qs'
export default {
	data() {
		return {
			labelPosition: 'right',
			username: '',
			password: '',
			repassword: '',
		}
	},
	methods: {
		toLogin() {
			this.$router.push({ name: 'Login' })
		},
		userRegister() {
			if (
				this.username.length == 0 ||
				this.password.length == 0 ||
				this.repassword.length == 0
			) {
				this.$notify({
					title: 'Error',
					message: '表单未填写完整',
					type: 'error',
				})
				return
			}
			if (this.password != this.repassword) {
				// alert('两次密码不一致')
				this.$notify({
					title: 'Error',
					message: '两次密码输入不一致',
					type: 'error',
				})
				return
			}
			if (this.password.length < 8) {
				// alert('密码太短')
				this.$notify({
					title: 'Error',
					message: '密码太短',
					type: 'error',
				})
				return
			}
			// 提交注册
			axios({
				method: 'post',
				url: 'http://127.0.0.1:9000/api-json/dchat-register/',
				data: Qs.stringify({
					username: this.username,
					password: this.password,
					repassword: this.repassword,
				}),
			}).then((res) => {
				console.log(res.data)
				this.$store.commit('saveUserinfo', res.data)
				this.$notify({
					title: 'Success',
					message: '注册成功，将自动跳转至登录界面',
					type: 'success',
				})
				this.$router.push({ name: 'Login' })
			})
		},
	},
}
</script>

<style scoped>
#reg-bg {
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

#reg-box {
	width: 300px;
	text-align: center;
	background: #979797;
	padding: 10px;
	box-shadow: 0 2px 12px 0 #00000020;
}

.header {
	/* text-align: center; */
	font-size: 20px;
	font-weight: 600;
}
</style>
