import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random
import streamlit as st

### Create plotly diagram ###
@st.cache(max_entries = 5, ttl = 86400)
def fn_create_scratch_map(df, location_col, hover_name, color_map, label={}, data_on_hover=[], scope='world', projection = "natural earth"):

    fig = px.choropleth(df
                        , locations=location_col                        
                        # ,color_continuous_scale=px.colors.sequential.Plasma
                        # ,color_continuous_scale=px.colors.sequential.swatches_continuous()
                        , color_continuous_scale="Viridis"
                        # ,color_discrete_sequence = px.colors.cyclical.swatches
                        # , range_color=(0,max_nights_away)
                        ,hover_name = hover_name
                        ,hover_data = data_on_hover
                        ,color=color_map
                        ,labels=label
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
                    , resolution=110 # this takes longer to render - slows page load
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

@st.experimental_memo(max_entries = 5, ttl=900)
def fn_create_track_map(list_lat, list_lon):
    random_color = random.choice(['wheat', 'snow', 'white', 'ivory'])
    fig = go.Figure(data=go.Scattergeo(
        lat = list_lat, # lat [from, to]
        lon = list_lon, # lon [from, to]
        mode = 'lines+markers',
        line = dict(width = 3,
            color = random_color
            ,dash = "dashdot"
            ),
        marker = dict(
            color = (random_color, random_color)
            ,symbol = ('circle-open-dot','circle-dot')
            ,size = (10,15)
        )
        
    ))

    fig.update_layout(
        # title_text = f"{flight_info['dep_city']} to {flight_info['arr_city']}",
        showlegend = False,
        autosize = False,
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        geo = dict(
            fitbounds = "locations", # geojson
            resolution = 110, # this takes longer to render - slows page load
            bgcolor='rgba(0,0,0,0)',
            # showland = True,
            # showlakes = True,
            # landcolor = 'rgb(204, 204, 204)',
            showcountries=True,
            countrycolor = 'grey',
            # lakecolor = 'rgb(255, 255, 255)',
            projection_type = "equirectangular",
            # projection_type = "natural earth",
            # projection_type = "orthographic",
            # projection_scale = 2,
            scope="world",
            # coastlinewidth = 2,
            # lataxis = dict(
            #     range = [10, 80],
            #     # showgrid = True,
            #     # dtick = 10
            # ),
            # lonaxis = dict(
            #     range = [-0.3, -90],
            #     # showgrid = True,
            #     # dtick = 20
            #     ),
            )
    ) 

    return fig