"""

"""


from request_maker.request_builder import AsyncRequestMaker, SyncRequestMaker
import requests
import logging
import json
import swapi

Global_FILM_DICT = {
    "1": "in_film_one",
    "2": "in_film_two",
    "3": "in_film_three",
    "4": "in_film_four",
    "5": "in_film_five",
    "6": "in_film_six",
    "7": "in_film_seven",
    "8": "in_film_eight"
}

FILM_NUM_DICT = {
    "in_film_one": 0,
    "in_film_two": 0,
    "in_film_three": 0,
    "in_film_four": 0,
    "in_film_five": 0,
    "in_film_six": 0,
    "in_film_seven": 0,
    "in_film_eight": 0
}

logging.basicConfig(level=logging.INFO)
module_logger = logging.getLogger('starship-recommendation.request_maker')
module_logger.setLevel(logging.INFO)


class RetrieveData:

    def __init__(self, category):
        self.logger = logging.getLogger("starship-recommendation.request_maker.RetrieveData")
        self.logger.setLevel(logging.INFO)
        if category == "people" or category == "films" or category == "starships":
            self.category = category
        else:
            raise ValueError("The category accepted by the URL builder must either people, films or starships")

    @staticmethod
    def base_url():
        return "https://swapi.co/api"

    def api_url_builder(self, upper_range):
        """

        :param upper_range:
        :return:
        """

        return ["{0}/{1}/{2}/".format(self.base_url(), self.category, i) for i in range(1, upper_range)]

    def get_count(self):
        url = "{0}{1}".format(self.base_url(), self.category)
        r = requests.get(url).json
        return r["count"]

    def api_requests(self, upper_range, sync_or_async):
        urls = self.api_url_builder(upper_range)
        if sync_or_async == "sync":
            request_maker = SyncRequestMaker(3, 0.6)
            responses = request_maker.make_request(urls)
            return responses
        else:
            request_maker = AsyncRequestMaker()
            responses = request_maker.run_fetch_all(urls)
            return responses


class ParseInfo:

    """

    """

    def __init__(self, category):
        self.logger = logging.getLogger("starship-recommendation.request_maker.RetrieveData")
        self.logger.setLevel(logging.INFO)
        self.category = category

    @staticmethod
    def __request_all_starships__():
        response = swapi.get_all("starships")
        raw_output = json.dumps(response, default=lambda o: o.__dict__, indent=4)
        return json.loads(raw_output)["items"]

    @staticmethod
    def __film_info_collector__(film_urls, starship_or_pilot="starship"):
        if starship_or_pilot == "starship":
            film_data = FILM_NUM_DICT
            for url in film_urls:
                film_number = url.split("/")[-2]
                item = Global_FILM_DICT.get("{}".format(film_number))
                film_data[item] = 1
            return film_data

    @staticmethod
    def __pilot_info_collector__(pilot_urls):
        data = {"number_of_pilots": len(pilot_urls)}
        return data

    def parse_starship_info(self, starwars_responses):
        results = []
        for response in starwars_responses:
            if response:
                film_info = self.__film_info_collector__(response["films"])
                pilot_info = self.__pilot_info_collector__(response["pilots"])
                starship_id = {"starship_id": response["url"].split("/")[-2]}
                response.pop("films")
                response.pop("pilots")
                response.update(film_info)
                response.update(pilot_info)
                response.update(starship_id)
                results.append(response)
        return results


if __name__ == "__main__":

    test = RetrieveData(category="starships")
    test2 = ParseInfo(category="starships")
    output = test.api_requests(10, "async")
    stuff = test2.parse_starship_info(output)
    print(stuff)
