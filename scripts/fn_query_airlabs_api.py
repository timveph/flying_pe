import requests
import json
import streamlit as st


@st.experimental_memo(ttl=900)
def fn_query_airlabs_api(method='ping', flight_iata=None) -> dict:
    """
    method: 'ping' | 'flight'
    flight_iata: Flight Number e.g. BA138

    More info about method 'flight': https://airlabs.co/docs/flight
    """

    params = {
    'api_key': st.secrets["airLabsApiKey"],
    'flight_iata': flight_iata
    }
    
    # method = 'ping' - use this to get metadata info about account e.g. how many calls left this month, day, hour
    method = method # flight
    api_base = 'http://airlabs.co/api/v9/'
    api_result = requests.get(api_base+method, params)
    api_response = api_result.json()
    json_return = json.dumps(api_response, indent=4, sort_keys=True)
    return json_return