<template>
	<div id="reset-bg">
		<div id="reset-box">
			<div class="header">
				重置密码
				<el-divider></el-divider>
			</div>
			<el-form :label="labelPosition" label-width="70px">
				<el-form-item label="用户名" size="default">
					<el-input v-model="username" placeholder="input username"></el-input>
				</el-form-item>
				<el-form-item label="密码" size="default">
					<el-input v-model="password" placeholder="reset password "></el-input>
				</el-form-item>
				<el-form-item label="重复密码" size="default">
					<el-input v-model="repassword" placeholder="repeat it"></el-input>
				</el-form-item>
				<el-form-item label="">
					<el-button type="danger" @click="userRegister()">重置</el-button>
					<el-button type="warning" @click="toLogin">取消</el-button>
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
					message: '用户名或密码不能为空！',
					type: 'error',
				})
				return
			}
			if (this.password != this.repassword) {
				this.$notify({
					title: 'Error',
					message: '两次密码输入不一致',
					type: 'error',
				})
				return
			}
			if (this.password.length < 8) {
				this.$notify({
					title: 'Error',
					message: '密码太短',
					type: 'error',
				})
				return
			}
			// 重新提交密码
			axios({
				method: 'post',
				url: 'http://127.0.0.1:9000/api-json/dchat-resetPwd/',
				data: Qs.stringify({
					username: this.username,
					password: this.password,
					repassword: this.repassword,
				}),
			}).then((res) => {
				console.log(res.data)
				if (res.data == 'user not exist') {
					this.$notify({
						title: 'Error',
						message: '用户不存在！',
						type: 'error',
					})
					return
				} else {
					this.$store.commit('saveUserinfo', res.data)
					this.$notify({
						title: 'Success',
						message: '修改成功',
						type: 'success',
					})
					this.$router.push({ name: 'Login' })
				}
			})
		},
	},
}
</script>

<style scoped>
#reset-bg {
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

#reset-box {
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
