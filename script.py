import sys
import random
import streamlit as st
from gspread_pandas import Spread,Client
from google.oauth2 import service_account
import pandas as pd
import plotly.express as px
from dataprep.clean import clean_country
from geopy.distance import great_circle
from millify import millify

################### STREAMLIT-Config #################
# App config #
st.set_page_config(page_title="Flying Pe"
                    ,page_icon = ":airplane"
                    # ,page_icon=Image.open('')
                    ,layout="centered" 
                    )

# Hide menu & footer
hide_menu_style = """
                    <style>
                    #MainMenu {visibility: visible; }
                    footer {visibility: hidden;}
                    </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

######################################################


# Panda options #
# pd.set_option('display.max_rows', 100)
# pd.set_option('display.max_columns', None)

### Create a connection to spreadsheet ###
scope = ["https://www.googleapis.com/auth/spreadsheets"
        ,"https://spreadsheets.google.com/feeds"
        ,"https://www.googleapis.com/auth/drive"]
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scope
)
client = Client(scope=scope, creds=credentials)
spreadsheet_name = 'py_flight_data'
sheet_name = 'flightDataset'
spread = Spread(spreadsheet_name, client = client)

# Call our spreadsheet
sh = client.open(spreadsheet_name)
# worksheet_list = sh.worksheets()

### READ SPREADSHEET ###
@st.experimental_memo()
def fn_read_spreadsheet():
    worksheet = sh.worksheet(sheet_name)
    df = pd.DataFrame(worksheet.get_all_records())
    df = df[~(df['Flight Number'].isin(['#VALUE!']))] # filter out rows without data
    return df

df = fn_read_spreadsheet()

### Calculate great-circle distnace for each trip ###
df['Departing Coordinates'] = list(zip(df['Latitude'], df['Longitude']))
df['Arriving Coordinates'] = list(zip(df['Arrival Latitude'], df['Arrival Longitude']))
df['Distance travelled (km)'] = df.apply(
        lambda x: 
        great_circle(x['Departing Coordinates'], x['Arriving Coordinates']).kilometers
        , axis=1)

#######################################################


### Read in country codes + other (maybe) useful data ###

@st.experimental_memo(ttl=86400)
def fn_country_code_data():
    df_country_codes = pd.read_csv("https://datahub.io/core/country-codes/r/country-codes.csv"
                        , header=0, delimiter=',', keep_default_na=False, na_values='')
    return df_country_codes

@st.experimental_memo(ttl=86400)
def fn_continent_code_data():
    df_continent_codes = pd.read_csv("https://datahub.io/core/continent-codes/r/continent-codes.csv"
                        , header=0, delimiter=',', keep_default_na=False, na_values='')
    return df_continent_codes

df_continent_codes = fn_continent_code_data()
df_continent_codes = df_continent_codes.rename(columns = {'Code':'Continent', 'Name':'Continent Name'})


df_country_codes = fn_country_code_data()
df_country_codes = df_country_codes[
    ['official_name_en', 'ISO4217-currency_country_name', 'Capital', 'Region Name', 'Sub-region Name'
        , 'Continent', 'Languages', 'is_independent', 'Developed / Developing Countries', 'ISO3166-1-Alpha-2'
        , 'ISO3166-1-Alpha-3', 'Geoname ID']
]

### function to get official country name and alpha-3 country codes ###

df = clean_country(df, "Country", input_format="name", output_format="official", inplace=False)
df.rename(columns={'Country_clean': 'Official_Country_Name'}, inplace=True)
df = clean_country(df, "Official_Country_Name", input_format="official", output_format="alpha-3", inplace=False)
df.rename(columns={'Official_Country_Name_clean': 'alpha-3'}, inplace=True)

### merge and get Continent Names ###
df_country_codes = pd.merge(
        df_country_codes
        ,df_continent_codes
        ,how='left'
        ,on=['Continent']
)

#######################################################


### Calculate frequency of trips by various categories ###
# Times visited & Days spent

visits = df[["Country", "City", 'Official_Country_Name', 'alpha-3']] \
    .groupby(["Country", "City", 'Official_Country_Name', 'alpha-3']) \
    .size().to_frame().reset_index()
visits.rename(columns={0: 'Visits'}, inplace=True)

nights_away = df[["Country", "City", 'Official_Country_Name', 'alpha-3', "Nights away"]] \
    .groupby(["Country", "City", 'alpha-3', 'Official_Country_Name'])["Nights away"] \
    .sum().to_frame().reset_index()

distance_travelled = df[["Country", "City", 'Official_Country_Name', 'alpha-3', "Distance travelled (km)"]] \
    .groupby(["Country", "City", 'alpha-3', 'Official_Country_Name'])["Distance travelled (km)"] \
    .sum().to_frame().reset_index()

# nights_away = df[["Country", "City", 'Official_Country_Name', 'alpha-3', "Nights away"]] \
#     .groupby(["Country", "City", 'alpha-3', 'Official_Country_Name']) \
#     .sum().reset_index()

# nights_away = nights_away['Nights away'].sum()

# print(visits.sample(5))
# print(nights_away)
# print(nights_away.sample(5))

## join on to these dataframes, the alpha 2 country code and the continent code #
# Merge vists and nights_away
df_geo = pd.merge(
    visits,
    nights_away,
    how="inner",
    on=['Country', 'City', 'Official_Country_Name', 'alpha-3'],
    sort=True,
    suffixes=("_x", "_y"),
    copy=True,
    indicator=False,
    validate=None,
)
# Merge distance travelled
df_geo = pd.merge(
    df_geo,
    distance_travelled,
    how="inner",
    on=['Country', 'City', 'Official_Country_Name', 'alpha-3'],
    sort=True,
    suffixes=("_x", "_y"),
    copy=True,
    indicator=False,
    validate=None,
)
# merge country codes onto df + additional metadata
df_geo = pd.merge(
    df_geo,
    df_country_codes[
        ['Continent', 'Continent Name', 'Capital', 'Region Name', 'Sub-region Name', 'ISO3166-1-Alpha-2', 'ISO3166-1-Alpha-3']],
    how='left',
    left_on='alpha-3',
    right_on='ISO3166-1-Alpha-3',
    sort=True,
    copy=True
).sort_values(by=['Nights away']) # sorting values so that it shows up in the legend of the chart in correct order

# Metric from df_geo
max_nights_away = df_geo['Nights away'].max()


### Create plotly diagram ###
def fn_create_scratch_map(scope='world', projection = "natural earth"):
    st.write()

    fig = px.choropleth(df_geo, locations="alpha-3"
                        
                        # ,color_continuous_scale=px.colors.sequential.Plasma
                        # ,color_continuous_scale=px.colors.sequential.swatches_continuous()
                        , color_continuous_scale="Viridis"
                        # ,color_discrete_sequence = px.colors.cyclical.swatches
                        , range_color=(0,max_nights_away)
                        ,hover_name = 'Country'
                        ,hover_data = ['Capital', 'Sub-region Name', 'Visits', 'Nights away']
                        ,color="Nights away"
                        ,labels={'alpha-3':'Country Code'}
                        ,basemap_visible = True
                        # ,fitbounds="locations"
                        # ,title=scope
                        ,projection=projection
                        )

    # Reference: https://plotly.com/python/map-configuration/   - changing the look and feel of the map
    # fig.update_geos(projection_type="orthographic")
    fig.update_geos(scope=scope # "africa" | "asia" | "europe" | "north america" | "south america" | "usa" | "world" )
                    , showframe=True
                    , framecolor=random.choice(['wheat', 'snow', 'powderblue','midnightblue'])
                    # , bgcolor="#0E1117"
                    , bgcolor='rgba(0,0,0,0)'
                    , resolution=110
                    , showcountries=True
                    , countrycolor="grey"
                    # , showsubunits=True
                    # , subunitcolor="green"
                    # , showcoastlines=True, coastlinecolor="light grey"
                    # , showland=True, landcolor="LightGreen"
                    # , showocean=True, oceancolor="LightBlue"
                    # , showlakes=True, lakecolor="white"
                    # , showrivers=True, rivercolor="Blue"
                    )
    fig.update_layout(height=450
                     ,margin={"r": 0, "t": 0, "l": 0, "b": 0}
                     
                     )
    fig.update_layout(legend=dict(
                                    orientation="h",
                                    yanchor="bottom",
                                    y=-0.1,
                                    xanchor="center",
                                    x=0.5
                            ))
    fig.update_layout(transition={
                'duration': 200,
                'easing': 'circle-in'
        })

    return fig


################### STREAMLIT - Page #################################

st.title('Flying Pe')
st.markdown("***")

# Columns
col_flights, col_distance, col_countries, col_cities, col_nights_away = st.columns(5, gap='small')
# Radio button - select continent
radio_continent = st.radio(" "
                            ,('🌎', 'Africa', 'Asia', 'Europe', 'North America', 'South America', 'Oceania')
                            ,index=0
                            ,key='radio_continent'
                            ,horizontal=True)

st.markdown('***')

# Metrics Calculations
# All places/regions/countries/continents etc.
cnt_flights = len(df)
sum_distance_travelled = df['Distance travelled (km)'].sum()
cnt_countries = df['Country'].nunique()
cnt_cities = df['City'].nunique()
sum_nights_away = df['Nights away'].sum()
# Metrics based on continets
cnt_flights_filtered = df_geo[df_geo['Continent Name']==radio_continent]['Visits'].sum()
sum_distance_travelled_filtered = df_geo[df_geo['Continent Name']==radio_continent]['Distance travelled (km)'].sum()
cnt_countries_filtered = df_geo[df_geo['Continent Name']==radio_continent]['Country'].nunique()
cnt_cities_filtered = df_geo[df_geo['Continent Name']==radio_continent]['City'].nunique()
sum_nights_away_filtered = df_geo[df_geo['Continent Name']==radio_continent]['Nights away'].sum()

# Metrics
with col_flights:
    st.metric('Flights'
        , cnt_flights if radio_continent=='🌎' else cnt_flights_filtered
        , delta=cnt_flights)
with col_distance:
    st.metric('Distance (km)'
        , millify(sum_distance_travelled, precision=2) if radio_continent=='🌎' else millify(sum_distance_travelled_filtered, precision=2)
        , delta=millify(sum_distance_travelled, precision=2))
with col_countries:
    st.metric('Countries Visited'
        , cnt_countries if radio_continent=='🌎' else cnt_countries_filtered
        , delta=cnt_countries)
with col_cities:
    st.metric('Cities Visited'
        , cnt_cities if radio_continent=='🌎' else cnt_cities_filtered
        , delta=cnt_cities)
with col_nights_away:
    st.metric('Nights Away'
        , sum_nights_away if radio_continent=='🌎' else sum_nights_away_filtered
        , delta=sum_nights_away)

# Scratch Map
with st.spinner('Loading...'):
    if radio_continent == '🌎':
            st.plotly_chart(fn_create_scratch_map(scope='world', projection='orthographic'), use_container_width=True)
    elif radio_continent == 'Africa':
            st.plotly_chart(fn_create_scratch_map(scope='africa'), use_container_width=True)
    elif radio_continent == 'Asia':
            st.plotly_chart(fn_create_scratch_map(scope='asia'), use_container_width=True)
    elif radio_continent == 'Europe':
            st.plotly_chart(fn_create_scratch_map(scope='europe'), use_container_width=True)
    elif radio_continent == 'North America':
            st.plotly_chart(fn_create_scratch_map(scope='north america'), use_container_width=True)                
    elif radio_continent == 'South America':
            st.plotly_chart(fn_create_scratch_map(scope='south america'), use_container_width=True)
    elif radio_continent == 'Oceania':
            # st.plotly_chart(fn_create_scratch_map(scope='oceania'), use_container_width=True)
            st.error('There is no map info in plotly choropleth... Sorry.... but nothing I can do for now.')
    else: st.write()

# Dataframe
# st.dataframe(df)
with st.expander('Click to see data... (for debugging)'):
    st.dataframe(df)
    st.dataframe(df_geo)
# st.dataframe(df_country_codes)
# st.dataframe(fn_country_code_data())

# print(df.head())