import logging
import re
import time
from typing import Dict

import pandas as pd
import requests
from bs4 import BeautifulSoup

log = logging.getLogger(__name__)


def scrape_all_games(conf: Dict) -> pd.DataFrame:
    tournaments = conf["tournaments"]
    team_url = conf["team_url"]

    all_tournaments = []
    for tournament_name, tournament_url in tournaments.items():
        log.info(f"scraping data for {tournament_name}")
        df = scrape_game_data(tournament_url, team_url)
        df["tournament"] = tournament_name
        all_tournaments.append(df)
    return pd.concat(all_tournaments)


def scrape_game_data(tournament_url: str, team_url: str) -> pd.DataFrame:

    # Get team numbers for every team in the tournament
    page = requests.get(tournament_url)
    soup = BeautifulSoup(page.content, "html.parser")
    tb = soup.find("table", class_="data-freeze-2 unstriped")
    all_teams = [str(x) for x in tb.find_all("a")]
    pattern_number = "team_id=([0-9]+)"
    pattern_team = ">(.+)<"
    number_team = [
        (re.findall(pattern_number, line)[0], re.findall(pattern_team, line)[0])
        for line in all_teams
    ]

    # Scrape games
    result = pd.DataFrame()
    for i, (number, team) in enumerate(number_team):
        if i % 10 == 0:
            log.info(f"scraped {i} teams")
        tmp = pd.read_html(team_url + number)[2]
        tmp["team"] = team
        result = pd.concat([result, tmp])
        time.sleep(0.01)

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
