from kedro.pipeline import Pipeline, node

from naqt_bayes.nodes.scrape import scrape_game_data
from naqt_bayes.nodes.process_game_data import process_game_data


def scrape_data_pipeline() -> Pipeline:

    pipeline = Pipeline([
        node(func=scrape_game_data,
             inputs=None,
             outputs="raw_2018_all_games",
             name="Scape 2018 game data"),
        node(func=process_game_data,
             inputs="raw_2018_all_games",
             outputs="2018_all_games",
             name="process game data")

    ])
    return pipeline