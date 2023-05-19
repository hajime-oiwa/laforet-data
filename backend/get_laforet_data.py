from flask import jsonify
import sqlalchemy
import pandas as pd
import numpy as np
import requests
import json
import pymysql.cursors

def get_laforet_table(url_list=[]):

    df_monthly = pd.DataFrame({})

    #データベースの最新レコード取得
    user = "xxxx"
    password = "xxxx"
    host = "xxxx"
    port = "xxxx"
    database = "xxxx"
    url = f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'

    engine = sqlalchemy.create_engine(url)
    sql_query = 'select max(sales_date) from sales'

    try:
        result = pd.read_sql(sql=sql_query, con=engine)

        last_year = int(pd.to_datetime(result["max(sales_date)"]).dt.year.values[0])
        last_month = int(pd.to_datetime(result["max(sales_date)"]).dt.month.values[0])
        last_date = pd.to_datetime(result["max(sales_date)"])[0]
    except:
        last_year = 2023
        last_month = 2
        last_date = "2023-01-01 00:00:00"


    #最新レコードの日付から、取得対象の愛と狂気スプレッドシートURLをリスト化

    search_url_list = [url_list[i] for i in range(len(url_list)) if url_list[i][0] >= last_year and url_list[i][1] >= last_month]
    api_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

    #愛と狂気のデータ取得

    for i in range(len(search_url_list)):

        url = search_url_list[i][2]

        sheet_id = url[url.find("/d/")+3:url.find("/edit")]
        url_get = "https://sheets.googleapis.com/v4/spreadsheets/" + sheet_id + "/values/%E6%97%A5%E5%88%A5%E5%A3%B2%E4%B8%8A!A5:G200?key=" + api_key

        res = requests.get(url_get)

        sales_data = json.loads(res.text)

        data_list = [sales_data['values'][x] for x in range(len(sales_data['values'])) if sales_data['values'][x][1] != '#N/A']

        if data_list == []:
            continue

        data_np = np.array(data_list).T
        data_dict = {}
        df_columns = ["sales_date", "product_name", "unit_price", "quantity", "amount", "canceled"]

        for index in range(len(df_columns)):
            data_dict[df_columns[index]] = data_np[index+1]

        df_tmp = pd.DataFrame(data_dict)

        df_tmp["sales_date"] = pd.to_datetime(df_tmp["sales_date"])
        df_tmp["quantity"] = df_tmp["quantity"].str.replace(",", "").astype(int)
        df_tmp["unit_price"] = df_tmp["unit_price"].str.replace(",", "").astype(int)
        df_tmp["amount"] = df_tmp["amount"].str.replace(",", "").astype(int)

        if i != 0:
            df_monthly = pd.concat([df_monthly, df_tmp], axis=0)
        else:
            df_monthly = df_tmp

    #df_monthlyの中から、last_date以降のデータをデータベースに登録

    if len(df_monthly) == 0:
        return jsonify(f"エラー：最新のURLを入力してください{search_url_list}")
    else:
        df_monthly = df_monthly[df_monthly["sales_date"] > last_date]

    conn = pymysql.connect(host="xxxx",
            user="xxxx",
            password="xxxx",
            database="xxxx",
            cursorclass=pymysql.cursors.DictCursor)

    with conn:
        with conn.cursor() as cursor:
            sql = 'INSERT INTO sales (sales_date, product_name, unit_price, quantity, amount, canceled) VALUES(%s,%s,%s,%s,%s,%s)'
            cursor.executemany(sql, df_monthly.values.tolist())
        conn.commit()
        
    return df_monthly
