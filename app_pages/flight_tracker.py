import re
import json
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
import time
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
# from scripts.fn_query_airlabs_api import fn_query_airlabs_api
import scripts.fn_query_airlabs_api as airlabs
from scripts.fn_calc_distance import fn_calc_distance
from scripts.fn_calc_midpoint import fn_calc_midpont
from scripts.fn_create_maps import fn_create_track_map
from scripts.fn_data_prep import fn_data_attributes
from scripts.fn_translate import fn_translate

def fn_create_dashboard(df, remaining_requests, language):
    # st.write(df) # debug
    # st.write(df.dtypes) # debug
    st.markdown(f"#### {fn_translate(language, 'Next flight')}", unsafe_allow_html=True)
    st.markdown("***")
    col1, col2, col3 = st.columns([3,1,3])
    with col1:
        st.markdown(f"{fn_translate(language, '**Departing**')}")
        st.markdown(f"##### {df['City']} ({df['Airport Code (IATA)']}) ####")
        st.markdown(f"**{df['Destination Start Time']}** ({df['alpha-3']})") 
        st.markdown(f"""
                    **{df['Event Start'].replace(tzinfo=timezone.utc).astimezone(tz=None)
                            }** ({fn_translate(language, 'local')})
                    """) 

    with col3:
        st.markdown(f"{fn_translate(language, '**Landing at**')}")
        st.markdown(f"##### {df['Arrival Airport']} ####")
        st.markdown(f"""**{df['Destination End Time']}** ({df['alpha-3']})""")
        st.markdown(f"""
                    **{df['Event End'].replace(tzinfo=timezone.utc).astimezone(tz=None)
                    }** ({fn_translate(language, 'local')})
                    """)  

    # chart - for scheduled flight
    (dep_lat, dep_lon) = df['Departing Coordinates'] # unpack tuple 'departing_coordinates' into seperate variables
    (arr_lat, arr_lon) = df['Arriving Coordinates']
    list_lat = [dep_lat, arr_lat] # create input for graph
    list_lon = [dep_lon, arr_lon] # create input for graph
    midpoint = fn_calc_midpont(df['Arriving Coordinates'], df['Departing Coordinates'])
    fig = fn_create_track_map(list_lat, list_lon, midpoint)
    config = {'displayModeBar': False}

    st.plotly_chart(fig
                    ,theme="streamlit"
                    ,config=config
                    ,use_container_width=True)
    
    st.markdown(f"{fn_translate(language, '<sub>Number of queries left: ')} {remaining_requests}</sub>",unsafe_allow_html=True)


def app():
    ### variables ###
    language = st.session_state.language # set from the main page where the radio button is defined

    date_format = "%d/%m/%Y %H:%M:%S"
    timezone = 'Europe/London'
    utc_timezone = ZoneInfo("UTC")
    current_datetime_uk = datetime.now(ZoneInfo(timezone))
    utc_datetime = datetime.utcnow()
    date_uk = current_datetime_uk.date()
    time_uk = current_datetime_uk.time()

    ### Get remaining requests ###
    requests_left = json.loads(airlabs.fn_query_airlabs_api('ping'))
    requests_left = int(requests_left['request']['key']['limits_total'])
    # st.write(int(requests_left['request']['key']['limits_total']))

    # Get data from spreadsheet + attributes
    df = fn_data_attributes()
    # Get today's flight info
    df_todays_flights = df[(df['Event Start Date'] == utc_datetime.date()) 
                            | (df['Event End Date'] == utc_datetime.date())
                            ] # could be more than 1

    # Get future flights
    df_future_flights = df[(df['Destination End Time'] > utc_datetime)].iloc[0]
    
    
    # df_todays_flights = pd.DataFrame() # debug/test

    # Check if Paulina is flying today
    if requests_left <= 3:
        st.write(f"{fn_translate(language, 'Unfortunately, we cannot track any flights')}")

    # If there is no flights today, get next flight from spreadsheet
    elif df_todays_flights.empty:
        fn_create_dashboard(df_future_flights, requests_left, language)

    else: 
        departing_time_utc = df_todays_flights['Event Start'].item()
        # departing_time = datetime.strptime(departing_time, date_format)
        # departing_time_utc = departing_time.astimezone(utc_timezone)
        arriving_time_utc = df_todays_flights['Event End'].item()
        # arriving_time = datetime.strptime(arriving_time, date_format)
        # arriving_time_utc = arriving_time.astimezone(utc_timezone)

        # Scheduled 
        if departing_time_utc - timedelta(hours=1) >= utc_datetime:
            st.markdown(f"{fn_translate(language, '**Live tracking** info from <u>1 hour</u> before the flight.')}",unsafe_allow_html=True)
            
            # how to account for more than 1 flight per day
            # for now, just get one flight
            df_todays_flights = df_todays_flights.iloc[0] # change to <class 'pandas.core.series.Series'>
            # That is how the function fn_create_dashboard receives data. If you want to send it a dataframe,
            # we must adjust the function to pull out the .item() of all columns

            fn_create_dashboard(df_todays_flights, requests_left, language)
        
        # Arrived/ Landed
        elif arriving_time_utc <= utc_datetime: # no flight info a few minutes after flight has landed
            st.write(f'{fn_translate(language, "The flight has landed at approximately ")} {arriving_time_utc}')
            fn_create_dashboard(df_future_flights, requests_left, language)
        
        # En-route
        else:
            flight_no_str = df_todays_flights['Flight Number'].to_string(index=False)
            departing_coordinates = df_todays_flights['Departing Coordinates'].item()
            flight_iata = 'BA'+str(re.findall(r'\d+', flight_no_str)[0])
            api_data = airlabs.fn_query_airlabs_api('flight', flight_iata)
            a = json.loads(api_data)
            # st.write(a)
            
            #check for error message - meaning flight is not found i.e. it has landed and no more flight tracking info
            # should this error check be placed in function? 
            if 'error' in a:
                st.write(f"{fn_translate(language, 'Flight {flight_iata} has landed at approximately ')}{arriving_time_utc}")
                fn_create_dashboard(df_future_flights, requests_left, language)
            else:
                flight_info = airlabs.fn_flight_tracking_info(a['response'], flight_iata)

                # Create tracking dashboard
                con_metrics = st.container()
                con_progress = st.container()
                con_map = st.container()
                st.markdown('---')

                with con_metrics:
                    col1, col2, col3, col4, col5, col6 = st.columns([3,1,4,4,1,3])
                    with col1:
                        st.markdown(f"{fn_translate(language, '**Departing**')}")
                        st.markdown(f"#### {flight_info['dep_city']} ####")
                        st.markdown(f"""**{flight_info['dep_actual_utc'] 
                                                or flight_info['dep_time_utc'] 
                                                or flight_info['dep_time']}**
                                        """)  
                    with col2:
                        st.write()
                    with col3:
                        if flight_info['duration'] is not None:
                            duration = '{:02d}H{:02d}m'.format(*divmod(flight_info['duration'], 60))
                        else: duration = 0
                        if flight_info['status'] == 'landed':
                            eta = 0
                        elif flight_info['eta'] is not None:
                            eta = '{:02d}H{:02d}m'.format(*divmod(flight_info['eta'], 60))
                        else: eta = duration

                        st.metric(fn_translate(language, 'Time remaining'), eta, f"{duration} total")

                        speed = flight_info['speed']
                        if speed is not None:
                            speed = speed
                        else: speed = 0
                        st.metric(fn_translate(language, 'Speed'), f"{speed} km/h")
                        
                        
                    with col4:
                        try:
                            distance_total = df_todays_flights['Distance travelled (km)']
                            destination_coords = df_todays_flights['Arriving Coordinates']
                        except:
                            distance_total=0
                            destination_coords = (0,0)
                            
                        current_coords = (flight_info['lat'], flight_info['lng'])
                        if current_coords == (None, None):
                            current_coords = df_todays_flights['Departing Coordinates']

                        if flight_info['status'] == 'landed':
                            distance_left = 0
                        else: distance_left = fn_calc_distance(current_coords, destination_coords)

                        st.metric(fn_translate(language, 'Distance Remaining'), f"{int(distance_left)} km", delta=f"{int(distance_total)} km")
                    
                        altitude = flight_info['alt']
                        if altitude is not None:
                            altitude = altitude
                        else: altitude = 0
                        st.metric(fn_translate(language, 'Altitude'), f"{altitude} m")

                    with col5:
                        st.write()
                    with col6:
                        st.markdown(f"{fn_translate(language, '**Landing at**')}")
                        st.markdown(f"#### {flight_info['arr_city']} ####")
                        st.markdown(f"""**{flight_info['arr_actual_utc'] 
                                            or flight_info['arr_time_utc']
                                            or flight_info['arr_time']}**
                                        """)    

                with con_progress:    
                    st.progress(flight_info['percent'] or 0)
                    # st.write(f"{flight_info['lat']},{flight_info['lng']}")


                with con_map:
                    (dep_lat, dep_lon) = departing_coordinates # unpack tuple 'departing_coordinates' into seperate variables
                    curr_lat = flight_info['lat']
                    curr_lon = flight_info['lng']
                    list_lat = [dep_lat, curr_lat] # create input for graph
                    list_lon = [dep_lon, curr_lon] # create input for graph

                    midpoint = fn_calc_midpont(df['Arriving Coordinates'], df['Departing Coordinates'])
                    fig = fn_create_track_map(list_lat, list_lon, midpoint)
                    config = {'displayModeBar': False}

                    st.plotly_chart(fig
                                    ,theme="streamlit"
                                    ,config=config
                                    ,use_container_width=True)
                    st.caption(flight_iata)


                st.markdown(f"{fn_translate(language, '<sub>Number of queries left: ')} {requests_left}</sub>",unsafe_allow_html=True)


# 2. What info to show after the flight has landed?
# 3. Probably need some additional error handling