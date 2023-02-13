import { createStore } from 'vuex'
import Qs from 'qs'
import axios from 'axios'
import router from '../router'
// import { ELNotification } from 'element-plus'

const HostURL = 'http://127.0.0.1:9000'

export default createStore({
	state: {
		userinfo: {
			headImg: null,
			nickName: null,
		},
		token: null,
	},
	getters: {
		// 查询登录状态
		isnotUserLogin(state) {
			return state.token
		},
	},
	mutations: {
		saveUserinfo(state, userinfo) {
			state.userinfo = userinfo
		},
		setToken(state, token) {
			state.token = token
			console.log(state.token)
		},
		// 清空用户登录状态
		clearToken(state) {
			state.token = ''
		},
	},
	actions: {
		// 自动登录
		async tryAutoLogin({ commit }, token) {
			console.log('----actions---vuex---自动登录')
			let loginType = false
			await axios({
				method: 'post',
				url: HostURL + '/api-json/userinfo/',
				data: Qs.stringify({
					token: token,
				}),
			}).then((res) => {
				let userinfo = res.data
				console.log(res.data)
				if (userinfo.nickName.length > 0) {
					userinfo.headImg = HostURL + userinfo.headImg
					loginType = true
				}
				commit('saveUserinfo', userinfo)
			})

			return loginType
		},
		// 退出登录
		userLogout({ commit }) {
			// 取浏览器缓存的token
			let token = localStorage.getItem('token')
			axios({
				url: HostURL + '/api-json/dchat-logout/',
				method: 'post',
				data: Qs.stringify({ token }),
			}).then((res) => {
				console.log(res.data)
				// 清除vuex里的token
				commit('clearToken')
				// 清空缓存
				localStorage.removeItem('token')
				// this.$notify({
				// 	title: 'Success',
				// 	message: '登出成功',
				// 	type: 'success',
				// })
				router.push({ name: 'Login' })
			})
		},
	},
	modules: {},
})
