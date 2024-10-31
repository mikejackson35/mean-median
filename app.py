
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

# Create a toggle for PC view
centered_view = st.toggle("mobile/PC", value=False)
st.markdown("<h1 style='text-align: center; font-family:Courier New;'>mean-median</h1>", unsafe_allow_html=True)

#######################
# CSS styling with Toggle


# Apply CSS based on the toggle state
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
                padding-left: 2rem !important;
                padding-right: 2rem !important;
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
                padding-left: 1rem !important;
                padding-right: 1rem !important;
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
    # Create the list of players and initialize the player season data
    player_list = list(all_data[all_data.market == 'receiving_yards'].player.sort_values().unique())
    player_season = all_data[all_data.player == player_list[0]].reset_index(drop=True)  # Initial player selection

    col1, col2 = st.columns([1.35, 1])

    with col1:

        info_col1, info_col2, info_col3 = st.columns([1,1.5,1])

        # lines, player name, and game info
        with info_col1:
            lines_placeholder = st.empty()
        
        with info_col2:
            name_placeholder = st.empty()
            game_placeholder = st.empty()

        with info_col3:
            lines_placeholder2 = st.empty()

        # Display the scatter plot without the title
        scatter_placeholder = st.empty()

        # Centered selectbox with reduced width
        center_col1, selectbox_col, center_col2 = st.columns([1,6,1])  # Adjust widths as needed

        with selectbox_col:
            # make selectbox and update player
            player = st.selectbox("Select Player", player_list, key='tab1_select')
            player_season = all_data[all_data.player == player].reset_index(drop=True)

            # display underdog and prizepicks lines
            lines_placeholder.markdown(f"<div style='text-align: center; color: yellow; font-size: 20px;'>"
                        f"Udog<br>{player_season[player_season.market == 'receiving_yards'].fillna(0).ud_line.median()}<br>",
                        unsafe_allow_html=True)
            
            lines_placeholder2.markdown(f"<div style='text-align: center; color: yellow; font-size: 20px;'>"
                        f"<span style='color: violet;'>Ppick<br>{player_season[player_season.market == 'receiving_yards'].fillna(0).pp_line.median()}</span></div>", 
                        unsafe_allow_html=True)

            #display player name
            name_placeholder.markdown(f"<div style='text-align: center; color: white; font-size: 24px;'>"
                                f"<b>{player_season.player[0]}</b></div>", 
                                unsafe_allow_html=True)  
            
            # Conditional logic to add a '+' symbol if the spread is non-negative
            spread_display = f"+{player_season.spread[0]}" if player_season.spread[0] >= 0 else str(player_season.spread[0])

            # Using <span> to add more space instead of a pipe
            game_placeholder.markdown(f"<div style='text-align: center; color: white; font-size: 16px;'>"
                                    f"<b><small>{spread_display} v. {player_season.opponent_team[0]} <span style='margin-left: 20px;'>o/u</span> {(player_season.over_under[0])}</small></b></div>", 
                                    unsafe_allow_html=True)
                     
            scatter_placeholder.plotly_chart(get_player_scatter_vertical(player_season), config={'displayModeBar': False}, theme=None, use_container_width=True)

    with col2:
        '###'
        '###'
        # '###'
        # '###'
        st.markdown('<center>Game Log</center>', unsafe_allow_html=True)
        st.dataframe(
            get_rec_table_wide(player_season),
            hide_index=True,
            height=475,
            column_config={
                'Week': {'alignment': 'left', 'header': 'Week'},
                'Yards': {'alignment': 'left', 'header': 'Yards'},
                'Targets': {'alignment': 'left', 'header': 'Targets'},
                'Rec': {'alignment': 'left', 'header': 'Rec'},
                'TDs': {'alignment': 'left', 'header': 'TDs'}
            },
            use_container_width=True
        )
        
with tab2:
    # Create the list of players and initialize the player season data
    player_list = list(all_data[all_data.market == 'rushing_yards'].player.sort_values().unique())
    player_season = all_data[all_data.player == player_list[0]].reset_index(drop=True)  # Initial player selection

    col1, col2 = st.columns([1.35, 1])

    with col1:
        info_col1, info_col2 = st.columns(2)

        # Lines, player name, and game info
        with info_col1:
            lines_placeholder = st.empty()

        with info_col2:
            name_placeholder = st.empty()
            game_placeholder = st.empty()

        # Display the scatter plot without the title
        scatter_placeholder = st.empty()

        # Centered selectbox with reduced width
        center_col1, selectbox_col, center_col2 = st.columns([1,6,1])  # Adjust widths as needed

        with selectbox_col:
            # Make selectbox and update player
            player = st.selectbox("Select Player", player_list, key='tab2_select')
            player_season = all_data[all_data.player == player].reset_index(drop=True)

            # Display underdog and prizepicks lines
            lines_placeholder.markdown(f"<div style='text-align: center; color: yellow; font-size: 18px;'>"
                                       f"<span style='color: yellow;'>Udog {player_season[player_season.market == 'rushing_yards'].fillna(0).ud_line.median()}</span>"
                                       f"<br><span style='color: yellow;'></span>"
                                       f"<span style='color: violet;'>Ppick {player_season[player_season.market == 'rushing_yards'].fillna(0).pp_line.median()}</span></div>",
                                       unsafe_allow_html=True)

            # lines_placeholder2.markdown(f"<div style='text-align: center; color: yellow; font-size: 20px;'>"
            #                             f"<span style='color: violet;'>Ppick<br>{player_season[player_season.market == 'rushing_yards'].fillna(0).pp_line.median()}</span></div>",
            #                             unsafe_allow_html=True)

            # Display player name
            name_placeholder.markdown(f"<div style='text-align: center; color: white; font-size: 24px;'>"
                                      f"<b>{player_season.player[0]}</b></div>",
                                      unsafe_allow_html=True)

            # Conditional logic to add a '+' symbol if the spread is non-negative
            spread_display = f"+{player_season.spread[0]}" if player_season.spread[0] >= 0 else str(player_season.spread[0])

            # Using <span> to add more space instead of a pipe
            game_placeholder.markdown(f"<div style='text-align: center; color: white; font-size: 16px;'>"
                                      f"<b><small>{spread_display} v. {player_season.opponent_team[0]} <span style='margin-left: 20px;'>o/u</span> {(player_season.over_under[0])}</small></b></div>",
                                      unsafe_allow_html=True)

            scatter_placeholder.plotly_chart(get_player_scatter_vertical_rush(player_season), config={'displayModeBar': False}, theme=None, use_container_width=True)

    with col2:
        '###'
        '###'
        # '###'
        # '###'
        st.markdown('<center>Game Log</center>', unsafe_allow_html=True)
        st.dataframe(
            get_rush_table_wide(player_season),
            hide_index=True,
            height=475,
            column_config={
                'Week': {'alignment': 'left', 'header': 'Week'},
                'Yards': {'alignment': 'left', 'header': 'Yards'},
                'Carries': {'alignment': 'left', 'header': 'Carries'}
            },
            use_container_width=True
        )
     
# Tab 3: Passing Yards Data
with tab3:
    # Create the list of players and initialize the player season data
    player_list = list(all_data[all_data.market == 'passing_yards'].player.sort_values().unique())
    player_season = all_data[all_data.player == player_list[0]].reset_index(drop=True)  # Initial player selection

    col1, col2 = st.columns([1.35, 1])

    with col1:
        info_col1, info_col2, info_col3 = st.columns([1, 1.5, 1])

        # Lines, player name, and game info
        with info_col1:
            lines_placeholder = st.empty()

        with info_col2:
            name_placeholder = st.empty()
            game_placeholder = st.empty()

        with info_col3:
            lines_placeholder2 = st.empty()

        # Display the scatter plot without the title
        scatter_placeholder = st.empty()

        # Centered selectbox with reduced width
        center_col1, selectbox_col, center_col2 = st.columns([1, 6, 1])  # Adjust widths as needed

        with selectbox_col:
            # Make selectbox and update player
            player = st.selectbox("Select Player", player_list, key='tab3_select')
            player_season = all_data[all_data.player == player].reset_index(drop=True)

            # Display underdog and prizepicks lines
            lines_placeholder.markdown(f"<div style='text-align: center; color: yellow; font-size: 20px;'>"
                                       f"Udog<br>{player_season[player_season.market == 'passing_yards'].fillna(0).ud_line.median()}<br>",
                                       unsafe_allow_html=True)

            lines_placeholder2.markdown(f"<div style='text-align: center; color: yellow; font-size: 20px;'>"
                                        f"<span style='color: violet;'>Ppick<br>{player_season[player_season.market == 'passing_yards'].fillna(0).pp_line.median()}</span></div>",
                                        unsafe_allow_html=True)

            # Display player name
            name_placeholder.markdown(f"<div style='text-align: center; color: white; font-size: 24px;'>"
                                      f"<b>{player_season.player[0]}</b></div>",
                                      unsafe_allow_html=True)

            # Conditional logic to add a '+' symbol if the spread is non-negative
            spread_display = f"+{player_season.spread[0]}" if player_season.spread[0] >= 0 else str(player_season.spread[0])

            # Using <span> to add more space instead of a pipe
            game_placeholder.markdown(f"<div style='text-align: center; color: white; font-size: 16px;'>"
                                      f"<b><small>{spread_display} v. {player_season.opponent_team[0]} <span style='margin-left: 20px;'>o/u</span> {(player_season.over_under[0])}</small></b></div>",
                                      unsafe_allow_html=True)

            scatter_placeholder.plotly_chart(get_player_scatter_vertical_pass(player_season), config={'displayModeBar': False}, theme=None, use_container_width=True)

    with col2:
        '###'
        '###'
        # '###'
        # '###'
        st.markdown('<center>Game Log</center>', unsafe_allow_html=True)
        st.dataframe(
            get_pass_table_wide(player_season),
            hide_index=True,
            height=475,
            column_config={
                'Week': {'alignment': 'left', 'header': 'Week'},
                'Yards': {'alignment': 'left', 'header': 'Yards'},
                'Attempts': {'alignment': 'left', 'header': 'Attempts'},
                'TDs': {'alignment': 'left', 'header': 'TDs'}
            },
            use_container_width=True
        )



# ---- REMOVE UNWANTED STREAMLIT STYLING ----
# hide_st_style = """
#             <style>
#             Main Menu {visibility: hidden;}
#             footer {visibility: hidden;}
#             header {visibility: hidden;}
#             </style>
#             """
            
# st.markdown(hide_st_style, unsafe_allow_html=True)