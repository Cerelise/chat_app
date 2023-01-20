<template>
	<router-view></router-view>
</template>

<script>
export default {
	computed: {
		token() {
			return this.$store.state.token
		},
	},
	watch: {
		token(newvalue, oldvalue) {
			console.log('----token监听')
			console.log(newvalue, oldvalue)
			this.$store.dispatch('tryAutoLogin', newvalue)
		},
	},
	mounted() {},
}
</script>
