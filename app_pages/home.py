import streamlit as st
import pandas as pd
import plotly.express as px
from millify import millify
from scripts.fn_create_maps import fn_create_scratch_map
import scripts.fn_data_prep as data_prep
import datetime


def app():
    # Global Variables
    datetime_now = datetime.datetime.now()
    datetime_in_utc = datetime.datetime.utcnow()
    date_format_in_spreadsheet = "%d/%m/%Y %H:%M:%S"

    # Panda options #
    # pd.set_option('display.max_rows', 100)
    # pd.set_option('display.max_columns', None)

    #################### Data Prep #########################
    ### Add data attributes ###
    df = data_prep.fn_data_attributes()
    ### Read in country codes ###
    df_country_codes = data_prep.fn_country_code_data()
    ### Read in continent codes ###
    df_continent_codes = data_prep.fn_continent_code_data()
    ### merge and get Continent Names ###
    df_country_codes = pd.merge(
            df_country_codes
            ,df_continent_codes
            ,how='left'
            ,on=['Continent']
            )

    #######################################################

    ################### Slices of data ####################
    # Do I need to convert the time from the df into utc? - probably
    df_past_flights = df[(df['Destination End Time'] < datetime_in_utc)]
    df_todays_flights = df[(df['Event Start Date'] == datetime_in_utc.date()) 
                            | (df['Event End Date'] == datetime_in_utc.date())
                            ] # could be more than 1
    df_future_flights = df[(df['Destination Start Time'] > datetime_in_utc)]
    #######################################################


    ### Calculate frequency of trips by various categories ###
    # Times visited & Days spent

    visits = df_past_flights[["Country", "City", 'Official_Country_Name', 'alpha-3']] \
        .groupby(["Country", "City", 'Official_Country_Name', 'alpha-3']) \
        .size().to_frame().reset_index()
    visits.rename(columns={0: 'Visits'}, inplace=True)

    nights_away = df_past_flights[["Country", "City", 'Official_Country_Name', 'alpha-3', "Nights away"]] \
        .groupby(["Country", "City", 'alpha-3', 'Official_Country_Name'])["Nights away"] \
        .sum().to_frame().reset_index()

    distance_travelled = df_past_flights[["Country", "City", 'Official_Country_Name', 'alpha-3', "Distance travelled (km)"]] \
        .groupby(["Country", "City", 'alpha-3', 'Official_Country_Name'])["Distance travelled (km)"] \
        .sum().to_frame().reset_index()

    seconds_spent_travelling = df_past_flights[["Country", "City", 'Official_Country_Name', 'alpha-3', "Time Spent Travelling (s)"]] \
        .groupby(["Country", "City", 'alpha-3', 'Official_Country_Name'])["Time Spent Travelling (s)"] \
        .sum().to_frame().reset_index()

    #######################################################

    ## join on to these dataframes, the alpha 2 country code and the continent code #
    # Merge vists and nights_away
    def fn_merge_data(left_tbl, right_tbl, merge_how, merge_on=None):
        df_merged = pd.merge(
                left_tbl,
                right_tbl,
                how=merge_how,
                on=merge_on,
                sort=True,
                suffixes=("_x", "_y"),
                copy=True,
                indicator=False,
                validate=None,
        )
        return df_merged

    merge_columns = ['Country', 'City', 'Official_Country_Name', 'alpha-3']

    # Merge nights away and visits
    df_geo = fn_merge_data(visits, nights_away, "inner", merge_columns)
    # Merge distance travelled
    df_geo = fn_merge_data(df_geo, distance_travelled, "inner", merge_columns)
    # Merge time spent travelled
    df_geo = fn_merge_data(df_geo, seconds_spent_travelling, "inner", merge_columns)

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
    # max_nights_away = df_geo['Nights away'].max()


    ################# Population - Metrics Calculations ##################
    # All places/regions/countries/continents etc.
    cnt_flights = len(df_past_flights)
    sum_distance_travelled = df_past_flights['Distance travelled (km)'].sum()
    sum_time_spent_travelling = df_past_flights['Time Spent Travelling (s)'].sum()/60/60/24 # days
    cnt_countries = df_past_flights['Country'].nunique()
    cnt_cities = df_past_flights['City'].nunique()
    sum_nights_away = df_past_flights['Nights away'].sum()
    #####################################################################



    ################### STREAMLIT - Page #################################

    # containers 
    # con_banner = st.container()
    con_next_flight = st.container()
    con_metrics = st.container()
    con_map = st.container()

    # Columns
    col_flights, col_distance, col_time = st.columns(3, gap='small')
    col_countries, col_cities, col_nights_away = st.columns(3, gap='small')

    # Radio button - select continent
    radio_continent = st.radio(" "
                                ,('🌎', 'Africa', 'Asia', 'Europe', 'North America', 'South America', 'Oceania')
                                ,index=0
                                ,key='radio_continent'
                                ,horizontal=True)

    st.markdown('***')

    ################# By Continent - Metrics Calculations ##################
    cnt_flights_filtered = df_geo[df_geo['Continent Name']==radio_continent]['Visits'].sum()
    sum_distance_travelled_filtered = df_geo[df_geo['Continent Name']==radio_continent]['Distance travelled (km)'].sum()
    sum_time_spent_travelling_filtered = df_geo[df_geo['Continent Name']==radio_continent]['Time Spent Travelling (s)'].sum()/60/60/24
    cnt_countries_filtered = df_geo[df_geo['Continent Name']==radio_continent]['Country'].nunique()
    cnt_cities_filtered = df_geo[df_geo['Continent Name']==radio_continent]['City'].nunique()
    sum_nights_away_filtered = df_geo[df_geo['Continent Name']==radio_continent]['Nights away'].sum()
    ########################################################################

    ################## Metrics #############################################
    with col_flights:
        st.metric('Flights'
            , cnt_flights if radio_continent=='🌎' else cnt_flights_filtered
            , delta=cnt_flights)
    with col_distance:
        st.metric('Distance (km)'
            , millify(sum_distance_travelled, precision=2) if radio_continent=='🌎' else millify(sum_distance_travelled_filtered, precision=2)
            , delta=millify(sum_distance_travelled, precision=2))
    with col_time:
        st.metric('Time on :airplane: (days)'
            , millify(sum_time_spent_travelling, precision=1) if radio_continent=='🌎' else millify(sum_time_spent_travelling_filtered, precision=1)
            , delta=millify(sum_time_spent_travelling, precision=1))

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

    ########################################################################

    ######################## Hover data stats ###############################
    df_map_data_stats = df_geo.groupby(['Country', 'alpha-3', 'Capital', 'Sub-region Name'])\
                            .agg({'Visits':'sum', 'Nights away':'sum'}).reset_index()\
                            .sort_values(by=['Nights away'])                             
    ########################################################################

    ################## Scratch Map #########################################
    data_on_hover = ['Capital', 'Sub-region Name', 'Visits', 'Nights away'] # list
    rename_cols = {'alpha-3':'Country Code'} # dict
    config = {'displayModeBar': False, 'responsive': True}

    with st.spinner('Loading...'):
        if radio_continent == '🌎':
                st.plotly_chart(
                    fn_create_scratch_map(df_map_data_stats, "alpha-3", "Country", "Nights away"
                                        , rename_cols, data_on_hover, scope='world', projection='orthographic')
                    ,config=config
                    ,use_container_width=True
                )
        elif radio_continent == 'Africa':
                st.plotly_chart(
                    fn_create_scratch_map(df_map_data_stats, "alpha-3", "Country", "Nights away"
                                        , rename_cols, data_on_hover, scope='africa')
                    ,config=config
                    ,use_container_width=True
                )
        elif radio_continent == 'Asia':
                st.plotly_chart(
                    fn_create_scratch_map(df_map_data_stats, "alpha-3", "Country", "Nights away"
                                        , rename_cols, data_on_hover, scope='asia')
                    ,config=config
                    ,use_container_width=True
                )
        elif radio_continent == 'Europe':
                st.plotly_chart(
                    fn_create_scratch_map(df_map_data_stats, "alpha-3", "Country", "Nights away"
                                        , rename_cols, data_on_hover, scope='europe')
                    ,config=config
                    ,use_container_width=True
                )
        elif radio_continent == 'North America':
                st.plotly_chart(
                    fn_create_scratch_map(df_map_data_stats, "alpha-3", "Country", "Nights away"
                                        , rename_cols, data_on_hover, scope='north america')
                    ,config=config
                    ,use_container_width=True
                )
                st.markdown("""
                    <sub><u>Note:</u> **Bermuda** and **Barbados** are not represented on 
                    this map. However, the metrics account for the trips to these countries.</sub>
                    """, unsafe_allow_html=True)          
        elif radio_continent == 'South America':
                st.plotly_chart(
                    fn_create_scratch_map(df_map_data_stats, "alpha-3", "Country", "Nights away"
                                        , rename_cols, data_on_hover, scope='south america')
                    ,config=config
                    ,use_container_width=True
                )             
        elif radio_continent == 'Oceania':
                st.error('There is no map info in plotly choropleth... Sorry.... but nothing I can do for now.')
        else: st.write()

    ########################################################################


    ################## Temporary - degub #############################################

    # Dataframe
    # st.dataframe(df)
    # with st.expander('Click to see data... (for debugging)'):
    #     st.dataframe(df)
    #     st.write("Past flights")
    #     st.dataframe(df_past_flights)
    #     st.write(datetime_now, datetime_in_utc)
    #     st.write(datetime_now.date())
    #     st.write("Today's flights")
    #     st.dataframe(df_todays_flights)
    #     st.write("Upcoming flights")
    #     st.dataframe(df_future_flights)
    #     st.dataframe(df_geo)
    # st.dataframe(df_country_codes)
    # st.dataframe(fn_country_code_data())

    # print(df.head())