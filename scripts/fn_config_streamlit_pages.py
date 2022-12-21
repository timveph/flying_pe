import streamlit as st

def fn_set_page_title(pageTitle):

    page_icon = "./images/Flying_Pe.png"
    layout="centered"

    # return f"page_title='{pageTitle}', page_icon='{page_icon}', layout='{layout}'"
    return st.set_page_config(page_title=pageTitle
                    ,page_icon = page_icon
                    ,layout=layout
                    )

def fn_apply_css():
    # Hide menu & footer
    hide_menu_style = """
                        <style>
                        #MainMenu {visibility: visible; }
                        footer {visibility: hidden;}
                        </style>
            """
    return st.markdown(hide_menu_style, unsafe_allow_html=True)

    