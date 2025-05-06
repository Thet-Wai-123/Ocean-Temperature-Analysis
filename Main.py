import pandas as pd
from HelperFunctions import *
from scipy.stats.mstats import pearsonr

def main():
    #Getting the ocean data and cleaning it.
    col_names = [
        "Year", "Month", "Anomaly_Temp_K"
    ]

    #Ocean Temperature
    ocean_temp_df = pd.read_csv("data/Ocean/aravg.mon.ocean.90S.90N.v6.0.0.202502.asc.txt",  delimiter="\s+", header=None, names = col_names, usecols=[0, 1, 2]) 
    clean_temp(ocean_temp_df)
    add_date(ocean_temp_df)
    plot_data(ocean_temp_df, "Date", "Anomaly_Temp_K", "Time", "Temperature Anomaly (K)", "Date vs Ocean Temperature")

    #Land Temperature
    land_temp_df = pd.read_csv("data/Land/aravg.mon.land.90S.90N.v6.0.0.202502.asc.txt", delimiter="\s+", header=None, names = col_names, usecols=[0, 1, 2])
    clean_temp(land_temp_df)
    add_date(land_temp_df)
    plot_data(ocean_temp_df, "Date", "Anomaly_Temp_K", "Time", "Temperature Anomaly (K)", "Date vs Land Temperature")

    #Pearson test between ocean and land
    correlation, pValue = pearsonr(land_temp_df['Anomaly_Temp_K'], ocean_temp_df['Anomaly_Temp_K'])
    print("Correlation and pValue between ocean and land temp:")
    print(correlation)
    print("p-value:")
    print(pValue)

    #Land_Ocean Temperature
    land_ocean_temp_df = pd.read_csv("data/Land_Ocean/aravg.mon.land_ocean.90S.90N.v6.0.0.202502.asc.txt", delimiter="\s+", header=None, names = col_names, usecols=[0, 1, 2])
    clean_temp(land_ocean_temp_df)
    add_date(land_ocean_temp_df)
    plot_data(land_ocean_temp_df, "Date", "Anomaly_Temp_K", "Time", "Temperature Anomaly (K)", "Date vs Land_Ocean Temperature")

    #Pearson test between ocean and land_ocean
    correlation, pValue = pearsonr(land_ocean_temp_df['Anomaly_Temp_K'], ocean_temp_df['Anomaly_Temp_K'])
    print("Correlation and pValue between ocean and ocean_land temp:")
    print(correlation)
    print("p-value:")
    print(pValue)


    #plotting ocean, land and land_ocean together over time
    ocean_temp_df['yearlyAverage'] = ocean_temp_df.groupby('Year')['Anomaly_Temp_K'].transform('mean')
    land_temp_df['yearlyAverage'] = land_temp_df.groupby('Year')['Anomaly_Temp_K'].transform('mean')
    land_ocean_temp_df['yearlyAverage'] = land_ocean_temp_df.groupby('Year')['Anomaly_Temp_K'].transform('mean')
    land_ocean_temp_df = land_ocean_temp_df.rename(columns={'yearlyAverage': 'yearlyAverage_land_ocean'})

    df_merged = ocean_temp_df.merge(land_temp_df, on='Year', suffixes=('_ocean', '_land'))
    df_merged = df_merged.drop_duplicates(subset="Year")
    df_merged = df_merged.merge(land_ocean_temp_df, on='Year', suffixes=('', "_land_ocean"))
    df_merged = df_merged.drop_duplicates(subset="Year")

    plot_multiple_data(
        df_merged,
        x='Year',
        y_list=['yearlyAverage_ocean', 'yearlyAverage_land', 'yearlyAverage_land_ocean'],
        labels=['Ocean Temp', 'Land Temp', 'Land_Ocean Temp'],
        xLabel='Date',
        yLabel='Temperature Anomaly',
        title='Time vs Ocean, Land_Ocean and Land Temperature Anomalies'
    )

    #Comparing with CO2 Emissions
    co2_emissions_df = pd.read_csv("data/Emissions/cumulative-co-emissions.csv")
    plot_data(co2_emissions_df, "Year", "Cumulative CO₂ emissions", "Time", "Cumulative CO₂ emissions" , "Year vs Cumulative CO₂ emissions")

    df_merged = pd.merge(ocean_temp_df, co2_emissions_df, on='Year', how='inner') 
    correlation, pValue = pearsonr(df_merged['Cumulative CO₂ emissions'], df_merged['Anomaly_Temp_K'])
    print("Correlation between CO₂ emissions and Ocean Temp:")
    print(correlation)
    print("p-value:")
    print(pValue)



    #Plotting the rest of the data, categorized by latitude

    #Ocean Temperature Data
    ocean_temp_00N_30N = pd.read_csv("data/Ocean/aravg.mon.ocean.00N.30N.v6.0.0.202502.asc.txt", delimiter="\s+", header=None, names=col_names, usecols=[0, 1, 2])
    ocean_temp_30N_60N = pd.read_csv("data/Ocean/aravg.mon.ocean.30N.60N.v6.0.0.202502.asc.txt", delimiter="\s+", header=None, names=col_names, usecols=[0, 1, 2])
    ocean_temp_60N_90N = pd.read_csv("data/Ocean/aravg.mon.ocean.60N.90N.v6.0.0.202502.asc.txt", delimiter="\s+", header=None, names=col_names, usecols=[0, 1, 2])
    ocean_temp_30S_00N = pd.read_csv("data/Ocean/aravg.mon.ocean.30S.00N.v6.0.0.202502.asc.txt", delimiter="\s+", header=None, names=col_names, usecols=[0, 1, 2])
    ocean_temp_60S_30S = pd.read_csv("data/Ocean/aravg.mon.ocean.60S.30S.v6.0.0.202502.asc.txt", delimiter="\s+", header=None, names=col_names, usecols=[0, 1, 2])
    ocean_temp_90S_60S = pd.read_csv("data/Ocean/aravg.mon.ocean.90S.60S.v6.0.0.202502.asc.txt", delimiter="\s+", header=None, names=col_names, usecols=[0, 1, 2])

    # Load Land Temperature Data
    land_temp_00N_30N = pd.read_csv("data/Land/aravg.mon.land.00N.30N.v6.0.0.202502.asc.txt", delimiter="\s+", header=None, names=col_names, usecols=[0, 1, 2])
    land_temp_30N_60N = pd.read_csv("data/Land/aravg.mon.land.30N.60N.v6.0.0.202502.asc.txt", delimiter="\s+", header=None, names=col_names, usecols=[0, 1, 2])
    land_temp_60N_90N = pd.read_csv("data/Land/aravg.mon.land.60N.90N.v6.0.0.202502.asc.txt", delimiter="\s+", header=None, names=col_names, usecols=[0, 1, 2])
    land_temp_30S_00N = pd.read_csv("data/Land/aravg.mon.land.30S.00N.v6.0.0.202502.asc.txt", delimiter="\s+", header=None, names=col_names, usecols=[0, 1, 2])
    land_temp_60S_30S = pd.read_csv("data/Land/aravg.mon.land.60S.30S.v6.0.0.202502.asc.txt", delimiter="\s+", header=None, names=col_names, usecols=[0, 1, 2])
    land_temp_90S_60S = pd.read_csv("data/Land/aravg.mon.land.90S.60S.v6.0.0.202502.asc.txt", delimiter="\s+", header=None, names=col_names, usecols=[0, 1, 2])

    # Load Land_Ocean Temperature Data
    land_ocean_temp_00N_30N = pd.read_csv("data/Land_Ocean/aravg.mon.land_ocean.00N.30N.v6.0.0.202502.asc.txt", delimiter="\s+", header=None, names=col_names, usecols=[0, 1, 2])
    land_ocean_temp_30N_60N = pd.read_csv("data/Land_Ocean/aravg.mon.land_ocean.30N.60N.v6.0.0.202502.asc.txt", delimiter="\s+", header=None, names=col_names, usecols=[0, 1, 2])
    land_ocean_temp_60N_90N = pd.read_csv("data/Land_Ocean/aravg.mon.land_ocean.60N.90N.v6.0.0.202502.asc.txt", delimiter="\s+", header=None, names=col_names, usecols=[0, 1, 2])
    land_ocean_temp_30S_00N = pd.read_csv("data/Land_Ocean/aravg.mon.land_ocean.30S.00N.v6.0.0.202502.asc.txt", delimiter="\s+", header=None, names=col_names, usecols=[0, 1, 2])
    land_ocean_temp_60S_30S = pd.read_csv("data/Land_Ocean/aravg.mon.land_ocean.60S.30S.v6.0.0.202502.asc.txt", delimiter="\s+", header=None, names=col_names, usecols=[0, 1, 2])
    land_ocean_temp_90S_60S = pd.read_csv("data/Land_Ocean/aravg.mon.land_ocean.90S.60S.v6.0.0.202502.asc.txt", delimiter="\s+", header=None, names=col_names, usecols=[0, 1, 2])

    # Bargraphs for Ocean, Land, and Land_Ocean
    data = [
        {'Latitude Band': '60N-90N', 'Ocean_Anomaly': avg_temp_anomaly_difference_in_2_decades(ocean_temp_60N_90N, 1850, 2025),
        'Land_Anomaly': avg_temp_anomaly_difference_in_2_decades(land_temp_60N_90N, 1850, 2025),
        'Land_Ocean_Anomaly': avg_temp_anomaly_difference_in_2_decades(land_ocean_temp_60N_90N, 1850, 2025)},
        {'Latitude Band': '30N-60N', 'Ocean_Anomaly': avg_temp_anomaly_difference_in_2_decades(ocean_temp_30N_60N, 1850, 2025),
        'Land_Anomaly': avg_temp_anomaly_difference_in_2_decades(land_temp_30N_60N, 1850, 2025),
        'Land_Ocean_Anomaly': avg_temp_anomaly_difference_in_2_decades(land_ocean_temp_30N_60N, 1850, 2025)},
        {'Latitude Band': '00N-30N', 'Ocean_Anomaly': avg_temp_anomaly_difference_in_2_decades(ocean_temp_00N_30N, 1850, 2025),
        'Land_Anomaly': avg_temp_anomaly_difference_in_2_decades(land_temp_00N_30N, 1850, 2025),
        'Land_Ocean_Anomaly': avg_temp_anomaly_difference_in_2_decades(land_ocean_temp_00N_30N, 1850, 2025)},
        {'Latitude Band': '30S-00N', 'Ocean_Anomaly': avg_temp_anomaly_difference_in_2_decades(ocean_temp_30S_00N, 1850, 2025),
        'Land_Anomaly': avg_temp_anomaly_difference_in_2_decades(land_temp_30S_00N, 1850, 2025),
        'Land_Ocean_Anomaly': avg_temp_anomaly_difference_in_2_decades(land_ocean_temp_30S_00N, 1850, 2025)},
        {'Latitude Band': '60S-30S', 'Ocean_Anomaly': avg_temp_anomaly_difference_in_2_decades(ocean_temp_60S_30S, 1850, 2025),
        'Land_Anomaly': avg_temp_anomaly_difference_in_2_decades(land_temp_60S_30S, 1850, 2025),
        'Land_Ocean_Anomaly': avg_temp_anomaly_difference_in_2_decades(land_ocean_temp_60S_30S, 1850, 2025)},
        {'Latitude Band': '90S-60S', 'Ocean_Anomaly': avg_temp_anomaly_difference_in_2_decades(ocean_temp_90S_60S, 1850, 2025),
        'Land_Anomaly': avg_temp_anomaly_difference_in_2_decades(land_temp_90S_60S, 1850, 2025),
        'Land_Ocean_Anomaly': avg_temp_anomaly_difference_in_2_decades(land_ocean_temp_90S_60S, 1850, 2025)}
    ]
    lat_temp_df = pd.DataFrame(data)

    plot_temp_by_Lat_in_barChart(lat_temp_df, "Average Temperature Anomaly Difference by Location in Last Decade from 1850")


    
    #One extra bar graph for global
    data = [
        {'Latitude Band': '90S-90N', 'Ocean_Anomaly': avg_temp_anomaly_difference_in_2_decades(ocean_temp_df, 1850, 2025),
        'Land_Anomaly': avg_temp_anomaly_difference_in_2_decades(land_temp_df, 1850, 2025),
        'Land_Ocean_Anomaly': avg_temp_anomaly_difference_in_2_decades(land_ocean_temp_df, 1850, 2025)}]
    global_lat_temp_df = pd.DataFrame(data)
    plot_temp_by_Lat_in_barChart(global_lat_temp_df, "Average Temperature Anomaly Difference Gloobally in Last Decade from 1850")



    #Interpolation
    formula = plot_data_with_bestFitLine(ocean_temp_df, "Date", "Anomaly_Temp_K", "Time", "Temperature Anomaly (K)", "Date vs Ocean Temperature")
    print("Formula: ", formula)


if __name__ == "__main__":
    main()
