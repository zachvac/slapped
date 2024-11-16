from functools import reduce
import functions_framework
import requests
import pandas as pd

num_weeks = 12
cookies = {'swid':'{97FD64FC-E909-4847-9481-08840AEA0E3D}','espn_s2':'AEBk%2BZxnTuZgtmMbgAf1ZD%2BQVk0%2FINTvdsJ9YwerfLFcGQAznxuOQ2Lq%2ByVeam2XMB%2FCnKSXEwd112wrC65B4LOcdz3%2FT14S7hDJ0c5csb2HxU5%2F4RmbhdAsytRJC7eXF%2FpRw3pjIMwMGWOLqfvYj%2FEZG7inQG3ZAOoGI%2BTUKMCHaOrio8OQxf1jYDJmnDbzED%2FdCGyYhWomaOtd%2FpjlsUdWSsaVmwm59bO7p2PUvTyskaBTvn21325LM7aYG4BjWiCmUhkY8BbUtLCo8kpHblvR'}

def extract_name_score(players, week):
    player = players["player"]
    name = player["fullName"]
    correct_stat = [stat for stat in player["stats"] if (stat["seasonId"] == 2024) & (stat["scoringPeriodId"] == week) & (stat["statSourceId"] == 0)]
    return name, correct_stat[0]["appliedTotal"] if len(correct_stat) > 0 else 0

def get_scores_for_week(week):
    res = requests.get(f"https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/2024/segments/0/leagues/748024?scoringPeriodId={week}&view=kona_playercard", cookies=cookies, headers={"x-fantasy-filter": '''{"players": {"limit": 1500,"sortDraftRanks": {"sortPriority": 100,"sortAsc": true,"value": "STANDARD"}}}'''})
    assert res.status_code == 200
    return [extract_name_score(players, week) for players in res.json()["players"]]

@functions_framework.http
def hello_http(request):
    headers = {
        'Access-Control-Allow-Origin': '*',
        "Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept",
        "Access-Control-Allow-Methods": "POST"
    }
    if request.method == "OPTIONS":
        return ("", 200, headers)
    scores = [get_scores_for_week(i) for i in range(1,num_weeks)]
    score_dfs = [pd.DataFrame(scores[i-1]).set_index(0).rename(columns={1:f"week {i}"}) for i in range(1,num_weeks)]
    score_df = reduce(lambda x, y: x.merge(y,left_index=True,right_index=True), score_dfs)
    score_df = score_df[~score_df.index.isin(["Ryan Griffin", "Josh Johnson"])]
    score_dict = score_df.to_dict(orient="split")
    score_dict_clean = {}
    for i,x in enumerate(score_dict["index"]):
        score_dict_clean[x] = score_dict["data"][i]
    return (score_dict_clean, 200, headers)
