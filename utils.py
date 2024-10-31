
import pandas as pd
import plotly.express as px
import seaborn as sns
import plotly.graph_objects as go
import streamlit as st
# from plotly.subplots import make_subplots


def merge_books(pp,ud):
    pp = pp[['Player','Position','Team','Opponent','Market Name','Line']].rename(columns={'Line':'pp_line'})
    ud = ud[['Player','Position','Team','Opponent','Market Name','Line']].rename(columns={'Line':'ud_line'})
    merged = pd.merge(pp,ud,on=['Player','Position', 'Team', 'Opponent','Market Name'],how='outer')
    merged.columns = ['player_display_name','position','team','opponent','market','pp_line','ud_line']
    merged.to_csv('data/books_merged.csv', index=False)
    return merged

# --- add 'delta' column
def pp_delta(row):
    if row['market'] == 'receiving_yards':
        return row['receiving_yards'] - row['pp_line']
    elif row['market'] == 'rushing_yards':
        return row['rushing_yards'] - row['pp_line']
    else:
        return row['passing_yards'] - row['pp_line']
    
def ud_delta(row):
    if row['market'] == 'receiving_yards':
        return row['receiving_yards'] - row['ud_line']
    elif row['market'] == 'rushing_yards':
        return row['rushing_yards'] - row['ud_line']
    else:
        return row['passing_yards'] - row['ud_line']

def get_rec_table_wide(player_season):

    rec_table_wide = player_season[player_season.market=='receiving_yards'][['week','receiving_yards','targets','receptions','receiving_tds']].sort_values(by='week',ascending=False).reset_index(drop=True) 
    rec_table_wide.columns = ['Week','Yards','Targets','Rec','TDs']

    ud_line = player_season[player_season.market=='receiving_yards'].ud_line.median()
    pp_line = player_season[player_season.market=='receiving_yards'].pp_line.median()

    # Define a function to highlight rows where 'receiving_yards' is greater than either ud_line or pp_line
    def highlight_high_yards(row):
        color = 'background-color: #65b1d7' if row['Yards'] > ud_line or row['Yards'] > pp_line else ''
        return [color] * len(row)
    
    # Apply the highlighting function and set font properties
    rec_table_wide = (rec_table_wide.style
                      .apply(highlight_high_yards, axis=1)
                      .format(precision=0))
    
    return rec_table_wide


def get_rush_table_wide(player_season):
    rush_table_wide = player_season[player_season.market=='rushing_yards'][['week','rushing_yards','carries']].sort_values(by='week',ascending=False).reset_index(drop=True)
    rush_table_wide.columns = ['Week','Yards','Carries']

    ud_line = player_season[player_season.market=='rushing_yards'].ud_line.median()
    pp_line = player_season[player_season.market=='rushing_yards'].pp_line.median()

    # Define a function to highlight rows where 'receiving_yards' is greater than either ud_line or pp_line
    def highlight_high_yards(row):
        color = 'background-color: #65b1d7' if row['Yards'] > ud_line or row['Yards'] > pp_line else ''
        return [color] * len(row)
    
    # Apply the highlighting function and set font properties
    rush_table_wide = (rush_table_wide.style
                      .apply(highlight_high_yards, axis=1)
                      .format(precision=0))
    
    return rush_table_wide

def get_pass_table_wide(player_season):
    pass_table_wide = player_season[player_season.market=='passing_yards'][['week','passing_yards','attempts','passing_tds']].sort_values(by='week',ascending=False).reset_index(drop=True) 
    pass_table_wide.columns = ['Week','Yards','Attempts','TDs']

    ud_line = player_season[player_season.market=='passing_yards'].ud_line.median()
    pp_line = player_season[player_season.market=='passing_yards'].pp_line.median()

    # function to hightlight weeks beating line
    def highlight_high_yards(row):
        color = 'background-color: #65b1d7' if row['Yards'] > ud_line or row['Yards'] > pp_line else ''
        return [color] * len(row)
    
    # Apply the highlighting function and set font properties
    pass_table_wide = (pass_table_wide.style
                      .apply(highlight_high_yards, axis=1)
                      .format(precision=0))
    
    return pass_table_wide


def get_player_scatter_vertical(player_season):
    # Create a new column for custom hover text
    player_season['hover_text'] = player_season.apply(
        lambda row: f"Week {int(row['week'])}<br>vs. {row['opponent_team']}<br><br>{int(row['receiving_yards'])} yards<br>{int(row['targets'])} targets", axis=1
        )
    
    player_scatter_vertical = px.scatter(player_season,x='targets',y='receiving_yards',
                        size='week',color='week',template='presentation',
                        size_max=17, height=550, #width=500
                        color_continuous_scale='blues',
                        # title = f"<b>{player_season.player[0]}<br><span style='color:yellow'>{player_season[player_season.market == 'receiving_yards'].fillna(0).ud_line.median()}</span> <span style='color:orchid'><b>{player_season[player_season.market == 'receiving_yards'].fillna(0).pp_line.median()}</span>",
                        labels={'receiving_yards':'Receiving Yards','targets':'Targets'}).update_coloraxes(showscale=False)
    player_scatter_vertical.add_hline(y=player_season[player_season['market']=='receiving_yards'].ud_line.max(), line_width=1, line_color="yellow")
    player_scatter_vertical.add_hline(y=player_season[player_season['market']=='receiving_yards'].pp_line.max(), line_width=1, line_color="purple")
    player_scatter_vertical.add_hline(y=player_season[player_season['market']=='receiving_yards'].receiving_yards.median(), line_width=2, line_color="white", line_dash="dot")
    player_scatter_vertical.update_yaxes(showgrid=True, gridcolor='grey')
    player_scatter_vertical.update_layout(title_y=.9)
    player_scatter_vertical.update_traces(textfont_family='Arial Black', hovertemplate=player_season['hover_text'])

    return player_scatter_vertical

def get_player_scatter_vertical_rush(player_season):
    # Create a new column for custom hover text
    player_season['hover_text'] = player_season.apply(
        lambda row: f"Week {int(row['week'])}<br>vs. {row['opponent_team']}<br><br>{int(row['rushing_yards'])} yards<br>{int(row['carries'])} carries", axis=1
        )
    
    player_scatter_vertical = px.scatter(player_season,x='carries',y='rushing_yards',
                        size='week',color='week',template='presentation',
                        size_max=17, height=550, #width=500
                        color_continuous_scale='blues',
                        title = f"<b>{player_season.player[0]}<br><span style='color:yellow'>{player_season[player_season.market == 'rushing_yards'].fillna(0).ud_line.median()}</span> <span style='color:orchid'><b>{player_season[player_season.market == 'rushing_yards'].fillna(0).pp_line.median()}</span><br>",
                        labels={'rushing_yards':'Rush Yards','carries':'Carries'}).update_coloraxes(showscale=False)
    player_scatter_vertical.add_hline(y=player_season[player_season['market']=='rushing_yards'].fillna(0).ud_line.median(), line_width=1, line_color="yellow")
    player_scatter_vertical.add_hline(y=player_season[player_season['market']=='rushing_yards'].fillna(0).pp_line.median(), line_width=1, line_color="purple")
    player_scatter_vertical.add_hline(y=player_season[player_season['market']=='rushing_yards'].fillna(0).rushing_yards.median(), line_width=2, line_color="white", line_dash="dot")
    player_scatter_vertical.update_yaxes(showgrid=True, gridcolor='grey')
    player_scatter_vertical.update_layout(title_y=.9)
    player_scatter_vertical.update_traces(textfont_family='Arial Black', hovertemplate=player_season['hover_text'])

    return player_scatter_vertical

def get_player_scatter_vertical_pass(player_season):
    # Create a new column for custom hover text
    player_season['hover_text'] = player_season.apply(
        lambda row: f"Week {int(row['week'])}<br>vs. {row['opponent_team']}<br><br>{int(row['passing_yards'])} yards<br>{int(row['attempts'])} attempts", axis=1
        )
    player_scatter_vertical = px.scatter(player_season,x='attempts',y='passing_yards',
                        size='week',color='week',template='presentation',
                        size_max=17, height=550, #width=500
                        color_continuous_scale='blues',
                        title = f"<b>{player_season.player[0]}<br><span style='color:yellow'>{player_season[player_season.market == 'passing_yards'].fillna(0).ud_line.median()}</span> <span style='color:orchid'><b>{player_season[player_season.market == 'passing_yards'].fillna(0).pp_line.median()}</span><br>",
                        labels={'passing_yards':'Pass Yards','attempts':'Attempts'}).update_coloraxes(showscale=False)
    player_scatter_vertical.add_hline(y=player_season[player_season['market']=='passing_yards'].ud_line.mean(), line_width=1, line_color="yellow")
    player_scatter_vertical.add_hline(y=player_season[player_season['market']=='passing_yards'].pp_line.mean(), line_width=1, line_color="lavender")
    player_scatter_vertical.add_hline(y=player_season[player_season['market']=='passing_yards'].passing_yards.median(), line_width=2, line_color="white", line_dash="dot")
    player_scatter_vertical.update_yaxes(showgrid=True, gridcolor='grey')
    player_scatter_vertical.update_layout(title_y=.9)
    player_scatter_vertical.update_traces(textfont_family='Arial Black', hovertemplate=player_season['hover_text'])
    return player_scatter_vertical
