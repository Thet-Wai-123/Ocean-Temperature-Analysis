import pandas as pd

def clean_temperature(df):
    df['Date'] = pd.to_datetime(df[['Year', 'Month']].assign(DAY=1))
    df = df[(df != -999.0).all(1)]

