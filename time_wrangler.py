import pandas as pd
from datetime import timedelta, datetime
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import warnings
warnings.filterwarnings("ignore")


def get_mcity_data():
    glt_mcity = pd.read_csv('GlobalLandTemperaturesByMajorCity.csv')
    return glt_mcity

def get_mexico(mexico_data):
    
    get_mcity_data(glt_mcity)
    mexico_data = glt_mcity[glt_mcity['City'] == 'Mexico'] 
    mexico_data.dt= pd.to_datetime(mexico_data.dt)
    mexico_data = mexico_data.reset_index()
    mexico_data = mexico_data.replace(to_replace="Mexico", value="Mexico City, Mexico")
    mexico_data = mexico_data.drop(['index','Latitude','Longitude','Country'], axis=1)
    mexico_data = mexico_data.round(2)
    mexico_data = mexico_data.rename(columns = {"dt": "Year_Month","AverageTemperature":"Avg_Temp", "AverageTemperatureUncertainty":"Avg_Temp_Uncerty"})
    mexico_data = mexico_data[(mexico_data['Year_Month'].dt.year != 2013)]
    mexico_data = mexico_data.set_index('Year_Month')
    return mexico_data


def get_berlin(df):
    df = df[df['City'] == 'Berlin'] 
    df = df.reset_index()
    df = df.replace(to_replace="Berlin", value="Berlin, Germany")
    df = df.drop(['index','Latitude','Longitude','Country'], axis=1)
    df = df.round(2)
    df = df.rename(columns = {"dt": "Year_Month","AverageTemperature":"Avg_Temp", "AverageTemperatureUncertainty":"Avg_Temp_Uncerty"})
    df.Year_Month= pd.to_datetime(df.Year_Month)
    df = df[(df['Year_Month'].dt.year != 2013)]
    df = df[(df['Year_Month'].dt.year >= 1835)]
    df = df.set_index('Year_Month')
    return df


def split_vis(df):
    df = df.drop(['City'], axis=1)

    train_size = int(len(df) * .5)
    validate_size = int(len(df) * .3)
    test_size = int(len(df) - train_size - validate_size)
    validate_end_index = train_size + validate_size

# split into train, validation, test
    train_size = df[: train_size]
    validate = df[train_size : validate_end_index]
    test = df[validate_end_index : ]
    
    for col in train.columns:
        plt.figure(figsize=(12,4))
        plt.plot(train[col])
        plt.plot(validate[col])
        plt.plot(test[col])
        plt.ylabel(col)
        plt.title(col)
        plt.show()
    
    return  train, validate, test
    
    
    
def evaluate(target_var):
    rmse = round(sqrt(mean_squared_error(validate[target_var], yhat_df[target_var])), 0)
    return rmse

def plot_and_eval(target_var):
    plt.figure(figsize = (12,4))
    plt.plot(train[target_var], label = 'Train', linewidth = 1)
    plt.plot(validate[target_var], label = 'Validate', linewidth = 1)
    plt.plot(yhat_df[target_var])
    plt.title(target_var)
    rmse = evaluate(target_var)
    print(target_var, '-- RMSE: {:.0f}'.format(rmse))
    plt.show()
    

# function to store rmse for comparison purposes
def append_eval_df(model_type, target_var):
    rmse = evaluate(target_var)
    d = {'model_type': [model_type], 'target_var': [target_var], 'rmse': [rmse]}
    d = pd.DataFrame(d)
    return eval_df.append(d, ignore_index = True)