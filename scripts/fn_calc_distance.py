
from geopy.distance import great_circle

def fn_calc_distance(start_point, end_point, unit_measure='km'):
    """
    A function to calculate the distance in km or m between two coordinates

    params:
    tuple: (lat,long): of current point
    tuple: (lat, long): of end point
    str: a unit of measure: km or m (default km)

    return:
    distance in either km or m
    
    """
    if unit_measure in ['km', 'k', 'kilometer', 'kilometers']:
        return great_circle(start_point, end_point).km
    elif unit_measure in ['m', 'mile', 'miles']:
        return great_circle(start_point, end_point).miles
    else:
        return great_circle(start_point, end_point).km