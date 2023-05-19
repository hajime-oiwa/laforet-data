import pandas as pd
import pymysql.cursors

def reg_url_table(url_list):
    conn = pymysql.connect(host="localhost",
            user="root",
            password="h3470obobby",
            database="sales_DB",
            cursorclass=pymysql.cursors.DictCursor)

    with conn:
        with conn.cursor() as cursor:
            sql = 'truncate table urls'
            cursor.execute(sql)
            sql = 'INSERT INTO urls (year, month, url) VALUES(%s,%s,%s)'
            cursor.executemany(sql, url_list)
        conn.commit()