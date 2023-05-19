import sqlalchemy
import pandas as pd

def get_sales_list(get_year, get_month):
    if get_month == "全期間":
        get_month = None
    else:
        get_year = int(get_year)
        get_month = int(get_month)

    user = "root"
    password = "h3470obobby"
    host = "localhost"
    port = "3306"
    database = "sales_DB"
    url = f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'

    engine = sqlalchemy.create_engine(url)

    sql_query = 'select * from sales'

    df = pd.read_sql(sql=sql_query, con=engine)

    if get_month:
        df_amount = df[(pd.to_datetime(df["sales_date"]).dt.month == get_month) * (pd.to_datetime(df["sales_date"]).dt.year == get_year)].groupby("product_name").amount.sum().reset_index()
        df_quantity = df[(pd.to_datetime(df["sales_date"]).dt.month == get_month) * (pd.to_datetime(df["sales_date"]).dt.year == get_year)].groupby("product_name").quantity.sum().reset_index()
    else:
        df_amount = df.groupby("product_name").amount.sum().reset_index()
        df_quantity = df.groupby("product_name").quantity.sum().reset_index()

    df_total = pd.merge(df_quantity, df_amount, on="product_name", how="inner")
    total_list = df_total.to_numpy().tolist()

    return total_list