import streamlit as st
import scripts.fn_config_streamlit_pages as config
from scripts.fn_translate import fn_translate
import app_pages.flight_tracker as flight_tracker
import app_pages.home as home
from PIL import Image


### Page configuration ###
config.fn_set_page_title("Flying Pe")
config.fn_apply_css()


### Page layout ###
con_banner = st.container()

### Banner ###

with con_banner:
        col_lang, col2, col_img = st.columns([1,1,3])
        with col_lang:
            language = st.radio(''
                            ,('🇬🇧','🇵🇱')
                            ,index=0
                            ,horizontal=True
                            ,label_visibility='hidden'
                            ,key='lang'
                            )
            
            if language == '🇬🇧':
                language = 'en'
            elif language == '🇵🇱':
                language = 'pl'

            st.session_state.language = language # initialise the session state 'language' used in sub pages

        with col_img:
            banner_image = Image.open("./images/cartoon_Pe_banner.png")
            banner_image = banner_image.resize((349, 90))
            st.image(banner_image)

tab_home, tab_ft = st.tabs([fn_translate(language,'Stats'), fn_translate(language,'Flight Tracker')])

with tab_home:
    # page = PAGES[home]
    home.app()

with tab_ft:
    flight_tracker.app()