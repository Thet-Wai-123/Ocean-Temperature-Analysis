from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
import seaborn as sns
import matplotlib.dates as mdates


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

    #Curve Line
    z = np.polyfit(date_nums, df[y_col], deg=2)
    p = np.poly1d(z)
    plt.plot(df[x_col], p(date_nums), color='red', label='Quadratic Best Fit')

    #Set x-axis to format in years instead of in date ordinal
    plt.gca().xaxis.set_major_locator(mdates.YearLocator(10))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.show()

    return z

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
    colors = ['blue', 'orange', 'red']
    for y, label, color in zip(y_list, labels, colors):
        plt.plot(df[x], df[y], label=label, alpha = 0.5, color=color)
    
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.title(title)
    plt.legend()
    plt.show()

#Average anomaly between two decades
def avg_temp_anomaly_difference_in_2_decades(df, start_year, end_year):
    first_decade = df[(df['Year'] >= start_year) & (df['Year'] < start_year + 10)]
    last_decade = df[(df['Year'] > end_year - 10) & (df['Year'] <= end_year)]
    
    first_mean = first_decade['Anomaly_Temp_K'].mean()
    last_mean = last_decade['Anomaly_Temp_K'].mean()
    
    return last_mean - first_mean


def plot_temp_by_Lat_in_barChart(lat_temp_df, title):
    # Plotting the bar chart
    bar_width = 0.25  # Bar width for each dataset
    index = range(len(lat_temp_df))
    
    # Plotting each dataset side by side
    plt.figure(figsize=(12, 6))
    plt.bar(index, lat_temp_df['Ocean_Anomaly'], bar_width, label='Ocean', color='skyblue')
    plt.bar([i + bar_width for i in index], lat_temp_df['Land_Anomaly'], bar_width, label='Land', color='orange')
    plt.bar([i + 2*bar_width for i in index], lat_temp_df['Land_Ocean_Anomaly'], bar_width, label='Land_Ocean', color='green')

    # Adding titles and labels
    plt.title(title)
    plt.xlabel('Latitude Band')
    plt.ylabel('Temperature_Anomaly_Difference')
    plt.xticks([i + bar_width for i in index], lat_temp_df['Latitude Band'], rotation=45)
    
    # Adding the legend
    plt.legend()

    # Display the plot
    plt.tight_layout()
    plt.show()
    