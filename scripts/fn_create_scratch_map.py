import pandas as pd
import plotly.express as px
import random

### Create plotly diagram ###
def fn_create_scratch_map(df, location_col, hover_name, color_map, label={}, hover_data=[], scope='world', projection = "natural earth"):

    fig = px.choropleth(df
                        , locations=location_col                        
                        # ,color_continuous_scale=px.colors.sequential.Plasma
                        # ,color_continuous_scale=px.colors.sequential.swatches_continuous()
                        , color_continuous_scale="Viridis"
                        # ,color_discrete_sequence = px.colors.cyclical.swatches
                        # , range_color=(0,max_nights_away)
                        ,hover_name = hover_name
                        ,hover_data = hover_data
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
                    , resolution=110
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