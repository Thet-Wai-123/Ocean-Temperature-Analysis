import pandas as pd
from HelperFunctions import *
from scipy.stats.mstats import pearsonr

def main():
    #Getting the ocean data and cleaning it.
    col_names = [
        "Year", "Month", "Anomaly_Temp_K"
    ]

    ocean_temp_df = pd.read_csv("data/Ocean/aravg.mon.ocean.90S.90N.v6.0.0.202502.asc.txt",  delimiter="\s+", header=None, names = col_names, usecols=[0, 1, 2]) 
    clean_temp(ocean_temp_df)
    add_date(ocean_temp_df)

    #Printing out the shape
    print("Ocean Temperature data shape: ")
    print(ocean_temp_df.shape)

    #Graph of global ocean temp over time, one without line of best fit and the other with. 
    plot_data(ocean_temp_df, "Date", "Anomaly_Temp_K", "Time", "Temperature Anomaly (K)", "Date vs Ocean Temperature")
    plot_data_with_bestFitLine(ocean_temp_df, "Date", "Anomaly_Temp_K", "Time", "Temperature Anomaly (K)", "Date vs Ocean Temperature")

    #Save the cleaned df back to csv
    ocean_temp_df.to_csv('outputData/cleaned_global_ocean_temp', index=False)

    #Analyze each area by splitting them into different latituides
    ocean_temp_00N_30N = pd.read_csv("data/Ocean/aravg.mon.ocean.00N.30N.v6.0.0.202502.asc.txt", delimiter="\s+", header=None, names=col_names, usecols=[0, 1, 2])
    ocean_temp_30N_60N = pd.read_csv("data/Ocean/aravg.mon.ocean.30N.60N.v6.0.0.202502.asc.txt", delimiter="\s+", header=None, names=col_names, usecols=[0, 1, 2])
    ocean_temp_60N_90N = pd.read_csv("data/Ocean/aravg.mon.ocean.60N.90N.v6.0.0.202502.asc.txt", delimiter="\s+", header=None, names=col_names, usecols=[0, 1, 2])
    ocean_temp_30S_00N = pd.read_csv("data/Ocean/aravg.mon.ocean.30S.00N.v6.0.0.202502.asc.txt", delimiter="\s+", header=None, names=col_names, usecols=[0, 1, 2])
    ocean_temp_60S_30S = pd.read_csv("data/Ocean/aravg.mon.ocean.60S.30S.v6.0.0.202502.asc.txt", delimiter="\s+", header=None, names=col_names, usecols=[0, 1, 2])
    ocean_temp_90S_60S = pd.read_csv("data/Ocean/aravg.mon.ocean.90S.60S.v6.0.0.202502.asc.txt", delimiter="\s+", header=None, names=col_names, usecols=[0, 1, 2])

    data = [
        {'Lat': 75, 'Avg_Anomaly': avg_years_range(ocean_temp_60N_90N, 2015, 2025)},
        {'Lat': 45, 'Avg_Anomaly': avg_years_range(ocean_temp_30N_60N, 2015, 2025)},
        {'Lat': 15, 'Avg_Anomaly': avg_years_range(ocean_temp_00N_30N, 2015, 2025)},
        {'Lat': -15, 'Avg_Anomaly': avg_years_range(ocean_temp_30S_00N, 2015, 2025)},
        {'Lat': -45, 'Avg_Anomaly': avg_years_range(ocean_temp_60S_30S, 2015, 2025)},
        {'Lat': -75, 'Avg_Anomaly': avg_years_range(ocean_temp_90S_60S, 2015, 2025)},
    ]

    lat_temp_df = pd.DataFrame(data)
    plot_temp_by_Lat(lat_temp_df)


    #Comparing with CO2 Emissions
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
