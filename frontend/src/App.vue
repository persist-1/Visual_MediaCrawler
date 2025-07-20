<template>
  <div id="app">
    <!-- 营销页面不使用Layout包装 -->
    <router-view v-if="$route.path === '/intro'" />
    <!-- 其他页面使用Layout包装 -->
    <Layout v-else />
  </div>
</template>

<script>
import Layout from './components/Layout.vue'

export default {
  name: 'App',
  components: {
    Layout
  }
}</script>

<style>
/* 引入FontAwesome图标 */
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css');

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f5f5f5;
  color: #333;
}

#app {
  min-height: 100vh;
}
</style>