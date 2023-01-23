from great_circle_calculator.great_circle_calculator import midpoint
import re

def fn_calc_midpoint(start_point, end_point):
    """
    Calculates the half-way point along a great circle path between the two points

    params:
    tuple: (lon, lat): of start point
    tuple: (lon, lat): of end point

    return:
    (lon, lat)
    
    """
    # print(f"midpoint: {midpoint(start_point, end_point)}")
    # try:
    return midpoint(start_point, end_point)
    # except ValueError as e:
    #     e = str(e)
    #     print('>>> e', type(e))
    #     print('>>> e', e)

    #     print('>>>> ', start_point)
    #     start_point = tuple(reversed(start_point))
    #     print('>>>> ', start_point)
    #     # end_point = tuple(reversed(end_point))
    #     # if 'is probably reversed' in e:
    #     #     res = re.findall(r'\(.*?\)', e)
    #     #     print('>>> res',res)
    #     return midpoint(start_point, end_point)
    # except  TypeError as t:
    #     print('t', t)
