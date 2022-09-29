import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
import acquire

def set_index(df):
    df.sale_date = df.sale_date.str.replace('00:00:00 GMT', '')
    df.sale_date = pd.to_datetime(df.sale_date, format='%a, %d %b %Y ')
    df = df.set_index('sale_date')
    return df

def plot_hist(df):
    df.sale_amount.hist()
    plt.title('distribution of sale_amount')
    plt.show()

    df.item_price.hist()
    plt.title('distribution of item_price')
    plt.show()

def add_m_and_d(df):
    df['month'] = df.index.month_name()
    df['day_of_week'] = df.index.day_name()
    return df

def add_sales_total(df):
    df['sales_total'] = df.sale_amount * df.item_price
    return df

def prepare_store(df):
    df = set_index(df)
    plot_hist(df)
    df = add_m_and_d(df)
    df = add_sales_total(df)
    return df






def get_electric():
    url = 'https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv'
    OPS_data = pd.read_csv(url)
    return OPS_data

def electric_index(df):
    df.Date = pd.to_datetime(df.Date)
    df = df.set_index('Date')
    return df

def plot_electric_(df):
    for col in df.columns:
        df[col].hist()
        plt.title(f'Distribution of {col}')
        plt.show()

def add_electric_m_and_d(df):
    df['month'] = df.index.month_name()
    df['day_of_week'] = df.index.day_name()
    return df

def fill_missing(df):
    df = df.fillna(0)
    return df

def wrangle_electric():
    df = get_electric()
    df = electric_index(df)
    plot_electric_(df)
    df = add_electric_m_and_d(df)
    df = fill_missing(df)
    return df


