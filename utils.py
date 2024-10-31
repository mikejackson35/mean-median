
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
        color = 'background-color: #3892F1' if row['Yards'] > ud_line or row['Yards'] > pp_line else ''
        return [color] * len(row)
    
    # Apply the highlighting function and set font properties
    rec_table_wide = (rec_table_wide.style
                      .apply(highlight_high_yards, axis=1)
                      .format(precision=0))
    
    return rec_table_wide

def get_rush_table_wide(player_season):
    # Create a DataFrame for rushing yards data, sorting by week
    rush_table_wide = player_season[player_season.market == 'rushing_yards'][['week', 'opponent_team', 'rushing_yards', 'carries']].sort_values(by='week', ascending=False).reset_index(drop=True)
    rush_table_wide.columns = ['Week', 'Opp', 'Yards', 'Carries']

    # Calculate the median lines for UD and PP
    ud_line = player_season[player_season.market == 'rushing_yards'].ud_line.median()
    pp_line = player_season[player_season.market == 'rushing_yards'].pp_line.median()

    # Define a function to highlight rows where 'Yards' is greater than either ud_line or pp_line
    def highlight_high_yards(row):
        color = 'background-color: #3892F1' if row['Yards'] > ud_line or row['Yards'] > pp_line else ''
        return [color] * len(row)

    # Apply the highlighting function and format the DataFrame
    rush_table_wide = (rush_table_wide.style
                       .apply(highlight_high_yards, axis=1)
                       .format(precision=0))

    return rush_table_wide

def get_pass_table_wide(player_season):
    pass_table_wide = player_season[player_season.market == 'passing_yards'][['week', 'passing_yards', 'attempts', 'passing_tds']].sort_values(by='week', ascending=False).reset_index(drop=True)
    pass_table_wide.columns = ['Week', 'Yards', 'Attempts', 'TDs']

    ud_line = player_season[player_season.market == 'passing_yards'].ud_line.median()
    pp_line = player_season[player_season.market == 'passing_yards'].pp_line.median()

    # Define a function to highlight rows where 'passing_yards' is greater than either ud_line or pp_line
    def highlight_high_yards(row):
        color = 'background-color: #3892F1' if row['Yards'] > ud_line or row['Yards'] > pp_line else ''
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
    
    # Calculate the maximum values for UD Line and PP Line
    ud_line_max = player_season[player_season['market'] == 'receiving_yards'].ud_line.max()
    pp_line_max = player_season[player_season['market'] == 'receiving_yards'].pp_line.max()
    br_line_max = player_season[player_season['market'] == 'receiving_yards'].br_line.max()

    # Create the scatter plot for rushing yards
    player_scatter_vertical = px.scatter(
        player_season,
        x='targets',
        y='receiving_yards',
        size='week',
        color='week',
        template='presentation',
        size_max=17,
        height=500,
        color_continuous_scale='blues',
        labels={'receiving_yards': 'Rec Yards', 'targets': 'Targets'}
    ).update_coloraxes(showscale=False)

    # Add horizontal lines only if the values are greater than zero
    if ud_line_max > 0:
        player_scatter_vertical.add_hline(y=ud_line_max, line_width=1, line_color="yellow")
    
    if pp_line_max > 0:
        player_scatter_vertical.add_hline(y=pp_line_max, line_width=1, line_color="purple")

    # if br_line_max > 0:
    #     player_scatter_vertical.add_hline(y=br_line_max, line_width=1, line_color="#17B169")
    
    # Median line and annotation
    max_value = player_season[player_season['market'] == 'receiving_yards'].receiving_yards.max()
    median_value = player_season[player_season['market'] == 'receiving_yards'].receiving_yards.median()
    targets_min = player_season[player_season['market'] == 'receiving_yards'].targets.min()
    br_line = player_season[player_season.market == 'receiving_yards'].fillna(0).br_line.median()
    player_scatter_vertical.add_hline(y=median_value, line_width=3, line_color="#3892F1", line_dash="dot")

    # Gather game information for the title
    spread_display = f"+{player_season.spread[0]}" if player_season.spread[0] >= 0 else str(player_season.spread[0])
    opponent = player_season.opponent_team[0]
    over_under = player_season.over_under[0]

    # Update chart title with game information
    player_scatter_vertical.update_layout(
        # f"<span style='color: white;text-align: center;'>bRiv {player_season[player_season.market == 'receiving_yards'].fillna(0).br_line).median()}</span>"
        title=f"<b>bRiv {br_line}<br><br>{spread_display} v. {opponent} &nbsp;&nbsp;&nbsp; o/u {over_under}<br><span style='color: #3892F1;text-align: right;'>Szn Median: {median_value} yards</span>",
        title_x=0.5, title_y=.96,  # Center the title
        title_font=dict(size=14, color='white')  # Adjust title font style
    )

        # Add annotation for the median line
    player_scatter_vertical.add_annotation(
        x=targets_min + .1,  # Positioning on the x-axis (far left)
        y=max_value - 1,  # Slightly above the line
        text=f'<b>bRiv<br>{br_line}',  # Value to display
        showarrow=False,  # No arrow
        font=dict(size=15, color='white'),  # Font size and color
        align='center'  # Center the text
    )

    # Update layout and axes
    player_scatter_vertical.update_traces(hovertemplate=player_season['hover_text'])

    return player_scatter_vertical

def get_player_scatter_vertical_rush(player_season):
    # Create a new column for custom hover text
    player_season['hover_text'] = player_season.apply(
        lambda row: f"Week {int(row['week'])}<br>vs. {row['opponent_team']}<br><br>{int(row['rushing_yards'])} yards<br>{int(row['carries'])} carries", axis=1
    )
    
    # Calculate the maximum values for UD Line and PP Line
    ud_line_max = player_season[player_season['market'] == 'rushing_yards'].ud_line.max()
    pp_line_max = player_season[player_season['market'] == 'rushing_yards'].pp_line.max()
    br_line_max = player_season[player_season['market'] == 'rushing_yards'].br_line.max()

    # Create the scatter plot for rushing yards
    player_scatter_vertical = px.scatter(
        player_season,
        x='carries',
        y='rushing_yards',
        size='week',
        color='week',
        template='presentation',
        size_max=17,
        height=500,
        color_continuous_scale='blues',
        labels={'rushing_yards': 'Rush Yards', 'carries': 'Carries'}
    ).update_coloraxes(showscale=False)

    # Add horizontal lines only if the values are greater than zero
    if ud_line_max > 0:
        player_scatter_vertical.add_hline(y=ud_line_max, line_width=1, line_color="yellow")
    
    if pp_line_max > 0:
        player_scatter_vertical.add_hline(y=pp_line_max, line_width=1, line_color="purple")
    
    # if br_line_max > 0:
    #     player_scatter_vertical.add_hline(y=br_line_max, line_width=1, line_color="#17B169")    

    # Median line and annotation
    max_value = player_season[player_season['market'] == 'rushing_yards'].rushing_yards.max()
    median_value = player_season[player_season['market'] == 'rushing_yards'].rushing_yards.median()
    carries_min = player_season[player_season['market'] == 'rushing_yards'].carries.min()
    br_line = player_season[player_season.market == 'rushing_yards'].fillna(0).br_line.median()
    player_scatter_vertical.add_hline(y=median_value, line_width=3, line_color="#3892F1", line_dash="dot")

    # Gather game information for the title
    spread_display = f"+{player_season.spread[0]}" if player_season.spread[0] >= 0 else str(player_season.spread[0])
    opponent = player_season.opponent_team[0]
    over_under = player_season.over_under[0]

    player_scatter_vertical.update_layout(
        title=f"<b>bRiv {br_line}<br><br>{spread_display} v. {opponent} &nbsp;&nbsp;&nbsp; o/u {over_under}<br><span style='color: #3892F1;text-align: right;'>Szn Median: {median_value} yards</span>",
        title_x=0.5, title_y=.96,  # Center the title
        title_font=dict(size=14, color='white')  # Adjust title font style
        )

            # Add annotation for the median line
    player_scatter_vertical.add_annotation(
        x=carries_min + .1,  # Positioning on the x-axis (far left)
        y=max_value - 1,  # Slightly above the line
        text=f'<b>bRiv<br>{br_line}',  # Value to display
        showarrow=False,  # No arrow
        font=dict(size=15, color='white'),  # Font size and color
        align='center'  # Center the text
    )

    # Update layout and axes
    player_scatter_vertical.update_traces(hovertemplate=player_season['hover_text'])

    return player_scatter_vertical


def get_player_scatter_vertical_pass(player_season):
    # Create a new column for custom hover text
    player_season['hover_text'] = player_season.apply(
        lambda row: f"Week {int(row['week'])}<br>vs. {row['opponent_team']}<br><br>{int(row['passing_yards'])} yards<br>{int(row['attempts'])} attempts", axis=1
    )
    
    # Calculate the maximum values for UD Line and PP Line
    ud_line_max = player_season[player_season['market'] == 'passing_yards'].ud_line.max()
    pp_line_max = player_season[player_season['market'] == 'passing_yards'].pp_line.max()

    # Create the scatter plot for rushing yards
    player_scatter_vertical = px.scatter(
        player_season,
        x='attempts',
        y='passing_yards',
        size='week',
        color='week',
        template='presentation',
        size_max=17,
        height=500,
        color_continuous_scale='blues',
        labels={'passing_yards': 'Pass Yards', 'attempts': 'Attempts'}
    ).update_coloraxes(showscale=False)

    # Add horizontal lines only if the values are greater than zero
    if ud_line_max > 0:
        player_scatter_vertical.add_hline(y=ud_line_max, line_width=1, line_color="yellow")
    
    if pp_line_max > 0:
        player_scatter_vertical.add_hline(y=pp_line_max, line_width=1, line_color="purple")
    
    # Median line and annotation
    max_value = player_season[player_season['market'] == 'passing_yards'].passing_yards.max()
    attempts_min = player_season[player_season['market'] == 'passing_yards'].attempts.min()
    br_line = player_season[player_season.market == 'passing_yards'].fillna(0).br_line.median()
    median_value = player_season[player_season['market'] == 'passing_yards'].passing_yards.median()
    player_scatter_vertical.add_hline(y=median_value, line_width=3, line_color="#3892F1", line_dash="dot")

    # Gather game information for the title
    spread_display = f"+{player_season.spread[0]}" if player_season.spread[0] >= 0 else str(player_season.spread[0])
    opponent = player_season.opponent_team[0]
    over_under = player_season.over_under[0]

    player_scatter_vertical.update_layout(# f"<span style='color: white;text-align: center;'>bRiv {player_season[player_season.market == 'receiving_yards'].fillna(0).br_line).median()}</span>"
        title=f"<b>bRiv {br_line}<br><br>{spread_display} v. {opponent} &nbsp;&nbsp;&nbsp; o/u {over_under}<br><span style='color: #3892F1;text-align: right;'>Szn Median: {median_value} yards</span>",
        title_x=0.5, title_y=.96,  # Center the title
        title_font=dict(size=14, color='white')  # Adjust title font style
    )

                # Add annotation for the median line
    player_scatter_vertical.add_annotation(
        x=attempts_min + .1,  # Positioning on the x-axis (far left)
        y=max_value - 1,  # Slightly above the line
        text=f'<b>bRiv<br>{br_line}',  # Value to display
        showarrow=False,  # No arrow
        font=dict(size=15, color='white'),  # Font size and color
        align='center'  # Center the text
    )

    # Update layout and axes
    player_scatter_vertical.update_traces(hovertemplate=player_season['hover_text'])

    return player_scatter_vertical