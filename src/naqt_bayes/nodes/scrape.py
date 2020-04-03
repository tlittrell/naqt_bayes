import requests
from bs4 import BeautifulSoup
import re
import time
import pandas as pd


def scrape_game_data() -> pd.DataFrame:
    url = "https://www.naqt.com/stats/tournament/standings.jsp?tournament_id=9500"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    tb = soup.find("table", class_="data-freeze-2 unstriped")
    all_teams = [str(x) for x in tb.find_all("a")]
    pattern_number = "team_id=([0-9]+)"
    pattern_team = ">(.+)<"
    number_team = [
        (re.findall(pattern_number, line)[0], re.findall(pattern_team, line)[0])
        for line in all_teams
    ]
    result = pd.DataFrame()
    for i, (number, team) in enumerate(number_team):
        if i % 10 == 0:
            print(i)
        try:
            tmp = pd.read_html(
                "https://www.naqt.com/stats/tournament/team.jsp?team_id=" + number
            )[2]
            tmp["team"] = team
            result = pd.concat([result, tmp])
            time.sleep(0.05)
        except:
            print("{0} {1} {2}".format(i, number, team))
    return result


def scrape_player_game_data() -> pd.DataFrame:
    url = "https://www.naqt.com/stats/tournament/individuals.jsp?tournament_id=9500&playoffs=true"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    tb = soup.find("table", class_="data-freeze-2")
    all_players = [str(x) for x in tb.find_all("a") if "tournament/team" not in str(x)]
    pattern_player_number = "team_member_id=([0-9]+)"
    pattern_player_name = ">(.+)<"
    player_number_tuple = [
        (
            re.findall(pattern_player_number, line)[0],
            re.findall(pattern_player_name, line)[0],
        )
        for line in all_players
    ]
    result = pd.DataFrame()
    for i, (number, player) in enumerate(player_number_tuple):
        if i % 50 == 0:
            print(i)
        tmp = pd.read_html(
            "https://www.naqt.com/stats/tournament/player.jsp?team_member_id=" + number
        )[1]
        tmp["player"] = player
        result = pd.concat([result, tmp])
        time.sleep(0.05)
        return result
