import re
import json
import datetime
import asyncio
import streamlit as st
from streamlit_echarts import st_echarts
from scripts.fn_read_spreadsheet import fn_read_spreadsheet
# from scripts.fn_query_airlabs_api import fn_query_airlabs_api
import scripts.fn_query_airlabs_api as airlabs
import scripts.fn_config_streamlit_pages as config
from charts.chart_speed import chart_speed

config.fn_set_page_title("Tracking")
config.fn_apply_css()
# with open( "stylesheet/stylesheet.css" ) as css:
#     st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)


# variables
datetime_in_utc = datetime.datetime.utcnow()

# How many requests do I have left this month
requests_left = json.loads(airlabs.fn_query_airlabs_api('ping'))
st.markdown(f"Number of queries left: {requests_left['request']['key']['limits_total']}",unsafe_allow_html=True)


#### Get data from spreadsheet ####
try:
    df = fn_read_spreadsheet()
    df_todays_flights = df[(df['Event Start Date'] == datetime_in_utc.date()) 
                            | (df['Event End Date'] == datetime_in_utc.date())
                            ] # could be more than 1
except:
    st.write("Please refresh the page")



#### Get flight number from spreadsheet ####
### Call API and get flight info ###
try:
    flight_no_str = df_todays_flights['Flight Number'].to_string(index=False)
    flight_iata = 'BA'+str(re.findall(r'\d+', flight_no_str)[0])
    api_data = airlabs.fn_query_airlabs_api('flight', flight_iata)
    a = json.loads(api_data)
    flight_info = airlabs.fn_flight_tracking_info(a['response'], flight_iata)

except:
    st.write("Pe is grounded! Check back tomorrow!")

    # temp - Get a temporary flight - provide the flight number of a flight currently flying
    flight_iata = 'BA244'
    api_data = airlabs.fn_query_airlabs_api('flight', flight_iata)
    a = json.loads(api_data)
    flight_info = airlabs.fn_flight_tracking_info(a['response'], flight_iata)
    st.write(f"Last updated: {flight_info['updated']}")


with st.expander("debugging info..."):
        st.text(flight_iata)
        st.write(a.keys())
        st.write(flight_info)
        # data = fn_query_airlabs_api('flights', flight_iata)
        # st.write(json.loads(data)['response']) 
        # st.write(a)

try:
    con_current_flight = st.container()
    with con_current_flight:
        col_start, col_status, col_end = st.columns([1,5,1])
        with col_start:
            st.markdown(f"**{flight_info['dep_city']}**")
            st.markdown(f"""**{flight_info['dep_actual_utc'] 
                                or flight_info['dep_time_utc'] 
                                or flight_info['dep_time']}**
                        """)          
        
        with col_status:
            try:
                duration = '{:02d}H{:02d}m'.format(*divmod(flight_info['duration'], 60))
                eta = '{:02d}H{:02d}m'.format(*divmod(flight_info['eta'], 60)) 
            except TypeError:
                st.write("duration and eta data is not available from the API")
                duration = '0'
                eta = '0'
                
            if flight_info['status'] == 'scheduled':
                st.write(flight_info['status'])
            elif flight_info['status'] == 'en-route':
                st.progress(flight_info['percent'] or 0)
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
            st.markdown(f"""**{flight_info['arr_actual_utc'] 
                            or flight_info['arr_time_utc']
                            or flight_info['arr_time']}**
                        """)            

    st.markdown("<br><br><sub> Note: Flight info delayed by 15 minutes </sub>", unsafe_allow_html=True)

except:
    st.write("no flight data i.e. no current flight i.e. no flight today")

# subset = {'a': 2, 'b': 8, 'c': ''}
# gap_subset = {'a': 2, 'b': '', 'c': ''}
# subset = dict(list(gap_subset.items()) + list(subset.items())) 
# st.write(subset)



# A countdown timer for flight_info['eta']
async def eta_countdown(eta):
    # Needs some error handling if 'eta' is None or zero or undefined
    n = flight_info['eta']
    n = 5
    for secs in range(n, 0, -1):
        mm, ss = secs//60, secs%60
        eta.metric("Arriving in...", f"{mm:02d}:{ss:02d}")
        r = await asyncio.sleep(1)


col_speed, col_altitude = st.columns(2)
with col_speed:
    speed_chart = chart_speed(flight_info['speed'])
    st_echarts(
        options=speed_chart
        # theme= Union[str, Dict]
        # ,events={"click" : "function () {myChart.setOption({'series': [{'data': [{'value': +(Math.random() * 1000).toFixed(2)}]}]});}, 2000)"
        #         }
        ,renderer="svg"
        # map: Map
        ,key="guage_speed"
        # ,height="250px"
        # ,width=""
    )
with col_altitude:
    st.metric('Altitude', flight_info['alt'])
    eta = st.empty()
    asyncio.run(eta_countdown(eta))
    
    





    


# Inspiration: https://amaral.northwestern.edu/blog/step-step-how-plot-map-slider-represent-time-evolu

# Big inspiration: http://vis.csail.mit.edu/pubs/animated-vega-lite/editor/#/url/vega-lite/N4Ig7glgJgLgFiAXARgAzoDQjgUwgczhiQDZMQAHAJwHsArHAYxghoDslQYBPCnJEDgCOAVwCGAGwCiYqvBBZGEiBSkAPGDjbFEAbV2oMqALoZdAFkwAOdMeMBfLBLHccVJLtBQxMMZxAiVBIC3r4A9GA0QVAAtMhoALYAdHQAzuwKIABmUQk+-jx8AjA0FPTpHFhZOD6B-IggjDQi2lQQOKkg9o4geVQA1gW89SD4ODSpcGJFVRASwQ0AxFkA7KurmakwtP0ji2IHXY5ePn6IoIELIKFiYQBGEFRQW227qUmMqQBuXVgUsmIEp09KA2ICRoxAlQtDAAPpZKjgzY4CRMHRcYYCMoQbSZDINFgJNy-EAPNhQfw4igiHQgRFsMaZBI4pDILB5NRIADMJAArFgtjgKKysGCiSEXEcMKCkQ1IOSaGB4YjxQKUWihkUGtjcVh8SBCcS-tCoBBGD56qAxOSPKAsu0JBSGmxYd5uJkJJp-Dg1NQBNaIAlYV9JCJ+N1pdkHU6QC63Zl8OjBL73A0A0GQxIwwACGLZgBMqCODgjMvF2pgnTVqOYmpGOuIeo4DQSzVS4y+RqjKOeHhAqT4jHanRLpgN9NSOSoCVtjUkkOcXoJNAAciIEnc3AAKULrpJugCUmTEwNjrslxyjnuJ50oAJncpxUEVyqR3THfUGDSHVCU-CwWhNKaDL+BI7D4BAMAiFAlrdo6AhgRwPSLpB0GwfaPYIfkPRNGBqZ2tGAgDkww4kqkEAAF6wU05KQawzagP8KpYpWmSZmGrLkDgCQUDwSBZJI7Y9Ox9SFj0pRiEOfG3jRposPijH3gIkJUNC2ivqqIAiaywmhvUqBJMgPSGv4GHwc657ugK5qonWAh3NaFJYPSjJ6IYaDoCYEYGjQNCeiopmEQ0xFDh0Rz2A4QA
# Video: https://www.youtube.com/watch?v=evoV6kvG7z4&t=53s
# source: http://vis.csail.mit.edu/pubs/animated-vega-lite/
# https://github.com/Hskl14/Flight-Aware-Web-Scraping/blob/master/flight_data_to_gexf.py


