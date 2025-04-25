from matplotlib import pyplot as plt
import pandas as pd
from CleanData import clean_temp, add_date
from PlotData import *
from scipy.stats.mstats import pearsonr

def main():
    """ Main program """
    
    col_names = [
        "Year", "Month", "Anomaly_Temp_K"
    ]

    ocean_temp_df = pd.read_csv("data/Ocean/aravg.mon.ocean.90S.90N.v6.0.0.202502.asc.txt",  delimiter="\s+", header=None, names = col_names, usecols=[0, 1, 2]) 
    clean_temp(ocean_temp_df)
    add_date(ocean_temp_df)
    print("Ocean Temperature data shape: ")
    print(ocean_temp_df.shape)
    #Same shape, meaning there is no outliers nor NaN values. Additionally cleaning added a new column combing Year and Month called "Date"

    # CO2 Emissions Comparison
    plot_data(ocean_temp_df, "Date", "Anomaly_Temp_K", "Time", "Temperature Anomaly (K)", "Date vs Ocean Temperature")

    co2_emissions_df = pd.read_csv("data/Emissions/cumulative-co-emissions.csv")
    plot_data(co2_emissions_df, "Year", "Cumulative CO₂ emissions", "Time", "Cumulative CO₂ emissions" , "Year vs Cumulative CO₂ emissions")

    df_merged = pd.merge(ocean_temp_df, co2_emissions_df, on='Year', how='inner') 
    correlation, pValue = pearsonr(df_merged['Cumulative CO₂ emissions'], df_merged['Anomaly_Temp_K'])
    print("Correlation between CO₂ emissions and Ocean Temp:")
    print(correlation)
    print("p-value:")
    print(pValue)



    #Land Temperature Comparison
    land_temp_df = pd.read_csv("data/Land/aravg.mon.land.90S.90N.v6.0.0.202502.asc.txt", delimiter="\s+", header=None, names = col_names, usecols=[0, 1, 2])
    clean_temp(land_temp_df)
    add_date(land_temp_df)
    print("Land Temperature data shape: ")
    print(land_temp_df.shape)

    correlation, pValue = pearsonr(ocean_temp_df['Anomaly_Temp_K'], land_temp_df['Anomaly_Temp_K'])
    print("Correlation and pValue between ocean and land temp:")
    print(correlation)
    print("p-value:")
    print(pValue)

    #plotting ocean and land together
    ocean_temp_df['yearlyAverage'] = ocean_temp_df.groupby('Year')['Anomaly_Temp_K'].transform('mean')
    land_temp_df['yearlyAverage'] = land_temp_df.groupby('Year')['Anomaly_Temp_K'].transform('mean')

    df_merged = ocean_temp_df.merge(land_temp_df, on='Year', suffixes=('_ocean', '_land'))
    df_merged = df_merged.drop_duplicates(subset="Year")

    print(df_merged.columns)
    print(df_merged.shape)

    plot_multiple_data(
        df_merged,
        x='Year',
        y_list=['yearlyAverage_ocean', 'yearlyAverage_land'],
        labels=['Ocean Temp', 'Land Temp'],
        xLabel='Date',
        yLabel='Temperature Anamoly',
        title='Time vs Ocean and Land Temp Anamolies'
    )

    return 0

if __name__ == "__main__":
    main()
