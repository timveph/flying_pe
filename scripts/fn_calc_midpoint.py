from great_circle_calculator.great_circle_calculator import midpoint

def fn_calc_midpont(start_point, end_point):
    """
    Calculates the half-way point along a great circle path between the two points

    params:
    tuple: (lon,lat): of start point
    tuple: (lon, lat): of end point

    return:
    (lon, lat)
    
    """
    # print(f"midpoint: {midpoint(start_point, end_point)}")
    return midpoint(start_point, end_point)