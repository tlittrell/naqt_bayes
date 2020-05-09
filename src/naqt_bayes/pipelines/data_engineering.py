from kedro.pipeline import Pipeline, node
from kedro.pipeline.decorators import log_time

from naqt_bayes.nodes.process_game_data import process_game_data
from naqt_bayes.nodes.scrape import scrape_all_games


def scrape_data_pipeline() -> Pipeline:

    pipeline = Pipeline(
        [
            node(
                func=scrape_all_games,
                inputs="parameters",
                outputs="raw_all_games",
                name="Scrape game data",
            ),
            node(
                func=process_game_data,
                inputs="raw_all_games",
                outputs="primary_all_games",
                name="process game data",
            ),
        ]
    ).decorate(log_time)
    return pipeline
