
#######################
# Import libraries
import streamlit as st
import altair as alt
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from utils import get_rush_table_wide, get_rec_table_wide, get_player_scatter_vertical, get_player_scatter_vertical_rush, get_player_scatter_vertical_pass, get_pass_table_wide

#######################
# Page configuration
st.set_page_config(
    page_title="mean-median",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("<h1 style='text-align: center; font-family:Courier New;'>mean-median</h1>", unsafe_allow_html=True)

#######################
# CSS styling with Toggle
# Checkbox to toggle between centered view and wide mode
centered_view = st.checkbox("PC View", value=False)

# Apply CSS based on the checkbox state
if centered_view:
    st.markdown("""
        <style>
            /* Center-align headers in the dataframe */
            .dataframe-container th {
                text-align: center !important;
            }
            /* Center the main container with max-width for centered view */
            [data-testid="stAppViewContainer"] {
                max-width: 60% !important;
                padding-left: 2rem;
                padding-right: 2rem;
                margin: auto;
            }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
            /* Center-align headers in the dataframe */
            .dataframe-container th {
                text-align: center !important;
            }
            /* Wide mode with full width */
            [data-testid="stAppViewContainer"] {
                max-width: 100% !important;
                padding-left: 1rem;
                padding-right: 1rem;
            }
        </style>
    """, unsafe_allow_html=True)

#######################
# READ IN DATA
all_data = pd.read_csv(r"data/week_9.csv")
all_data = all_data.astype({'season': int})

#####################
## START TABS
tab1, tab2, tab3 = st.tabs(["Receiving", "Rushing", "Passing"])

with tab1:
    player_list = list(all_data[all_data.market=='receiving_yards'].player.sort_values().unique())
    player = st.selectbox(" ", player_list)
    player_season = all_data[all_data.player==player].reset_index(drop=True)

    col1, col2 = st.columns([1.35, 1])

    with col1:
        st.plotly_chart(get_player_scatter_vertical(player_season), config={'displayModeBar': False}, theme=None, use_container_width=True)
    with col2:
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown('<center>Game Log', unsafe_allow_html=True)

        st.dataframe(get_rec_table_wide(player_season),
                     hide_index=True, height=475,
                     column_config={
                         'Week': {'alignment': 'left', 'header': 'Week'},
                         'Yards': {'alignment': 'left', 'header': 'Yards'},
                         'Targets': {'alignment': 'left', 'header': 'Targets'},
                         'Rec': {'alignment': 'left', 'header': 'Rec'},
                         'TDs': {'alignment': 'left', 'header': 'TDs'}
                     },
                     use_container_width=True)

with tab2:
    player_list = list(all_data[all_data.market=='rushing_yards'].player.sort_values().unique())
    player = st.selectbox(" ", player_list)
    player_season = all_data[all_data.player==player].reset_index(drop=True)

    col1, col2 = st.columns([1.5, 1])

    with col1:
        st.plotly_chart(get_player_scatter_vertical_rush(player_season), config={'displayModeBar': False}, theme=None, use_container_width=True)
    with col2:
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown('<center>Game Log', unsafe_allow_html=True)

        st.dataframe(get_rush_table_wide(player_season),
                     hide_index=True, height=475,
                     column_config={
                         'Week': {'alignment': 'left', 'header': 'Week'},
                         'Yards': {'alignment': 'left', 'header': 'Yards'},
                         'Carries': {'alignment': 'left', 'header': 'Carries'}
                     },
                     use_container_width=True)

with tab3:
    player_list = list(all_data[all_data.market=='passing_yards'].player.sort_values().unique())
    player = st.selectbox(" ", player_list)
    player_season = all_data[all_data.player==player].reset_index(drop=True)

    col1, col2 = st.columns([1.18, 1])

    with col1:
        st.plotly_chart(get_player_scatter_vertical_pass(player_season), config={'displayModeBar': False}, theme=None, use_container_width=True)
    with col2:
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown('<center>Game Log', unsafe_allow_html=True)

        st.dataframe(get_pass_table_wide(player_season),
                     hide_index=True, height=475,
                     column_config={
                         'Week': {'alignment': 'left', 'header': 'Week'},
                         'Yards': {'alignment': 'left', 'header': 'Yards'},
                         'Attempts': {'alignment': 'left', 'header': 'Attempts'},
                         'TDs': {'alignment': 'left', 'header': 'TDs'}
                     },
                     use_container_width=True)

# ---- REMOVE UNWANTED STREAMLIT STYLING ----
hide_st_style = """
            <style>
            Main Menu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
            
st.markdown(hide_st_style, unsafe_allow_html=True)