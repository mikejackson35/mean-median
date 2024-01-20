
import pandas as pd
import plotly.express as px
import seaborn as sns
import plotly.graph_objects as go

def merge_books(pp,ud):
    pp = pp[['Player','Position','Team','Opponent','Market Name','Line']].rename(columns={'Line':'pp_line'})
    ud = ud[['Player','Position','Team','Opponent','Market Name','Line']].rename(columns={'Line':'ud_line'})
    merged = pd.merge(pp,ud,on=['Player','Position', 'Team', 'Opponent','Market Name'],how='outer')
    merged.columns = ['player_display_name','position','team','opponent','book_stat','pp_line','ud_line']
    merged.to_csv('data/books_merged.csv', index=False)
    return merged

# --- add 'delta' column
def pp_delta(row):
    if row['book_stat'] == 'receiving_yards':
        return row['receiving_yards'] - row['pp_line']
    elif row['book_stat'] == 'rushing_yards':
        return row['rushing_yards'] - row['pp_line']
    else:
        return row['passing_yards'] - row['pp_line']
    
def ud_delta(row):
    if row['book_stat'] == 'receiving_yards':
        return row['receiving_yards'] - row['ud_line']
    elif row['book_stat'] == 'rushing_yards':
        return row['rushing_yards'] - row['ud_line']
    else:
        return row['passing_yards'] - row['ud_line']
    
# def player_selected(player_selected):
#      player = nfl[(nfl.player_display_name==player_selected) & (nfl.season==2023)].reset_index(drop=True)
#      return player

# )

# def get_rec_table_wide(player):
#     player_df = all_data[(all_data.player_display_name==player) & (all_data.season==2023)].reset_index(drop=True) 
#     rec_table_wide = player_df[['week','targets','receptions','receiving_tds','fantasy_points']].sort_values(by='week',ascending=False).reset_index(drop=True) 
#     return rec_table_wide

def get_rec_table_wide(player_season):
    rec_table_wide = player_season[player_season.book_stat=='receiving_yards'][['week','targets','receptions','receiving_tds','fantasy_points']].sort_values(by='week',ascending=False).reset_index(drop=True) 
    return rec_table_wide

def get_rec_table_skinny(player_season):
    rec_table_skinny = player_season[player_season.book_stat=='receiving_yards'][['week','receiving_yards']].sort_values(by='week',ascending=False).reset_index(drop=True) 
    return rec_table_skinny



def get_rec_table_skinny2(player_season):
    skinny = player_season[player_season.book_stat=='receiving_yards'][['week','receiving_yards']].sort_values(by='week',ascending=False).reset_index(drop=True) 
    rec_table_skinny2 = go.Figure(data = [go.Table(header = dict(values = ['<br><b>WEEK</b>', '<b>REC<br>YARDS</b>'],
                                                align = "center"),
                                    cells = dict(values = [skinny.week, skinny.receiving_yards],
                                                align = "center",
                                                font = dict(color = "white", size = 12, family = 'Courier New')))]).update_layout(height=600)
    return rec_table_skinny2








def get_player_scatter_vertical(player_season):
    player_scatter_vertical = px.scatter(player_season,x='targets',y='receiving_yards',
                        size='week',color='week',template='presentation',
                        size_max=17, height=600, #width=500
                        color_continuous_scale='blues',
                        # title = f"{player_season.player_display_name[0]}<br><b><span style='color:yellow'>{player_season.ud_line.mean()}</span><br><span style='color:purple'>{player_season.pp_line.mean()}</span><br>",
                        title = f"<span style='color:yellow'>ud<b>{player_season[player_season.book_stat=='receiving_yards'].ud_line.mean()}</b></span>    <span style='color:purple'>pp<b>{player_season[player_season.book_stat=='receiving_yards'].pp_line.mean()}</b></span>",                        
                        labels={'receiving_yards':'Receiving Yards','targets':'Targets'}).update_coloraxes(showscale=False).add_hline(y=player_season[player_season['book_stat']=='receiving_yards'].ud_line.mean(), line_width=2, line_color="yellow").add_hline(y=player_season[player_season['book_stat']=='receiving_yards'].pp_line.mean(), line_width=2, line_color="purple").update_yaxes(showgrid=True, gridcolor='grey')
    return player_scatter_vertical

def get_player_scatter_horizontal(player_season2):
    player_scatter_horizontal = px.scatter(player_season2,y='receiving_yards',
                                           template='plotly_white', size='targets', size_max=13,
                                           trendline="rolling", trendline_options=dict(function="median", window=6),trendline_scope="overall",
                                           labels={'index':'<b>Game</b>', 'receiving_yards':'<b>Rec Yards</b>'},
                                        #    width=1000,height=350,
                                           title = f"{player_season2.player_display_name[0]}<br><b><span style='color:yellow'>{player_season2.ud_line.mean()}</span><br><span style='color:purple'>{player_season2.pp_line.mean()}</span><br>"
                                           ).update_layout(showlegend=False).add_hline(y=(player_season2.pp_line.mean() + player_season2.ud_line.mean())/2, line_width=4, line_color="yellow")
    return player_scatter_horizontal
