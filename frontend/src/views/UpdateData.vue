<!DOCTYPE html>

<head>
<meta charset="utf-8">
</head>

<script>

const axios = require('axios').create()

export default {
  data () {
    return {
      urls: [],
      newurl: {
        year: '', month: '', url: ''
      },
      showmodal: false,
      modalcontent: '',
      apiurl: ''
    }
  },
  mounted () {
    this.GetURLs()
  },

  methods: {
    add_urls: async function () {
      this.urls.push([Number(this.newurl.year), Number(this.newurl.month), this.newurl.url])
      this.newurl = {
        year: '', month: '', url: ''
      }
      this.apiurl = '/api/regurl/' + JSON.stringify(this.urls).split('/').join('slash').split('#').join('sharp')
      const response = await axios.get(this.apiurl)
      this.GetURLs()
      this.apiurl = ''
      this.modalcontent = response.data
      this.showmodal = true
    },

    clear_url: async function (row) {
      this.urls = this.urls.filter(t => t !== row)
      this.apiurl = '/api/regurl/' + JSON.stringify(this.urls).split('/').join('slash').split('#').join('sharp')
      await axios.get(this.apiurl)
      this.GetURLs()
      this.apiurl = ''
      this.modalcontent = 'URLを1件消去しました'
      this.showmodal = true
    },

    CloseModal () {
      this.showmodal = false
    },

    GetURLs: async function () {
      const response = await axios.get('/api/geturl')
      this.urls = response.data
    },

    UpdateSalesData: async function () {
      this.apiurl = '/api/laforetdata/' + JSON.stringify(this.urls).split('/').join('slash').split('#').join('sharp')
      const response = await axios.get(this.apiurl)
      this.apiurl = ''
      this.modalcontent = response.data
      this.showmodal = true
    }
  }
}
</script>

<template>
    <div id="app">
        <p>
            <button @click="UpdateSalesData">売上データ更新</button>
        </p>
        <p></p>
        <p>
            <button v-if="newurl.year && newurl.month && newurl.url" @click="add_urls">URL更新</button>
            <button v-else :disabled="1">URL更新</button>
        </p>
        <div id="overlay" v-show="showmodal">
            <div id="content" v-show="showmodal">
                <p>{{modalcontent}}</p>
                <p><button @click="CloseModal">閉じる</button></p>
            </div>
        </div>
    </div>

    <table border="1" align="center">
        <thead>
            <tr>
                <th>年</th>
                <th>月</th>
                <th>URL</th>
                <th></th>
            </tr>
        </thead>

        <tbody>
            <tr v-for="row in urls" :key="row[2]">
                <th>{{ row[0] }}</th>
                <th>{{ row[1] }}</th>
                <th><input v-model=row[2] size="150"></th>
                <th>
                  <button @click=clear_url(row)>クリア</button>
                </th>
            </tr>

            <tr>
                <th><input v-model=newurl.year></th>
                <th><input v-model=newurl.month></th>
                <th><input v-model=newurl.url size="150"></th>
                <th></th>
            </tr>
        </tbody>
    </table>
</template>

<style>
#overlay{
  z-index:1;

  position:fixed;
  top:0;
  left:0;
  width:100%;
  height:100%;
  background-color:rgba(0,0,0,0.5);

  display: flex;
  align-items: center;
  justify-content: center;

}

#content{
  z-index: 2;
  width:30%;
  padding:1em;
  background: #fff;
}
</style>
