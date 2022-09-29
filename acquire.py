import numpy as np
import pandas as pd
import requests
import os

def get_items(url='https://python.zgulde.net/api/v1/items?page=1'):

    max_page = requests.get(url).json()['payload']['max_page'] + 1
    for i in range(1,max_page):
        url = url[:-1] + str(i)
        if i == 1:
            output = pd.DataFrame(requests.get(url).json()['payload']['items'])
        else:
            output = pd.concat([output, pd.DataFrame(requests.get(url).json()['payload']['items'])], 
                               ignore_index=True)
    return output




def get_stores(url='https://python.zgulde.net/api/v1/stores'):

    return pd.DataFrame(requests.get(url).json()['payload']['stores'])


def get_sales(url = 'https://python.zgulde.net/api/v1/sales?page='):
  
    max_page = requests.get(url+'1').json()['payload']['max_page'] + 1
    for i in range(1,max_page):
        new_url = url + str(i)
        if i == 1:
            output = pd.DataFrame(requests.get(new_url).json()['payload']['sales'])
        else:
            output = pd.concat([output, pd.DataFrame(requests.get(new_url).json()['payload']['sales'])], 
                               ignore_index=True)
    return output

def combined(sales, stores, items):
 
    both = sales.merge(items, left_on='item', right_on='item_id')
    both = both.merge(stores, left_on='store', right_on='store_id')
    both.drop(columns=['item', 'store'], inplace=True)

    return both

def superstore():
    
    filename = 'sales.csv'
    if os.path.isfile(filename):
        return pd.read_csv(filename)

    else:
        sales = get_sales()
        stores = get_stores()
        items = get_items()
        
        df = combined(sales, stores, items)

        df.to_csv(filename, index=False)
    
    return df




def get_electric():
 
    return pd.read_csv('https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv')

