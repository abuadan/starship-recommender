# -*- coding: utf-8 -*-

from flask import Flask, request
import json
from utils.destinations import destinations
import swapi
from preprocess_starship_data import PreProcessing
from recommender_system import StarShipRecommendation
import pandas as pd
import os

app = Flask(__name__)

# POST: /api/starships/recommend
# =====================
# --------------------------------------------------
# Content-Type: application/json
#
# { "id": 6 }
# --------------------------------------------------
# Example response:
# --------------------------------------------------
# Content-Type: application/json
#  curl -H "Content-Type: application/json" -X POST http://0.0.0.0:5000/api/starships/recommend -d '{"id":9}'
# { "alternatives": [ {starship 1}, {starship 2}, {starship 3} ...] }
# --------------------------------------------------

""" Write your API endpoint here """

# GET: /api/starships/
# =====================


def __cosine_similartie__():
    if not os.path.exists("cosine_similarities.csv"):
        preprocessor = PreProcessing("starships")
        cosine_sim = StarShipRecommendation()
        data = preprocessor.run_preprocessing().set_index("name", drop=True)
        cosine_sim = cosine_sim.cosine_similarity_table(data.drop(labels=["starship_id"], axis=1),
                                                        data.drop(labels=["starship_id"], axis=1))
        df = pd.DataFrame(cosine_sim, columns=data.index)
        try:
            df.index = data.index
            df.to_csv("cosine_similarities.csv", index=True)
            data[["starship_id"]].to_csv("id_to_name.csv", index=True)
            return df
        except Exception as e:
            raise e
    else:
        return pd.read_csv("cosine_similarities.csv")


def recommend(starship_id):
    recommending_engine = StarShipRecommendation()
    df = pd.read_csv("cosine_similarities.csv")
    id_to_name = pd.read_csv("id_to_name.csv")
    name = id_to_name.loc[id_to_name["starship_id"] == starship_id]
    recommendation = recommending_engine.make_recommendation(df,
                                                             sort_col=name.iloc[0, 0],
                                                             return_cols=["name",
                                                                          name.iloc[0, 0]])

    recommendation.columns = ["name", "relevance"]
    return recommendation.to_dict(orient="records")


@app.route('/api/starships', methods=['GET'])
def get_starships():
    try:
        starships = swapi.get_all("starships")
    except:
        response = {"error": "something went wrong"}

    return json.dumps(starships, default=lambda o: o.__dict__, indent=4)


@app.route("/api/starships/recommend", methods=["POST"])
def get_recommendation():

    """

    :return:
    """
    starship_id = request.get_json()
    print(starship_id["id"])
    recommendation = recommend(starship_id.get('id'))  # call model for recommendation here
    return json.dumps(recommendation, default=lambda o: o.__dict__, indent=4)


if __name__ == '__main__':
    __cosine_similartie__()
    app.run(host='0.0.0.0', port=5000)
