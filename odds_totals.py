import requests
import pandas as pd

from new_utils import API_KEY, sport

# # Define the URL for the API
# url = f'https://api.the-odds-api.com/v4/sports/{sport}/odds/?apiKey={API_KEY}&regions=us&markets=spreads,totals'
# response = requests.get(url)

# data = response.json()
# odds_and_totals = pd.DataFrame(data)

# # Clean odds and totals
# results = []  # List to store extracted data

def get_odds_and_totals():

    # Define the URL for the API
    url = f'https://api.the-odds-api.com/v4/sports/{sport}/odds/?apiKey={API_KEY}&regions=us&markets=spreads,totals'
    response = requests.get(url)

    data = response.json()
    raw_odds_and_totals = pd.DataFrame(data)

    # Clean odds and totals
    results = []  # List to store extracted data

    for index, row in raw_odds_and_totals.iterrows():
        # Remove city names from team names
        home_team = ' '.join(row['home_team'].split()[-1:])
        away_team = ' '.join(row['away_team'].split()[-1:])

        # Check if 'bookmakers' is a list and has elements
        if isinstance(row['bookmakers'], list):
            # Find the 'betrivers' bookmaker
            betrivers = next((bm for bm in row['bookmakers'] if bm['key'] == 'betrivers'), None)

            if betrivers and 'markets' in betrivers:
                # Find the 'spreads' market
                spreads_market = next((market for market in betrivers['markets'] if market['key'] == 'spreads'), None)

                # Find the 'totals' market for over/under
                totals_market = next((market for market in betrivers['markets'] if market['key'] == 'totals'), None)

                # Extract the over/under value if available
                over_under = None
                if totals_market and 'outcomes' in totals_market:
                    # Ensure the outcomes list is not empty and contains the expected structure
                    if totals_market['outcomes']:
                        # Loop through outcomes to find a valid total (if multiple exist)
                        for total_outcome in totals_market['outcomes']:
                            if 'point' in total_outcome:
                                over_under = total_outcome['point']
                                break  # Use the first valid point found

                if spreads_market and 'outcomes' in spreads_market:
                    # Extract the point spread for each team
                    outcomes = spreads_market['outcomes']
                    for outcome in outcomes:
                        team = ' '.join(outcome['name'].split()[-1:])  # Remove city from team name
                        line = outcome['point']

                        # Determine if the team is home or away
                        home_away = team == home_team  # True if home, False if away
                        opponent = away_team if home_away else home_team

                        # Append the data to results
                        results.append({
                            'team': team,
                            'home_away': home_away,
                            'opponent': opponent,
                            'line': line,
                            'over_under': over_under
                        })

    # Convert results to a DataFrame for easier analysis
    odds_and_totals = pd.DataFrame(results)
    return odds_and_totals