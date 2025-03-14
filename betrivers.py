import requests
import pandas as pd

from new_utils import API_KEY, markets, sport


# Chose sports and markets and put in a DataFrame

# Construct the full URL with the API key
# url = f'https://api.the-odds-api.com/v4/sports/{sport}/events/e0b1a11b515324fa603bb16ff278dcbf/odds?apiKey={API_KEY}&regions=us&markets={markets}&oddsFormat=american'

# response = requests.get(url)
# data = response.json()
# betrivers = pd.DataFrame(data)

# results = []

def get_betrivers():

# Construct the full URL with the API key
    url = f'https://api.the-odds-api.com/v4/sports/{sport}/events/3fd7cba821568399920fcea4dadad30d/odds?apiKey={API_KEY}&regions=us&markets={markets}&oddsFormat=american'

    response = requests.get(url)
    data = response.json()
    betrivers = pd.DataFrame(data)

    results = []

    for index, row in betrivers.iterrows():
        # Remove city names from team names
        home_team = ' '.join(row['home_team'].split()[1:])
        away_team = ' '.join(row['away_team'].split()[1:])

        # Check if 'bookmakers' is a dictionary
        if isinstance(row['bookmakers'], dict):
            bookmakers = row['bookmakers']  # Directly use the dictionary

            # Check if this bookmaker is 'betrivers'
            if bookmakers.get('key') == 'betrivers' and 'markets' in bookmakers:
                for market in bookmakers['markets']:
                    market_key = market['key']
                    if market_key in ['player_pass_yds', 'player_reception_yds', 'player_rush_yds']:
                        if 'outcomes' in market:
                            for outcome in market['outcomes']:
                                player_name = outcome.get('description', 'Unknown Player')
                                stat_type = market_key  # e.g., player_pass_yds
                                line = outcome.get('point', None)
                                price = outcome.get('price', None)

                                # Append the data to results
                                results.append({
                                    'player': player_name,
                                    'stat_type': stat_type,
                                    'line': line,
                                    # 'price': price,
                                    # 'home_team': home_team,
                                    # 'away_team': away_team
                                })

    # Convert results to a DataFrame for easier analysis
    betrivers = pd.DataFrame(results).rename(columns={'stat_type': 'market'}).drop_duplicates(subset=['player', 'market'])

    betrivers['market'] = betrivers['market'].map({'player_reception_yds': 'receiving_yards',
                                            'player_pass_yds': 'passing_yards',
                                            'player_rush_yds': 'rushing_yards'})
    
    return betrivers