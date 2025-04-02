import pandas as pd

col_names = [
    "Year", "Month", "Anomaly_Temp_K", "Total_Error_Var_K2", "High_Freq_Error_Var_K2", "Low_Freq_Error_Var_K2", "Bias_Error_Var_K2", "Diagnostic_Var_1", "Diagnostic_Var_2", "Diagnostic_Var_3"
]

df = pd.read_csv("data/aravg.mon.ocean.00N.30N.v6.0.0.202502.asc.txt",  delimiter="\s+", header=None, names = col_names)  
df_cleaned = df[(df != -999.0).all(1)]

print(df.head())
print(df.shape)
print(df.describe())

print("After cleaning")
print(df_cleaned.shape)
