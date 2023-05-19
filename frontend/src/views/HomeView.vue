<!DOCTYPE html>

<head>
<meta charset="utf-8">
</head>

<script>

const axios = require('axios').create()

export default {
  data () {
    return {
      sales_data: [],
      period: [],
      selected_year: '全期間',
      selected_month: '全期間',
      apiurl: ''
    }
  },

  mounted () {
    this.GetPeriod()
  },

  methods: {
    UpdateSalesData: async function () {
      this.apiurl = '/api/SalesData/' + this.selected_year + '/' + this.selected_month
      const response = await axios.get(this.apiurl)
      this.apiurl = ''
      this.sales_data = response.data
    },

    GetPeriod: async function () {
      const response = await axios.get('/api/period')
      this.period = response.data
    }
  }
}
</script>

<template>
    <p>年：
      <select v-model="selected_year">
          <option v-for="row in Object.keys(period)" :key="row">
            {{ row }}
          </option>
      </select>
      月：
      <select v-model="selected_month">
          <option v-for="month in period[selected_year]" :key=month>
            {{ month }}
          </option>
      </select>
    </p>
    <button @click="UpdateSalesData">データ表示</button>
    <table border="1" align="center">
        <thead>
            <tr>
                <th width="400px">商品名</th>
                <th width="100px">売数</th>
                <th width="100px">売上</th>
            </tr>
        </thead>

        <tbody>
            <tr v-for="sales in sales_data" :key="sales[0]">
                <th>{{ sales[0] }}</th>
                <th>{{ sales[1] }}</th>
                <th>{{ sales[2] }}</th>
            </tr>
        </tbody>
    </table>
</template>

<style>

select {
  width: 80px;
  text-align: center;
}

</style>
