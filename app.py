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
from utils import get_rec_table_skinny, get_rush_table_wide, get_rec_table_wide, get_player_scatter_vertical, get_player_scatter_horizontal, get_player_scatter_vertical_rush, get_player_scatter_vertical_pass, get_pass_table_wide

#######################
# Page configuration
st.set_page_config(
    page_title="mean-median",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")

# alt.themes.enable("dark")

#######################
# CSS styling
st.markdown("""
<style>

[data-testid="block-container"] {
    padding-left: 2rem;
    padding-right: 2rem;
    padding-top: 2rem;
    padding-bottom: 0rem;
    margin-bottom: -7rem;
}

[data-testid="stVerticalBlock"] {
    padding-left: 0rem;
    padding-right: 0rem;
}

[data-testid="stMetric"] {
    background-color: #393939;
    text-align: center;
    padding: 15px 0;
}

[data-testid="stMetricLabel"] {
  display: flex;
  justify-content: center;
  align-items: center;
}

[data-testid="stMetricDeltaIcon-Up"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

[data-testid="stMetricDeltaIcon-Down"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

</style>
""", unsafe_allow_html=True)

#######################
# READ IN DATA
all_data = pd.read_csv(r"data/week_9.csv")
all_data = all_data.astype({'season': int})

st.markdown("<h1 style='text-align: center; font-family:Courier New;'>mean-median</h1>", unsafe_allow_html=True)
#####################
## START TABS
tab1, tab2, tab3 = st.tabs(["Receiving", "Rushing", "Passing"])

with tab1:
    player_list = list(all_data[all_data.market=='receiving_yards'].player.sort_values().unique())
    player = st.selectbox(" ", player_list)
    player_season = all_data[all_data.player==player].reset_index(drop=True)

    ######################
    # PRIZE PICKS AND UNDERDOG LINES
    # with st.container():
    # col1,col2 = st.columns(2)
    # with col1:
    #     st.markdown(f"<center><h1 style='color:yellow'><small>Udog </small>{player_season[player_season.market=='receiving_yards'].fillna(0).ud_line.median()}</h1></center>",unsafe_allow_html=True)
    # with col2:
    #     st.markdown(f"<center><h1 style='color:purple'><small>Ppicks </small>{player_season[player_season.market=='receiving_yards'].fillna(0).pp_line.median()}</h1></center>",unsafe_allow_html=True)
    
    # Values to display
    ud_line_median = player_season[player_season.market == 'receiving_yards'].fillna(0).ud_line.median()
    pp_line_median = player_season[player_season.market == 'receiving_yards'].fillna(0).pp_line.median()

    # Display values in one line with different colors
    html_string = f"""
    <div style="display: flex; justify-content: center; align-items: center;">
        <div style="text-align: center; margin-right: 20px;">
            <h1 style='color: yellow;'>{ud_line_median}</h1>
        </div>
        <div style="text-align: center;">
            <h1 style='color: purple;'>{pp_line_median}</h1>
        </div>
    </div>
    """

    # Render in Streamlit
    st.markdown(html_string, unsafe_allow_html=True)
    
    ######################
    ## VERTICAL SCATTER & SKINNY TABLE WITH BORDER
    config = {'displayModeBar': False}

    # with st.container(border=True):
    col1,col2 = st.columns([1.35,1])
    with col1:
        st.plotly_chart(get_player_scatter_vertical(player_season), config = config, theme=None,use_container_width=True)
    with col2:
        st.markdown("####")
        st.markdown("###")
        st.dataframe(get_rec_table_wide(player_season),hide_index=True, height=475,column_config={'week':'Week','receiving_yards': 'Yards', 'targets':'Target','receptions':'Catch','receiving_tds':'TDs'},use_container_width=True)


with tab2:
    player_list = list(all_data[all_data.market=='rushing_yards'].player.sort_values().unique())
    player = st.selectbox(" ", player_list)
    player_season = all_data[all_data.player==player].reset_index(drop=True)

    ######################
    # PRIZE PICKS AND UNDERDOG LINES
    # with st.container():
    # col1,col2 = st.columns(2)
    # with col1:
    #     st.markdown(f"<center><h1 style='color:yellow'><small>Udog </small>{player_season[player_season.market=='rushing_yards'].fillna(0).ud_line.median()}</h1></center>",unsafe_allow_html=True)
    # with col2:
    #     st.markdown(f"<center><h1 style='color:purple'><small>Ppicks </small>{player_season[player_season.market=='rushing_yards'].fillna(0).pp_line.median()}</h1></center>",unsafe_allow_html=True)

    # Values to display
    ud_line_median = player_season[player_season.market == 'rushing_yards'].fillna(0).ud_line.median()
    pp_line_median = player_season[player_season.market == 'rushing_yards'].fillna(0).pp_line.median()

    # Display values in one line with different colors
    html_string = f"""
    <div style="display: flex; justify-content: center; align-items: center;">
        <div style="text-align: center; margin-right: 20px;">
            <h1 style='color: yellow;'>{ud_line_median}</h1>
        </div>
        <div style="text-align: center;">
            <h1 style='color: purple;'>{pp_line_median}</h1>
        </div>
    </div>
    """
    # Render in Streamlit
    st.markdown(html_string, unsafe_allow_html=True)

    ######################
    ## VERTICAL SCATTER & SKINNY TABLE WITH BORDER
    config = {'displayModeBar': False}

    # with st.container(border=True):
    col1,col2 = st.columns([1.5,1])
    with col1:
        st.plotly_chart(get_player_scatter_vertical_rush(player_season), config = config, theme=None,use_container_width=True)
    with col2:
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.dataframe(get_rush_table_wide(player_season),hide_index=True, height=475,column_config={'week':'Week','rushing_yards': 'Rush Yards', 'carries':'Carries'},use_container_width=True)

with tab3:
    player_list = list(all_data[all_data.market=='passing_yards'].player.sort_values().unique())
    player = st.selectbox(" ", player_list)
    player_season = all_data[all_data.player==player].reset_index(drop=True)

    ######################
    # PRIZE PICKS AND UNDERDOG LINES
    # with st.container():
    # col1,col2 = st.columns(2)
    # with col1:
    #     st.markdown(f"<center><h1 style='color:yellow'><small>Udog </small>{player_season[player_season.market=='passing_yards'].fillna(0).ud_line.median()}</h1></center>",unsafe_allow_html=True)
    # with col2:
    #     st.markdown(f"<center><h1 style='color:purple'><small>Ppicks </small>{player_season[player_season.market=='passing_yards'].fillna(0).pp_line.median()}</h1></center>",unsafe_allow_html=True)

   # Values to display
    ud_line_median = player_season[player_season.market == 'passing_yards'].fillna(0).ud_line.median()
    pp_line_median = player_season[player_season.market == 'passing_yards'].fillna(0).pp_line.median()

    # Display values in one line with different colors
    html_string = f"""
    <div style="display: flex; justify-content: center; align-items: center;">
        <div style="text-align: center; margin-right: 20px;">
            <h1 style='color: yellow;'><small>Udog </small>{ud_line_median}</h1>
        </div>
        <div style="text-align: center;">
            <h1 style='color: purple;'><small>Ppicks </small>{pp_line_median}</h1>
        </div>
    </div>
    """
    # Render in Streamlit
    st.markdown(html_string, unsafe_allow_html=True)

    ######################
    ## VERTICAL SCATTER & SKINNY TABLE WITH BORDER
    config = {'displayModeBar': False}

    # with st.container(border=True):
    col1,col2 = st.columns([1.18,1])
    with col1:
        st.plotly_chart(get_player_scatter_vertical_pass(player_season), config = config, theme=None,use_container_width=True)
    with col2:
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.dataframe(get_pass_table_wide(player_season),hide_index=True, height=475,column_config={'week':'Week','passing_yards': 'Yards', 'attempts':'Att','passing_tds':'TD'},use_container_width=True)


# ---- REMOVE UNWANTED STREAMLIT STYLING ----
hide_st_style = """
            <style>
            Main Menu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
            
st.markdown(hide_st_style, unsafe_allow_html=True)