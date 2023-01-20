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
					}
				})
		},
	},
	{
		path: '/about',
		name: 'About',
		// route level code-splitting
		// this generates a separate chunk (about.[hash].js) for this route
		// which is lazy-loaded when the route is visited.
		component: () =>
			import(/* webpackChunkName: "about" */ '../views/About.vue'),
	},
]

const router = createRouter({
	history: createWebHashHistory(),
	routes,
})

export default router
