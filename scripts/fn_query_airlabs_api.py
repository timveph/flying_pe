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
    # with st.expander("find me in fn_query_airlabs_api.py"):
    #     st.write(json_return)
    return json_return


### Data processing ###
# reducing the dictionary, testing for values, if not there, query another api endpoint
def fn_flight_tracking_info(adict, flight_iata):
    list_of_keys_from_flight = ['alt', 'arr_city'
                                , 'arr_time', 'dep_time'
                                , 'arr_time_utc', 'arr_actual_utc'
                                , 'dep_actual_utc', 'dep_time_utc', 'duration'
                                , 'dep_city', 'dir', 'eta', 'hex', 'lat', 'lng', 'percent', 'speed'
                                , 'status', 'updated']
    list_of_keys_from_flights = ['alt', 'dir', 'hex','lat', 'lng', 'speed', 'status', 'updated']
    # st.write(adict)

    flight_data = adict
    # Check if the dictionary has the desired keys, if not, create them with None value
    for i in list_of_keys_from_flight:
        if flight_data.get(i):
            continue
        else:
            flight_data.update({i:None})


    # Combine dictionaries from two API calls if a key from one set is None
    subset = {key: flight_data[key] for key in list_of_keys_from_flight}
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