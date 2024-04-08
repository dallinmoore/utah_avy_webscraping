import pandas as pd

df_avys = pd.read_csv("UT-Avalanches.csv")
df_danger = pd.read_csv("avy-danger/avalanche-forecast-rose.csv")
df_avys.drop(["Accident and Rescue Summary","Terrain Summary","Weather Conditions and History","Comments 1","Comments 2","Comments 3","Comments 4"], axis='columns')
replace_dict = {"Salt lake":"Salt Lake","Abajo":"Abajos"}
df_danger['Forecast Area'] = df_danger['Forecast Area'].replace(replace_dict)
replace_dict = {"SE Idaho":"Logan"}
df_avys['Region'] = df_avys['Region'].replace(replace_dict)
df_avys.drop(df_avys[df_avys['Region'].isin(['Southwest', 'State-wide'])].index, inplace=True)
# Removing commas and apostrophes
df_avys['Elevation'] = df_avys['Elevation'].str.replace(",", "").str.replace("'", "")
# Converting to numeric, coercing errors to NaN
df_avys['Elevation'] = pd.to_numeric(df_avys['Elevation'], errors='coerce')
# Converting NaNs to 0, if you want
df_avys['Elevation'].fillna(0, inplace=True)
# Converting to integers
df_avys['Elevation'] = df_avys['Elevation'].astype(int)

avy_levels = {"Salt Lake":[8000,9500],
              "Logan":[7000,8500],
              "Uintas":[10000,11000], # treeline
              "Provo":[8000,9500],
              "Skyline":[8000,9500],
              "Ogden":[7000,8500],
              "Moab":[10000,11000], # treeline
              "Abajos":[10000,11000]} # treeline

def match_danger(day, region, aspect, elevation):
    # find the region and grab the correct list for elevations
    # find which elevation matches by seeing if it is greater than the first or both elements of the list
    # save the avalanche danger as the aspect+'lower/middle/upper' for the day and region
    # if there isn't one matching, find the most recent day
    # save other avalanche danger rating (max danger for each aspect and elevation)
    
    # specific forecast, aspect max forecast, total max forecast
    # forecast = []
    # needs to make sure that the day and region has a forecast (will fail if region is nan)
    days_forecast = df_danger[(df_danger['Date Issued'] == day) & (df_danger['Forecast Area'] == region)]

    # if there is not a forecast, then there will be forecast for the avalanche
    if days_forecast.empty:
        return None
    
    if isinstance(aspect, str):
        if elevation == 0: # if there is no elevation data
            forecast = days_forecast[[aspect+'-lower',aspect+'-middle',aspect+'-upper']].max()
        elif elevation < avy_levels[region][0]:              # lower level
            forecast = days_forecast[aspect+'-lower']
        elif elevation > avy_levels[region][1]:              # upper level
            forecast = days_forecast[aspect+'-upper']
        else:                                                # middle level
            forecast = days_forecast[aspect+'-middle']
    else:
        if elevation == 0: # if there is no elevation data
            forecast = days_forecast.drop(columns=['Date Issued','Forecast Area','Link']).max()
        elif elevation < avy_levels[region][0]:              # lower level
            forecast = days_forecast[['North-lower','Northeast-lower','East-lower','Southeast-lower','South-lower','Southwest-lower','West-lower','Northwest-lower']].max()
        elif elevation > avy_levels[region][1]:              # upper level
            forecast = days_forecast[['North-upper','Northeast-upper','East-upper','Southeast-upper','South-upper','Southwest-upper','West-upper','Northwest-upper']].max()
        else:                                                # middle level
            forecast = days_forecast[['North-middle','Northeast-middle','East-middle','Southeast-middle','South-middle','Southwest-middle','West-middle','Northwest-middle']].max()
    
    return forecast.values[0]

# match_danger('2/19/2024','Uintas','Southeast',9800)
danger_levels = []
for index, row in df_avys.iterrows():
    # print(row)
    danger_level = match_danger(row['Date'], row['Region'], row['Aspect'], row['Elevation'])
    danger_levels.append(danger_level)
df_avys['Danger Level'] = danger_levels

df_avys.to_csv("UT-avalanches-full-dataset.csv",index=False)
