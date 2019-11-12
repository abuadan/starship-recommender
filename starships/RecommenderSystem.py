"""
This will be the recommendation engine we use to make the calls
There are two approaces we shall take,

- A naive approach where we recommend other starships that are in the same film
- A less naive approach that will use cosine similarity to find other closely related startships that we can recommend
"""
from sklearn.metrics.pairwise import cosine_similarity


class StarShipRecommendation:
    """

    """

    def __init__(self, naive=None, less_naive=None):
        """

        :param naive:
        :param less_naive:
        """
        self.naive = naive
        self.less_naive = less_naive

    def recommend_based_on_film(self):
        pass

    def starship_to_starship_similarity(self, starship_one, startship_two):
        pass
