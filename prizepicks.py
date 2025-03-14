import tls_client
import pandas as pd
from new_utils import stats_dict,remove_NFLSZN_pp


def get_prizepicks():

    # headers = {
    #     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
    #             'application/signed-exchange;v=b3;q=0.7',
    #     'accept-language': 'en-US,en;q=0.9',
    #     'cache-control': 'no-cache',
    #     'pragma': 'no-cache',
    #     'sec-ch-ua': '"Not.A/Brand";v="99", "Chromium";v="91", "Google Chrome";v="91"',
    #     'sec-ch-ua-mobile': '?0',
    #     'sec-ch-ua-platform': '"Windows"',
    #     'sec-fetch-dest': 'document',
    #     'sec-fetch-mode': 'navigate',
    #     'sec-fetch-site': 'none',
    #     'sec-fetch-user': '?1',
    #     'upgrade-insecure-requests': '1',
    #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
    #                 'Chrome/91.0.4472.124 Safari/537.36'
    # }

    requests = tls_client.Session(client_identifier="chrome112")

    # Fetch data from Prizepicks API
    response1 = requests.get('https://api.prizepicks.com/projections')#, headers=headers)
    prizepicks = response1.json()
    # prizepicks

    # Create empty list to store player data
    pplist = []

    # Dictionary to store PrizePicks player name mappings
    library = {}

    # Process PrizePicks API data (populates player library)
    for included in prizepicks['included']:
        if 'attributes' in included and 'name' in included['attributes']:
            PPname_id = included['id']
            PPname = included['attributes']['name']
            if 'team' in included['attributes']:
                ppteam = included['attributes']['team']
            else:
                ppteam = 'N/A'
            if 'league' in included['attributes']:
                ppleague = included['attributes']['league']
            else:
                ppleague = 'N/A'
            library[PPname_id] = {'name': PPname, 'team': ppteam, 'league': ppleague}
            
    for ppdata in prizepicks['data']:
        if '1st Half' in ppdata['attributes']['description']:
            continue
        PPid = ppdata['relationships']['new_player']['data']['id']
        PPprop_value = ppdata['attributes']['line_score']
        PPprop_type = ppdata['attributes']['stat_type']
        ppinfo = {"name_id": PPid, "Stat": PPprop_type, "Prizepicks": PPprop_value}
        pplist.append(ppinfo)

    # Iterate over the pplist array to add player names, team, and league, and remove name_id
    for element in pplist:
        name_id = element['name_id']
        if name_id in library:
            player_data = library[name_id]
            element['Name'] = player_data['name']
            element['Team'] = player_data['team']
            element['League'] = player_data['league']
        else:
            element['Name'] = "Unknown"
            element['Team'] = "N/A"
            element['League'] = "N/A"
        del element['name_id']
        
    pp_df = pd.DataFrame.from_dict(pd.json_normalize(pplist), orient='columns')

    # ----- RENAME COLUMNS -------
    pp_df.rename(columns={'Name':'player','Team':'team','Stat':'market','Prizepicks':'pp_line', 'League':'sport'},inplace=True)


    # ----- CHANGE PP PLAYER NAME TO NFL PLAYER NAME ------
    # name_dict = {'Kenneth Walker III':'Kenneth Walker','Michael Pittman Jr.':'Michael Pittman','D.K. Metcalf':'DK Metcalf'}
    # pp_df.replace(name_dict, inplace=True)

    # ----- GRAB FOOTBALL ONLY ------
    pp = pp_df[pp_df.sport == 'NFL']

    # pp = pp.groupby(['player','market'])['pp_line'].median().reset_index()

    pp = pp[['player','market','pp_line']]

    # normalize market column
    pp['market'] = pp['market'].map(stats_dict)
    pp = pp.astype({'player':str,'market':'category','pp_line':float})
    pp = remove_NFLSZN_pp(pp)

    prizepicks = pp.drop_duplicates(subset=['player','market'], keep='first')

    return prizepicks