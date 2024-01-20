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
from utils import get_rec_table_skinny, get_rec_table_skinny2, get_rec_table_wide, get_player_scatter_vertical, get_player_scatter_horizontal

#######################
# Page configuration
st.set_page_config(
    page_title="mean-median",
    page_icon="🏂",
    # layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

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

# [data-testid="stVerticalBlock"] {
#     padding-left: 0rem;
#     padding-right: 0rem;
# }

# [data-testid="stMetric"] {
#     background-color: #393939;
#     text-align: center;
#     padding: 15px 0;
# }

# [data-testid="stMetricLabel"] {
#   display: flex;
#   justify-content: center;
#   align-items: center;
# }

# [data-testid="stMetricDeltaIcon-Up"] {
#     position: relative;
#     left: 38%;
#     -webkit-transform: translateX(-50%);
#     -ms-transform: translateX(-50%);
#     transform: translateX(-50%);
# }

# [data-testid="stMetricDeltaIcon-Down"] {
#     position: relative;
#     left: 38%;
#     -webkit-transform: translateX(-50%);
#     -ms-transform: translateX(-50%);
#     transform: translateX(-50%);
# }

</style>
""", unsafe_allow_html=True)


#######################
all_data = pd.read_csv(r"data/final_data.csv")
all_data = all_data.astype({'season': int})


#######################
# Sidebar
# with st.sidebar:
#     st.caption("Underdog")

#     med_rec = int(player_season[player_season.book_stat == 'receiving_yards']['receiving_yards'].median())
#     med_rush = int(player_season[player_season.book_stat == 'rushing_yards']['rushing_yards'].median())

#     st.metric(label=f"Receiving Yards", 
#               value=f"{(player_all[player_all['book_stat']=='receiving_yards'].ud_line.mean())}", 
#               delta= med_rec)
#     st.metric(label="Rushing Yards", 
#               value=f"{player_all[player_all['book_stat']=='rushing_yards'].ud_line.mean()}", 
#               delta= med_rush)
#     st.markdown("---")
#     st.caption('Prize Picks')
#     st.metric(label=f"Receiving Yards", 
#               value=f"{player_all[player_all['book_stat']=='receiving_yards'].pp_line.mean()}", 
#               delta= med_rec)
#     st.metric(label="Rushing Yards", 
#               value=f"{player_all[player_all['book_stat']=='rushing_yards'].pp_line.mean()}", 
#               delta= med_rush)


player_list = list(all_data.player_display_name.unique())#[::-1]
player = st.selectbox("", player_list)
player_all = all_data[(all_data.player_display_name==player)].reset_index(drop=True)

#####################
#  TITLE
# st.markdown(f"<center><h1>{player_all.player_display_name[0]}</h1></center>", unsafe_allow_html=True)   

player_season = player_all[player_all.season==2023].reset_index(drop=True)
player_season2 = player_all[player_all.season > 2021].reset_index(drop=True)


######################
# PRIZE PICKS AND UNDERDOG LINES
# with st.container():
#     col1,col2 = st.columns([2,1])
#     with col1:
#         st.markdown(f"<center><h1 style='color:yellow'><small>ud</small>{player_season[player_season.book_stat=='receiving_yards'].ud_line.mean()}</h1></center>",unsafe_allow_html=True)
#     with col2:
#         st.markdown(f"<center><h1 style='color:purple'><small>pp</small>{player_season[player_season.book_stat=='receiving_yards'].pp_line.mean()}</h1></center>",unsafe_allow_html=True)

    
#######################
# VERTICAL SCATTER & SKINNY TABLE WITH BORDER
# col = st.columns([2,1])
skinny_scatter = get_player_scatter_vertical(player_season)
skinny_table = get_rec_table_skinny2(player_season)
config = {'displayModeBar': False}

with st.container(border=True):
    col1,col2 = st.columns([2,1])
    with col1:
        st.plotly_chart(skinny_scatter, config = config, theme=None,use_container_width=True)
    with col2:
        # st.dataframe(get_rec_table_skinny(player_season),
        #              hide_index=True, 
        #              height=600,
        #              column_config={'week':'Week','receiving_yards':'Rec Yards'},
        #              use_container_width=True)
        st.plotly_chart(skinny_table,
                        hide_index=True, 
                        height=600,
                        column_config={'week':'Week','receiving_yards':'Rec Yards'},
                        use_container_width=True)


######################
# WIDE TABLE
st.markdown("")
st.dataframe(get_rec_table_wide(player_season),hide_index=True, width=400, height=700, column_config={'week':'Week','targets':'Targets','receptions':'Receptions','receiving_tds':'Receiving TDs','fantasy_points':'Fantasy Points'},use_container_width=True)