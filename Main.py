import pandas as pd
from CleanData import clean_temp
from PlotData import plot_data
from scipy.stats.mstats import pearsonr

def main():
    """ Main program """
    
    col_names = [
        "Year", "Month", "Anomaly_Temp_K"
    ]

    ocean_temp_df = pd.read_csv("data/Ocean/aravg.mon.ocean.90S.90N.v6.0.0.202502.asc.txt",  delimiter="\s+", header=None, names = col_names, usecols=[0, 1, 2]) 
    print(ocean_temp_df.shape)

    clean_temp(ocean_temp_df)
    print(ocean_temp_df.shape)
    #Same shape, meaning there is no outliers nor NaN values. Additionally cleaning added a new column combing Year and Month called "Date"

    
    plot_data(ocean_temp_df, "Date", "Anomaly_Temp_K", "Date", "Temperature Anomaly (K)", "Date vs Ocean Temperature")

    co2_emissions_df = pd.read_csv("data/Emissions/cumulative-co-emissions.csv")
    plot_data(co2_emissions_df, "Year", "Cumulative CO₂ emissions", "test", "test" , "test")


    df_merged = pd.merge(ocean_temp_df, co2_emissions_df, on='Year', how='inner') 
    correlation, pValue = pearsonr(df_merged['Year'], df_merged['Anomaly_Temp_K'])
    print(correlation)
    print(pValue)
    return 0

if __name__ == "__main__":
    main()
