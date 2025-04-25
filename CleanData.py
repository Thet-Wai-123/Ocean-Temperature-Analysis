import numpy as np
import pandas as pd
from scipy import stats

#remove outliers and all that has -999 as value
def clean_temp(df):
    df = df[(df != -999.0).all(1)]
    df = df[np.abs(stats.zscore(df['Anomaly_Temp_K'])) < 2]

def add_date(df):
    df['Date'] = pd.to_datetime(df[['Year', 'Month']].assign(DAY=1))
