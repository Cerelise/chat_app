import { createStore } from 'vuex'
import Qs from 'qs'
import axios from 'axios'

const HostURL = 'http://127.0.0.1:9000'

export default createStore({
	state: {
		userinfo: {
			headImg: null,
			nickName: null,
		},
		token: null,
	},
	mutations: {
		saveUserinfo(state, userinfo) {
			state.userinfo = userinfo
		},
		setToken(state, token) {
			state.token = token
		},
	},
	actions: {
		// 自动登录
		async tryAutoLogin({ commit }, token) {
			console.log('----actions---vuex---自动登录')

			let loginType = false

			await axios({
				method: 'post',
				url: 'http://127.0.0.1:9000/api-json/userinfo/',
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
	},
	modules: {},
})
