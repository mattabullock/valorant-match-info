from flask import Flask, render_template
from app import app
import os
import json


@app.route("/", methods=["GET"])
def index():
    return "home"


@app.route("/api/user/<uid>/match_history")
def get_history(uid: str = ""):
    return None


@app.route("/api/user/<uid>/latest")
def get_latest_game(uid: str = ""):
    return None


@app.route("/api/user/<uid>/mmr")
def get_mmr(uid: str = ""):
    return None


@app.route("/api/user/<uid>/kills")
def get_kills(uid: str = ""):
    path = os.path.dirname(os.path.abspath(__file__))

    files = os.listdir(f"{path}/../data/{uid}")

    games = {}

    for file in files:
        game_obj: dict = {}
        file_path = f"{path}/../data/{uid}/{file}"
        game_file = open(file_path, "r")
        game = json.load(game_file)
        game_id = game["matchInfo"]["matchId"]
        game_obj["mapId"] = game["matchInfo"]["mapId"]

        # comp/unrated/snowball/etc
        game_obj["queueID"] = game["matchInfo"]["queueID"]

        # Get info about the game
        index = next(
            (i for i, item in enumerate(game["players"]) if item["subject"] == uid), -1
        )
        game_obj["competitiveTier"] = game["players"][index]["competitiveTier"]
        game_obj["characterId"] = game["players"][index]["characterId"]

        # Grab kills
        game_kills = []
        roundResults = game["roundResults"]
        for round in roundResults:
            plant_time = round["plantRoundTime"]
            index = next(
                (
                    i
                    for i, item in enumerate(round["playerStats"])
                    if item["subject"] == uid
                ),
                -1,
            )
            kills = round["playerStats"][index]["kills"]
            for kill in kills:
                if kill["roundTime"] > plant_time:
                    kill["postPlant"] = True
                    kill["plantSite"] = round["plantSite"]
            game_kills += kills

        game_obj["kills"] = game_kills
        games[game_id] = game_obj

    return games
