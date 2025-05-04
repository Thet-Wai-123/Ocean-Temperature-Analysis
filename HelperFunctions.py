from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
import seaborn as sns
import matplotlib.dates as mdates
import plotly.express as px


#remove outliers and all that has -999 as value, outliers are considered with z score bigger than 2.
def clean_temp(df):
    df = df[(df != -999.0).all(1)]
    df = df[np.abs(stats.zscore(df['Anomaly_Temp_K'])) < 2]

#add a date in the dataframe that takes Year and Month
def add_date(df):
    df['Date'] = pd.to_datetime(df[['Year', 'Month']].assign(DAY=1))

#plot the data with best fit line
def plot_data_with_bestFitLine(df, x_col, y_col, xlabel, ylabel, title):
    df[x_col] = pd.to_datetime(df[x_col])
    
    plt.figure(figsize=(12, 6))
    sns.scatterplot(data=df, x=x_col, y=y_col, s=10, alpha=1, edgecolor=None)

    #Convert to matplotlib date numbers for regression
    date_nums = mdates.date2num(df[x_col])

    sns.regplot(
        x=date_nums,
        y=df[y_col],
        scatter=False,
        color='red',
        label='Linear Trend',
    )

    #Set x-axis to format in years instead of in date ordinal
    plt.gca().xaxis.set_major_locator(mdates.YearLocator(10))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.show()

#plot a single data
def plot_data(df, x, y, xLabel, yLabel, title):
    plt.figure(figsize=(12, 6))
    plt.plot(df[x], df[y])  
    plt.xlabel(xLabel) 
    plt.ylabel(yLabel)
    plt.title(title)
    plt.show()

#plot multiple data sets in same graph
def plot_multiple_data(df, x, y_list, labels, xLabel, yLabel, title):
    plt.figure(figsize=(20, 6))
    colors = ['blue', 'orange']
    for y, label, color in zip(y_list, labels, colors):
        plt.plot(df[x], df[y], label=label, alpha = 0.5, color=color)
    
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.title(title)
    plt.legend()
    plt.show()

#Average anomaly between two years
def avg_years_range(df, start_year, end_year):
    df_filtered = df[(df['Year'] >= start_year) & (df['Year'] <= end_year)]
    return df_filtered['Anomaly_Temp_K'].mean()


#This function will plot temperature anomalies on a map with latitudes and color them based on temperature
def plot_temp_by_Lat(lat_temp_df):
    fig = px.scatter_geo(
        lat_temp_df,
        lat='Lat',
        lon=[0]*len(lat_temp_df),
        color='Avg_Anomaly',
        size=[20000]*len(lat_temp_df),
        color_continuous_scale='RdBu_r',
        projection='natural earth',
        title='Average Ocean Temperature Anomaly by Latitude (Last 10 Years)'
    )

    # fig.update_traces(marker=dict(line=dict(width=0)))  #Remove white outline
    fig.show()