
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
    layout="centered",
    initial_sidebar_state="expanded"
)

#######################
# READ IN DATA
def get_data():
    all_data = pd.read_csv(r'C:\Users\mikej\Desktop\mean-median\data\mean_median.csv')
    # all_data = all_data.astype({'season': int})
    return all_data
all_data = get_data()

st.markdown('<h5><center>mean-median',unsafe_allow_html=True)

#####################
## START TABS
tab1, tab2, tab3 = st.tabs(["Receiving", "Rushing", "Passing"])

with tab1:
    # Create the list of players and initialize the player season data
    player_list = list(all_data[all_data.market == 'receiving_yards'].player.sort_values().unique())
    player_season = all_data[all_data.player == player_list[0]].reset_index(drop=True)  # Initial player selection

    # display player name, game info, and lines above scatter plot
    lines_placeholder = st.empty()

    # dicplay scatter plot
    scatter_placeholder = st.empty()

    # Centered selectbox with reduced width
    center_col1, selectbox_col, center_col2 = st.columns([1,6,1])  # Adjust widths as needed

    with selectbox_col:
        # Make selectbox and update player
        player = st.selectbox("Select Player", player_list, key='tab1_select', label_visibility='collapsed')
        player_season = all_data[all_data.player == player].reset_index(drop=True)

        lines_placeholder.markdown(
            f"<div <span style='color: white; font-size: 24px; text-align: center;'>{player_season.player[0]}</span></div>"
            f"<div style='display: flex; justify-content: space-between; color: yellow; font-size: 18px;font-weight: bold;'>"
            f"<span style='color: yellow;text-align: right;'>uDog {player_season[player_season.market == 'receiving_yards'].fillna(0).ud_line.max()}</span>"
            f"<span style='color: white;text-align: right;'>bRiv {player_season[player_season.market == 'receiving_yards'].fillna(0).br_line.max()}</span>"
            f"<span style='color: violet;text-align: left;'>pPicks {player_season[player_season.market == 'receiving_yards'].fillna(0).pp_line.max()}</span>"
            f"</div>",
            unsafe_allow_html=True
        )

        scatter_placeholder.plotly_chart(get_player_scatter_vertical(player_season), config={'displayModeBar': False}, theme=None, use_container_width=True)

        '###'
        st.markdown('<center>Game Log</center>', unsafe_allow_html=True)
        
        # Get the styled DataFrame
        styled_table = get_rec_table_wide(player_season)

        # Get the actual number of rows in the DataFrame
        num_rows = len(player_season[player_season.market == 'receiving_yards'])
        
        # Dynamically adjust height: 35px per row, capped at 475px
        dynamic_height = min(43 * num_rows, 475)

        # Display the DataFrame in Streamlit
        st.dataframe(
            styled_table,
            hide_index=True,
            height=dynamic_height,
            column_config={
                'Week': {'alignment': 'left', 'header': 'Week'},
                'Yards': {'alignment': 'left', 'header': 'Yards'},
                'Attempts': {'alignment': 'left', 'header': 'Attempts'}
            },
            use_container_width=True
        )

        
with tab2:
    # Create the list of players and initialize the player season data
    player_list = list(all_data[all_data.market == 'rushing_yards'].player.sort_values().unique())
    player_season = all_data[all_data.player == player_list[0]].reset_index(drop=True)  # Initial player selection

        # display player name, game info, and lines above scatter plot
    lines_placeholder = st.empty()

    # dicplay scatter plot
    scatter_placeholder = st.empty()

    # Centered selectbox with reduced width
    center_col1, selectbox_col, center_col2 = st.columns([1,6,1])  # Adjust widths as needed

    with selectbox_col:
        # Make selectbox and update player
        player = st.selectbox("Select Player", player_list, key='tab2_select', label_visibility='collapsed')
        player_season = all_data[all_data.player == player].reset_index(drop=True)

        # Display underdog and prizepicks lines
        lines_placeholder.markdown(
            f"<div <span style='color: white; font-size: 24px; text-align: center;'>{player_season.player[0]}</span></div>"
            f"<div style='display: flex; justify-content: space-between; color: yellow; font-size: 18px;font-weight: bold;'>"
            f"<span style='color: yellow;text-align: right;'>uDog {player_season[player_season.market == 'rushing_yards'].fillna(0).ud_line.max()}</span>"
            f"<span style='color: white;text-align: right;'>bRiv {player_season[player_season.market == 'rushing_yards'].fillna(0).br_line.max()}</span>"
            f"<span style='color: violet;text-align: left;'>pPicks {player_season[player_season.market == 'rushing_yards'].fillna(0).pp_line.max()}</span>"
            f"</div>",
            unsafe_allow_html=True
        )

        scatter_placeholder.plotly_chart(get_player_scatter_vertical_rush(player_season), config={'displayModeBar': False}, theme=None, use_container_width=True)

        '###'
        st.markdown('<center>Game Log</center>', unsafe_allow_html=True)
        
        # Get the styled DataFrame
        styled_table = get_rush_table_wide(player_season)

        # Get the actual number of rows in the DataFrame
        num_rows = len(player_season[player_season.market == 'rushing_yards'])
        
        # Dynamically adjust height: 35px per row, capped at 475px
        dynamic_height = min(43 * num_rows, 475)

        # Display the DataFrame in Streamlit
        st.dataframe(
            styled_table,
            hide_index=True,
            height=dynamic_height,
            column_config={
                'Week': {'alignment': 'left', 'header': 'Week'},
                'Yards': {'alignment': 'left', 'header': 'Yards'},
                'Attempts': {'alignment': 'left', 'header': 'Attempts'}
            },
            use_container_width=True
        )
     
with tab3:
    # Create the list of players and initialize the player season data
    player_list = list(all_data[all_data.market == 'passing_yards'].player.sort_values().unique())
    player_season = all_data[all_data.player == player_list[0]].reset_index(drop=True)  # Initial player selection

    # display player name, game info, and lines above scatter plot
    lines_placeholder = st.empty()

    # dicplay scatter plot
    scatter_placeholder = st.empty()

    # Centered selectbox with reduced width
    center_col1, selectbox_col, center_col2 = st.columns([1,6,1])  # Adjust widths as needed

    with selectbox_col:
        # Make selectbox and update player
        player = st.selectbox("Select Player", player_list, key='tab3_select', label_visibility='collapsed')
        player_season = all_data[all_data.player == player].reset_index(drop=True)

        # Display underdog and prizepicks lines
        lines_placeholder.markdown(
            f"<div <span style='color: white; font-size: 24px; text-align: center;'>{player_season.player[0]}</span></div>"
            f"<div style='display: flex; justify-content: space-between; color: yellow; font-size: 18px;font-weight: bold;'>"
            f"<span style='color: yellow;text-align: right;'>uDog {player_season[player_season.market == 'passing_yards'].fillna(0).ud_line.max()}</span>"
            f"<span style='color: white;text-align: right;'>bRiv {player_season[player_season.market == 'passing_yards'].fillna(0).br_line.max()}</span>"
            f"<span style='color: violet;text-align: left;'>pPicks {player_season[player_season.market == 'passing_yards'].fillna(0).pp_line.max()}</span>"
            f"</div>",
            unsafe_allow_html=True
        )

        scatter_placeholder.plotly_chart(get_player_scatter_vertical_pass(player_season), config={'displayModeBar': False}, theme=None, use_container_width=True)

        '###'
        st.markdown('<center>Game Log</center>', unsafe_allow_html=True)
        
        # Get the styled DataFrame
        styled_table = get_pass_table_wide(player_season)

        # Get the actual number of rows in the DataFrame
        num_rows = len(player_season[player_season.market == 'passing_yards'])
        
        # Dynamically adjust height: 35px per row, capped at 475px
        dynamic_height = min(43 * num_rows, 475)

        # Display the DataFrame in Streamlit
        st.dataframe(
            styled_table,
            hide_index=True,
            height=dynamic_height,
            column_config={
                'Week': {'alignment': 'left', 'header': 'Week'},
                'Yards': {'alignment': 'left', 'header': 'Yards'},
                'Attempts': {'alignment': 'left', 'header': 'Attempts'}
            },
            use_container_width=True
        )



# ---- REMOVE UNWANTED STREAMLIT STYLING ----
hide_st_style = """
            <style>
            Main Menu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
            
st.markdown(hide_st_style, unsafe_allow_html=True)

st.markdown(
    """
    <style>
    .stApp {
        footer {display: none;}
    }
    </style>
    """,
    unsafe_allow_html=True
)