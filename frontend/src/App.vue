<template>
  <img :src="imgPath" style="width: 20%; height: 20%">
  <nav>
    <router-link to="/">データを見る</router-link> |
    <router-link to="/updatedata">データを更新する</router-link>
  </nav>
  <router-view/>
</template>

<script>
export default {
  data () {
    return {
      imgPath: '../static/img/kanchigai2.jpg'
    }
  }
}
</script>

<style>

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>
