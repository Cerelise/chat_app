import { createRouter, createWebHashHistory } from 'vue-router'
import store from '../store'

const routes = [
	{
		path: '/',
		name: 'Chat',
		component: () => import('../views/Chat.vue'),
		beforeEnter(to, from, next) {
			// console.log(to, from)
			store
				.dispatch('tryAutoLogin', localStorage.getItem('token'))
				.then((loginType) => {
					console.log(loginType)
					if (loginType) {
						next()
						return
					}
				})
			// 浏览器缓存清空后，返回登录页面
			if (!localStorage.getItem('token')) {
				next('/login')
				return
			}
		},
	},
	// 登录
	{
		path: '/login',
		name: 'Login',
		component: () => import('../views/Login.vue'),
	},
	// 注册
	{
		path: '/register',
		name: 'Register',
		component: () => import('../views/Register.vue'),
	},
	// 用户密码重置
	{
		path: '/reset-pwd',
		name: 'ResetPwd',
		component: () => import('../views/ResetPwd.vue'),
	},
	// 	{
	// 		path: '/about',
	// 		name: 'About',
	// 		// route level code-splitting
	// 		// this generates a separate chunk (about.[hash].js) for this route
	// 		// which is lazy-loaded when the route is visited.
	// 		component: () =>
	// 			import(/* webpackChunkName: "about" */ '../views/About.vue'),
	// 	},
]

const router = createRouter({
	history: createWebHashHistory(),
	routes,
})

export default router
