import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random
import streamlit as st
from scripts.fn_translate import fn_translate

### Create plotly diagram ###
@st.cache(max_entries = 5, ttl = 86400)
def fn_create_scratch_map(df, location_col, hover_name, color_map, legend_title, label={}, data_on_hover=[], scope='world', projection = "natural earth"):

    fig = px.choropleth(df
                        , locations=location_col                        
                        # ,color_continuous_scale=px.colors.sequential.Plasma
                        # ,color_continuous_scale=px.colors.sequential.swatches_continuous()
                        , color_continuous_scale=random.choice(['Blues', 'Earth', 'Greens', 'Reds'])  
                        # options: Blackbody,Bluered,Blues,Cividis,Earth,Electric,Greens,Greys,Hot,Jet,Picnic,Portland,Rainbow,RdBu,Reds,Viridis,YlGnBu,YlOrRd.
                        # , color_continuous_scale = ["rgb(166,206,227)", "rgb(31,120,180)", "rgb(178,223,138)"
                        #                         ,"rgb(51,160,44)", "rgb(251,154,153)", "rgb(227,26,28)"]
                        # , color_continuous_midpoint=10
                        # , reversescale=True
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
    
    # Update legend/color bar
    fig.update_layout(coloraxis_colorbar=dict(
            title=legend_title, title_side='top',
            thicknessmode="pixels", thickness=5,
            lenmode="pixels", len=200,
            xanchor="left", x=-0.05,
            yanchor="bottom", y=-0.05,
            orientation='h'
            ,ticks="inside", ticksuffix="",
            dtick=5
        ))

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
def fn_create_track_map(list_lat, list_lon, midpoint):
    (m_lat, m_lon) = midpoint

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
            scope="world",
            # coastlinewidth = 2,
            # fitbounds = "geojson", # locations
            projection_scale = 2.5, # zoom into the map - goes hand in hand with center
            center=dict(lat=m_lat, lon=m_lon) # center the map based on midpoint between start and end coordinates
            # lataxis = dict(
            #     range = [0, 200],
            #     # showgrid = True,
            #     # dtick = 10
            # ),
            # lonaxis = dict(
            #     range = [0, 200],
            #     # showgrid = True,
            #     # dtick = 20
            #     ),
            )
    ) 

    return fig