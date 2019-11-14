"""
This will be the recommendation engine we use to make the calls
There are two approaces we shall take,

- A naive approach where we recommend other starships that are in the same film
- A less naive approach that will use cosine similarity to find other closely related startships that we can recommend
"""
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import logging


class StarShipRecommendation:

    """
    """

    def __init__(self):
        self.logger = logging.getLogger("starship-recommendation.starships.StarShipRecommendation")
        self.logger.setLevel(logging.INFO)

    @staticmethod
    def cosine_similarity_table(feature_processed_columns, target_columns=None):
        return cosine_similarity(feature_processed_columns, target_columns)

    @staticmethod
    def make_recommendation(cosine_similarity_df, sort_col, return_cols):
        sorted_df = cosine_similarity_df.sort_values(by=[sort_col], ascending=False)
        return sorted_df[return_cols]
