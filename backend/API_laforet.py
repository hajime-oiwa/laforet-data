from flask import Blueprint, jsonify
from flask_restful import Api, Resource
import sqlalchemy
import pandas as pd
import numpy as np
import requests
import json
import pymysql.cursors
import urllib.parse
from get_urls import get_url_table
from reg_urls import reg_url_table
from get_salesdata import get_sales_list
from get_laforet_data import get_laforet_table
from available_year_month import get_available_period

api_reg_laforet_data = Blueprint('get_data', __name__, url_prefix='/api')

class laforetData(Resource):
    def get(self, url_list=[]):
        url_list = url_list.replace("slash", "/")
        url_list = url_list.replace("sharp", "#")
        url_list = eval(url_list)

        df_monthly = get_laforet_table(url_list)

        return jsonify(f"{len(df_monthly)}件の売上データを追加しました")

class SalesData(Resource):
    def get(self, get_year, get_month):
        total_sales_list = get_sales_list(get_year, get_month)
        return total_sales_list

class GetUrlTeble(Resource):
    def get(self):
        urls = get_url_table()
        return urls
    
class RegUrlTeble(Resource):
    def get(self, url_list):
        url_list = url_list.replace("slash", "/")
        url_list = url_list.replace("sharp", "#")
        url_list = eval(url_list)
        reg_url_table(url_list)
        return "URLを更新しました"
    
class GetAvailablePeriod(Resource):
    def get(self):
        period = get_available_period()
        return period

api = Api(api_reg_laforet_data)


api.add_resource(laforetData, '/laforetdata/<url_list>')
api.add_resource(SalesData, '/SalesData/<get_year>/<get_month>')
api.add_resource(GetUrlTeble, '/geturl')
api.add_resource(RegUrlTeble, '/regurl/<url_list>')
api.add_resource(GetAvailablePeriod, '/period')