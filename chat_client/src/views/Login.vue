<template>
	<div id="login-bg">
		<div id="login-box">
			<div class="header">
				用户登录
				<el-divider></el-divider>
			</div>
			<el-form :label="labelPosition" label-width="70px">
				<el-form-item label="用户名" size="default">
					<el-input
						v-model="username"
						placeholder="input your account"
					></el-input>
				</el-form-item>
				<el-form-item label="密码" size="default">
					<el-input
						v-model="password"
						placeholder="input your password"
					></el-input>
				</el-form-item>
				<div style="display: flex; flex-direction: row-reverse">
					<router-link to="/reset-pwd" style="color: aqua"
						>忘记密码?</router-link
					>
					<!-- <a @click="toRestPwd" style="color: aqua">忘记密码?</a> -->
					<!-- <el-button @click.prevent="toResetPwd">忘记密码？</el-button> -->
				</div>
				<el-form-item style="margin-top: 10px">
					<el-button type="primary" @click="userLogin">登录</el-button>
					<el-button type="warning" @click="toRegister">注册</el-button>
				</el-form-item>
			</el-form>
		</div>
	</div>
</template>

<script>
import axios from 'axios'
import Qs from 'qs'
// import { ELNotification } from 'element-plus'
// import swal from 'sweetalert'
export default {
	data() {
		return {
			labelPosition: 'right',
			username: this.username,
			password: this.password,
			// showBox: false,
		}
	},

	mounted() {},

	methods: {
		toRegister() {
			this.$router.push({ name: 'Register' })
		},
		toResetPwd() {
			this.$router.push({ name: 'ResetPwd' })
		},
		userLogin() {
			// console.log(this.formValue.username, this.formValue.password)
			// let formValue = this.formValue
			axios({
				method: 'post',
				url: 'http://127.0.0.1:9000/api-json/dchat-login/',
				data: Qs.stringify({
					username: this.username,
					password: this.password,
				}),
			}).then((res) => {
				console.log(res.data)
				if (res.data == 'user none') {
					// alert('用户名不存在')
					this.$notify({
						title: 'Error',
						message: '用户名不存在！',
						type: 'error',
					})
					return
				}
				if (res.data == 'pwd err') {
					// alert('密码错误')
					this.$notify({
						title: 'Error',
						message: '密码错误',
						type: 'error',
					})
					return
				}
				localStorage.setItem('token', res.data)
				this.$store.commit('setToken', res.data)
				// alert('登录成功')
				this.$notify({
					title: 'Success',
					message: '登录成功',
					type: 'success',
				})
				this.$router.push({ name: 'Chat' })
			})
		},
	},
}
</script>

<style scoped>
#login-bg {
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

#login-box {
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
