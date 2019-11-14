"""
This file will contain the code to calculate the cosine similarity
There will be two parts
- a pre-processing section
- a preprocess generation
"""
import logging
import category_encoders as ce
from request_maker.collect_info import ParseInfo
import pandas as pd
from sklearn import preprocessing
import numpy as np

module_logger = logging.getLogger("starship-recommendation.preprocess")
module_logger.setLevel(logging.INFO)


class PreProcessing(ParseInfo):

    """
    """

    def __init__(self, category):
        self.category = category
        super(ParseInfo, self).__init__()
        self.logger = logging.getLogger("starship-recommendation.preprocess.PreProcessing")
        self.logger.setLevel(logging.INFO)

    def __read_raw_processed_data__(self):
        request_starships = self.__request_all_starships__()
        return request_starships

    def __parse_data__(self, raw_data):
        return self.parse_starship_info(raw_data)

    @staticmethod
    def fix_missing_info_columne(x):
        try:
            return float(x)
        except ValueError:
            if type(x) == float or type(x) == int:
                return x
            if "unknown" in x:
                return np.nan
            if "km" in x:
                return float(x.strip("km"))
            if "n/a" in x:
                return np.nan
            if "year" in x:
                return float("".join(filter(str.isdigit, x)))
            if "month" in x:
                return int("".join(filter(str.isdigit, x))) / 12
            if "week" in x:
                return int("".join(filter(str.isdigit, x))) / 54

    @staticmethod
    def preprocess_missing_data_point(data, cols_to_process):
        data[cols_to_process] = data[cols_to_process].apply(pd.to_numeric, errors='coerce')
        return data

    @staticmethod
    def feature_encoding(raw_data, cols_to_encode):
        enc = ce.one_hot.OneHotEncoder(cols=cols_to_encode)
        return enc.fit_transform(raw_data.drop(labels=["name", "starship_id"], axis=1), raw_data["starship_id"])

    @staticmethod
    def standerdise_features(dirty_x, cols_to_standerdise):
        scalar = preprocessing.MinMaxScaler()
        dirty_x[cols_to_standerdise] = scalar.fit_transform(dirty_x[cols_to_standerdise])
        return dirty_x

    def run_preprocessing(self):
        raw_data = self.__read_raw_processed_data__()
        parse_raw_data = self.__parse_data__(raw_data)
        raw_df = pd.DataFrame(parse_raw_data)
        raw_drop_cols = raw_df.drop(labels=["url", "created", "edited", "model"], axis=1)
        raw_drop_cols["crew"] = raw_drop_cols["crew"].apply(self.fix_missing_info_columne)
        raw_drop_cols["consumables"] = raw_drop_cols["consumables"].apply(self.fix_missing_info_columne)
        raw_drop_cols["cost_in_credits"] = raw_drop_cols["cost_in_credits"].apply(self.fix_missing_info_columne)
        raw_drop_cols["max_atmosphering_speed"] = raw_drop_cols["max_atmosphering_speed"].apply(
                self.fix_missing_info_columne)
        raw_data_handle_missing = self.preprocess_missing_data_point(raw_drop_cols, ["MGLT", "cargo_capacity",
                                                                                     "hyperdrive_rating",
                                                                                     "consumables",
                                                                                     "max_atmosphering_speed",
                                                                                     "cost_in_credits", "length",
                                                                                     "passengers"])
        standardise_data = self.standerdise_features(raw_data_handle_missing, ["MGLT", "cargo_capacity",
                                                                                     "hyperdrive_rating",
                                                                                     "consumables",
                                                                                     "max_atmosphering_speed",
                                                                                     "cost_in_credits", "length",
                                                                                     "passengers", "number_of_pilots"])
        encode_categories = self.feature_encoding(standardise_data, ["manufacturer", "starship_class"])
        processed_data = pd.concat([raw_df[["name", "starship_id"]], encode_categories], axis=1)
        processed_data = processed_data.fillna(-1)
        return processed_data


if __name__ == "__main__":
    data_ = PreProcessing("starships")
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(data_.run_preprocessing())
