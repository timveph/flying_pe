from geopy.distance import great_circle
from scripts.fn_read_spreadsheet import fn_read_spreadsheet
import streamlit as st
import pandas as pd
from dataprep.clean import clean_country


def fn_data_attributes():
    df=fn_read_spreadsheet()
    ### Calculate great-circle distance for each trip ###
    df['Departing Coordinates'] = list(zip(df['Latitude'], df['Longitude']))
    df['Arriving Coordinates'] = list(zip(df['Arrival Latitude'], df['Arrival Longitude']))
    df['Distance travelled (km)'] = df.apply(
            lambda x: 
            great_circle(x['Departing Coordinates'], x['Arriving Coordinates']).kilometers
            , axis=1)
            
    ### Calculate time for each trip ###
    df['Time Spent Travelling (s)'] = (df['Destination End Time'] - df['Destination Start Time']).dt.total_seconds()

    ### function to get official country name and alpha-3 country codes ###
    df = clean_country(df, "Country", input_format="name", output_format="official", inplace=False)
    df.rename(columns={'Country_clean': 'Official_Country_Name'}, inplace=True)
    df = clean_country(df, "Official_Country_Name", input_format="official", output_format="alpha-3", inplace=False)
    df.rename(columns={'Official_Country_Name_clean': 'alpha-3'}, inplace=True)

    return df

### Read in country codes ###
@st.experimental_memo(ttl=86400)
def fn_country_code_data():
    df_country_codes = pd.read_csv("https://datahub.io/core/country-codes/r/country-codes.csv"
                        , header=0, delimiter=',', keep_default_na=False, na_values='')
    df_country_codes = df_country_codes[
        ['official_name_en', 'ISO4217-currency_country_name', 'Capital', 'Region Name', 'Sub-region Name'
        , 'Continent', 'Languages', 'is_independent', 'Developed / Developing Countries', 'ISO3166-1-Alpha-2'
        , 'ISO3166-1-Alpha-3', 'Geoname ID']
]
    return df_country_codes

### Read in continent codes ###
@st.experimental_memo(ttl=86400)
def fn_continent_code_data():
    df_continent_codes = pd.read_csv("https://datahub.io/core/continent-codes/r/continent-codes.csv"
                        , header=0, delimiter=',', keep_default_na=False, na_values='')
    df_continent_codes = df_continent_codes.rename(columns = {'Code':'Continent', 'Name':'Continent Name'})
    return df_continent_codes


#######################################################