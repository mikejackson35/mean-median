


API_KEY = '7a790b61b403c766e6226ab27c579d97'
sport = 'americanfootball_nfl'
markets = f"player_pass_yds,player_reception_yds,player_rush_yds"




def remove_NFLSZN_ud(df):
    # Filter out rows based on the conditions
    filtered_df = df[~(
        ((df['market'] == 'passing_yards') & (df['ud_line'] > 500)) |
        ((df['market'] == 'receiving_yards') & (df['ud_line'] > 200)) |
        ((df['market'] == 'receiving_tds') & (df['ud_line'] > 2.5)) |
        ((df['market'] == 'receptions') & (df['ud_line'] > 15)) |
        ((df['market'] == 'rushing_tds') & (df['ud_line'] > 3)) |
        ((df['market'] == 'rushing_yards') & (df['ud_line'] > 200)) |
        ((df['market'] == 'carries') & (df['ud_line'] > 30))
    )]
    return filtered_df

def remove_NFLSZN_pp(df):
    # Filter out rows based on the conditions
    filtered_df = df[~(
        ((df['market'] == 'passing_yards') & (df['pp_line'] > 500)) |
        ((df['market'] == 'receiving_yards') & (df['pp_line'] > 200)) |
        ((df['market'] == 'receiving_tds') & (df['pp_line'] > 2.5)) |
        ((df['market'] == 'receptions') & (df['pp_line'] > 15)) |
        ((df['market'] == 'rushing_tds') & (df['pp_line'] > 3)) |
        ((df['market'] == 'rushing_yards') & (df['pp_line'] > 200)) |
        ((df['market'] == 'carries') & (df['pp_line'] > 30))
    )]
    return filtered_df

# stats dictionary for clean mapping
stats_dict = {'1Q Passing Yards': '1q_passing_yards',
    '1Q Receiving Yards': '1q_receiving_yards',
    '1Q Rushing Yards': '1q_rushing_yards',
    '48+ Yard FG Made (Combo)': '48+yard_fg_made_combo',
    'Assists': 'assists',
    'Avg Yards Per Punt': 'avg_yards_per_punt',
    'Completion Percentage': 'completion_perc',
    'Completions': 'completions',
    'FG Made': 'fg_made',
    'FG Made (Combo)': 'fg_made_combo',
    'Fantasy Points': 'fantasy_points',
    'Fantasy Score': 'fantasy_points',
    'Field Goal Yards (Combo)': 'fg_yards_combo',
    '1H Passing Yards': '1h_passing_yards',
    '1H Receiving Yards': '1h_receiving_yards',
    '1H Rushing Yards': '1h_rushing_yards',
    'INT': 'interceptions',
    'Interceptions':'interceptions',
    'Kicking Points': 'kicking_points',
    'Longest Completion': 'longest_completion',
    'Longest Reception': 'longest_reception',
    'Longest Rush': 'longest_rush',
    'Pass + Rush Yards': 'pass+rush_yards',
    'Pass Attempts': 'attempts',
    'Pass Completions': 'completions',
    'Pass TDs': 'passing_tds',
    'Pass Yards': 'passing_yards',
    'Pass Yards (Combo)': 'pass_yards_combo',
    'Pass+Rush Yds': 'pass+rush_yards',
    'Pass+Rush+Rec TDs': 'pass+rush+rec_tds',
    'Passing Attempts': 'attempts',
    'Passing First Downs': 'passing_first_downs',
    'Passing TDs': 'passing_tds',
    'Passing Yards': 'passing_yards',
    'Rec Targets': 'targets',
    'Receiving TDs': 'receiving_tds',
    'Receiving Yards': 'receiving_yards',
    'Receiving Yards (Combo)': 'rec_yards_combo',
    'Receiving Yards in First 2 Receptions': 'rec_yards_first_2_receptions',
    'Receptions': 'receptions',
    'Rush + Rec First Downs': 'rush+rec_first_downs',
    'Rush + Rec TDs': 'rush+rec_tds',
    'Rush + Rec Yards': 'rush+rec_yards',
    'Rush Attempts': 'carries',
    'Rush Yards': 'rushing_yards',
    'Rush Yards (Combo)': 'rush_yards_combo',
    'Rush Yards in First 5 Attempts': 'rush_yards_first_5_attempts',
    'Rush+Rec TDs': 'rush+rec_tds',
    'Rush+Rec TDs (Combo)': 'rush+rec_tds_combo',
    'Rush+Rec Yds': 'rush+rec_yards',
    'Rush+Rec Yds (Combo)': 'rush+rec_yards_combo',
    'Rushing Attempts': 'carries',
    'Rushing TDs':'rushing_tds',
    'Rushing Yards': 'rushing_yards',
    'Sacks': 'sacks',
    'Sacks Taken': 'sacks_taken',
    'Solo Tackles': 'solo_tackles',
    'Tackles + Assists': 'tackles+assists',
    'Targets': 'targets',
    'XP Made': 'xp_made'}