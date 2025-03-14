import json
from urllib.request import Request, urlopen
import pandas as pd
from new_utils import stats_dict,remove_NFLSZN_ud


# UNDERDOG API

# def get_underdog(sportName2=None):
def get_underdog():

    sportName2 = 'NFL'
        
    url = 'https://api.underdogfantasy.com/beta/v3/over_under_lines'
    req2 = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    dataFile2 = json.loads(urlopen(req2).read())

    underdogFantasy = []
    for dataNames in dataFile2['over_under_lines']:
            splitted = dataNames['over_under']['title'].split()
            underdogFantasy.append({
                    'OverUnder': dataNames['stat_value'],
                    'Name': splitted[0]+" "+splitted[1],
                    'Stat Type': dataNames['over_under']['appearance_stat']['display_stat']
            })
            names2 = []
    for dataNames in dataFile2['players']:
            names2.append({
                    'First Name': dataNames['first_name'],
                    'Last Name': dataNames['last_name'],
                    'Sport': dataNames['sport_id']
            })

    nameFrame = pd.DataFrame(names2)
    nameFrame = nameFrame[nameFrame['Sport'] != 'NFLSZN']
    underdogFrame = pd.DataFrame(underdogFantasy)
    nameFrame['Name'] = nameFrame['First Name'] + " " + nameFrame['Last Name']

    result = pd.merge(underdogFrame, nameFrame, on=["Name"])
    result = result[['Name', 'Stat Type', 'OverUnder', 'Sport']]

    if sportName2 == None:
            return result
    else:
            sportName2 = str(sportName2).upper()
            result = result.loc[result['Sport'] == sportName2]
            return result

    ud = result.rename(columns={'Name':'player','Stat Type':'market','OverUnder':'ud_line'})
    ud = ud.drop(columns=['Sport'])

    ud['market'] = ud['market'].map(stats_dict)                             # normalize market column
    ud = ud.astype({'player':str,'market':'category','ud_line':float})      # convert to string and category
    ud = remove_NFLSZN_ud(ud)

    return ud