"""
This file will contain the code to calculate the cosine similarity
There will be two parts
- a pre-processing section
- a model generation
"""
import logging
import category_encoders as ce
from sklearn.metrics.pairwise import cosine_similarity
from CollectInfo import ParseInfo
import pandas as pd

module_logger = logging.getLogger("starship-recommendation.model")
module_logger.setLevel(logging.INFO)


class RecommendStarship(ParseInfo):

    """
    """

    def __init__(self, category):
        super(ParseInfo).__init__(category)
        self.logger = logging.getLogger("starship-recommendation.model.Model")
        self.logger.setLevel(logging.INFO)

    def __read_raw_processed_data__(self):
        request_starships = self.__request_all_starships__()
        return request_starships

    def __parse_data__(self, raw_data):
        return self.parse_starship_info(raw_data)

    @staticmethod
    def feature_encoding(raw_data, cols_to_encode):
        return ce.cat_boost.CatBoostEncoder(raw_data, cols=cols_to_encode)

    @staticmethod
    def cosine_similarity_table(feature_processed_columns):
        return cosine_similarity(feature_processed_columns)

    @staticmethod
    def __save_data_to_memory_table__():
        return pd.DataFrame.to_sql()
