import numpy as np
import pandas as pd
from scipy import stats

def clean_temp(df):
    df['Date'] = pd.to_datetime(df[['Year', 'Month']].assign(DAY=1))
    df = df[(df != -999.0).all(1)]
    
    df = df[np.abs(stats.zscore(df['Anomaly_Temp_K'])) < 3]

