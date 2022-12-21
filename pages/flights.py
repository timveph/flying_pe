import re
import json
import datetime
import streamlit as st
from scripts.fn_read_spreadsheet import fn_read_spreadsheet
from scripts.fn_query_airlabs_api import fn_query_airlabs_api
import scripts.fn_config_streamlit_pages as config

config.fn_set_page_title("Tracking")
config.fn_apply_css()


# variables
datetime_in_utc = datetime.datetime.utcnow()

# How many requests do I have left this month
requests_left = json.loads(fn_query_airlabs_api('ping'))
st.write(f"Number of queries left: {requests_left['request']['key']['limits_total']}")


try:
    df = fn_read_spreadsheet()
    df_todays_flights = df[(df['Event Start Date'] == datetime_in_utc.date()) 
                            | (df['Event End Date'] == datetime_in_utc.date())
                            ] # could be more than 1
except:
    st.write("Please refresh the page")


### Data processing ###

def fn_flight_tracking_info(adict):
    list_of_keys_from_flight = ['alt', 'arr_city', 'arr_time_utc', 'arr_actual_utc', 'dep_actual_utc', 'dep_time_utc'
                                , 'dep_city', 'dir', 'duration', 'eta', 'hex', 'lat', 'lng', 'percent', 'speed'
                                , 'status', 'updated']
    list_of_keys_from_flights = ['alt', 'dir', 'hex','lat', 'lng', 'speed', 'status', 'updated']

    subset = {key: adict[key] for key in list_of_keys_from_flight}
    if None in subset.values(): # first test if subset has null values for any keys
        gap_list = []
        for key in list_of_keys_from_flights: # if so, loop through list of keys from flightS and ...
            if subset[key]: # check if any of those keys are null in the subset
                continue
            else: # If they are, make a list of keys needed
                gap_list.append(key)
        data = fn_query_airlabs_api('flights', flight_iata) # make another call to the API but with different method
        dict_flights = json.loads(data)['response'] # get dict
        gap_subset = {key: dict_flights[key] for key in gap_list} # keep only the missing fields
        subset = dict(list(gap_subset.items()) + list(subset.items())) 
    else:
        print('') # do nothing


    return subset



try:
    flight_no_str = df_todays_flights['Flight Number'].to_string(index=False)
    flight_iata = 'BA'+str(re.findall(r'\d+', flight_no_str)[0])
    # flight_iata = 'BA249'
    api_data = fn_query_airlabs_api('flight', flight_iata)
    a = json.loads(api_data)
    flight_info = fn_flight_tracking_info(a['response'])

except:
    st.write("Pe is grounded! Check back tomorrow!")

try:
    with st.expander("debugging info..."):
            st.text(flight_iata)
            st.write(a.keys())
            st.write(fn_flight_tracking_info(a['response']))
            # data = fn_query_airlabs_api('flights', flight_iata)
            # st.write(json.loads(data)['response']) 
            # st.write(a)


    con_current_flight = st.container()

    with con_current_flight:


        col_start, col_status, col_end = st.columns([1,5,1])
        with col_start:
            st.markdown(f"**{flight_info['dep_city']}**")
            st.markdown(f"**{flight_info['dep_actual_utc'] or flight_info['dep_time_utc']}**")
            
        
        with col_status:
            duration = '{:02d}H{:02d}m'.format(*divmod(flight_info['duration'], 60)) 
            eta = '{:02d}H{:02d}m'.format(*divmod(flight_info['eta'], 60)) 
            if flight_info['status'] == 'scheduled':
                st.write(flight_info['status'])
            elif flight_info['status'] == 'en-route':
                st.progress(flight_info['percent'])
                st.markdown(f"""
                <center>Duration: {duration} 
                <br>Time left: {eta}</center>
                """, unsafe_allow_html=True)
            elif flight_info['status'] == 'landed':
                st.write(flight_info['status'])
            else: 
                st.write('')


        with col_end:
            st.markdown(f"**{flight_info['arr_city']}**")
            st.markdown(f"**{flight_info['arr_actual_utc'] or flight_info['arr_time_utc']}**")
            

    st.markdown("<br><br><sub> Note: Flight info delayed by 15 minutes </sub>", unsafe_allow_html=True)

except:
    st.write("no flight data i.e. no current flight i.e. no flight today")

# subset = {'a': 2, 'b': 8, 'c': ''}
# gap_subset = {'a': 2, 'b': '', 'c': ''}
# subset = dict(list(gap_subset.items()) + list(subset.items())) 
# st.write(subset)




# st.write(a)
    

    


# Inspiration: https://amaral.northwestern.edu/blog/step-step-how-plot-map-slider-represent-time-evolu

# Big inspiration: http://vis.csail.mit.edu/pubs/animated-vega-lite/editor/#/url/vega-lite/N4Ig7glgJgLgFiAXARgAzoDQjgUwgczhiQDZMQAHAJwHsArHAYxghoDslQYBPCnJEDgCOAVwCGAGwCiYqvBBZGEiBSkAPGDjbFEAbV2oMqALoZdAFkwAOdMeMBfLBLHccVJLtBQxMMZxAiVBIC3r4A9GA0QVAAtMhoALYAdHQAzuwKIABmUQk+-jx8AjA0FPTpHFhZOD6B-IggjDQi2lQQOKkg9o4geVQA1gW89SD4ODSpcGJFVRASwQ0AxFkA7KurmakwtP0ji2IHXY5ePn6IoIELIKFiYQBGEFRQW227qUmMqQBuXVgUsmIEp09KA2ICRoxAlQtDAAPpZKjgzY4CRMHRcYYCMoQbSZDINFgJNy-EAPNhQfw4igiHQgRFsMaZBI4pDILB5NRIADMJAArFgtjgKKysGCiSEXEcMKCkQ1IOSaGB4YjxQKUWihkUGtjcVh8SBCcS-tCoBBGD56qAxOSPKAsu0JBSGmxYd5uJkJJp-Dg1NQBNaIAlYV9JCJ+N1pdkHU6QC63Zl8OjBL73A0A0GQxIwwACGLZgBMqCODgjMvF2pgnTVqOYmpGOuIeo4DQSzVS4y+RqjKOeHhAqT4jHanRLpgN9NSOSoCVtjUkkOcXoJNAAciIEnc3AAKULrpJugCUmTEwNjrslxyjnuJ50oAJncpxUEVyqR3THfUGDSHVCU-CwWhNKaDL+BI7D4BAMAiFAlrdo6AhgRwPSLpB0GwfaPYIfkPRNGBqZ2tGAgDkww4kqkEAAF6wU05KQawzagP8KpYpWmSZmGrLkDgCQUDwSBZJI7Y9Ox9SFj0pRiEOfG3jRposPijH3gIkJUNC2ivqqIAiaywmhvUqBJMgPSGv4GHwc657ugK5qonWAh3NaFJYPSjJ6IYaDoCYEYGjQNCeiopmEQ0xFDh0Rz2A4QA
# Video: https://www.youtube.com/watch?v=evoV6kvG7z4&t=53s
# source: http://vis.csail.mit.edu/pubs/animated-vega-lite/
# https://github.com/Hskl14/Flight-Aware-Web-Scraping/blob/master/flight_data_to_gexf.py


