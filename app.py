import streamlit as st
import app_pages.flight_tracker as flight_tracker
import app_pages.home as home
import scripts.fn_config_streamlit_pages as config
from PIL import Image


### Page configuration ###
config.fn_set_page_title("Flying Pe")
config.fn_apply_css()

### Page layout ###
con_banner = st.container()

### Banner ###

with con_banner:
        col_img1, col_img2, col_img3 = st.columns([1,3,1])
        with col_img2:
            banner_image = Image.open("./images/cartoon_Pe_banner.png")
            banner_image = banner_image.resize((349, 90))
            st.image(banner_image)

tab_home, tab_ft = st.tabs(['Stats', 'Flight Tracker'])
with tab_home:
    # page = PAGES[home]
    home.app()

with tab_ft:
    flight_tracker.app()