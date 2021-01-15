from flask import Flask, render_template, request

from ecoround import app, utils

import os
import sys
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


# TODO: regexes!
@app.route("/user/<uid>/kills/<game_map>")
def get_kills(uid: str = "", game_map: str = ""):
    # move this
    GAME_MAPS = {
        "ascent": "/Game/Maps/Ascent/Ascent",
        "icebox": "/Game/Maps/Port/Port",
        "split": "/Game/Maps/Duality/Duality",
        "haven": "/Game/Maps/Triad/Triad",
        "bind": "/Game/Maps/Bonsai/Bonsai",
    }

    files = utils.get_files_by_uid(uid)

    games = []

    for file_path in files:
        game_obj: dict = {}
        with open(file_path, "r") as game_file:
            game = json.load(game_file)
            game_id = game["matchInfo"]["matchId"]
            game_obj["mapId"] = game["matchInfo"]["mapId"]
            if game_obj["mapId"] != GAME_MAPS[game_map]:
                continue

            # comp/unrated/snowball/etc
            game_obj["queueID"] = game["matchInfo"]["queueID"]
            if game_obj["queueID"] != "competitive":
                continue

            # Get info about the game
            index = next(
                (i for i, item in enumerate(game["players"]) if item["subject"] == uid),
                -1,
            )
            game_obj["competitiveTier"] = game["players"][index]["competitiveTier"]
            game_obj["characterId"] = game["players"][index]["characterId"]
            game_obj["matchId"] = game["matchInfo"]["matchId"]

            # Grab kills
            game_kills = []
            roundResults = game["roundResults"]
            for round in roundResults:
                plant_time = (
                    round["plantRoundTime"] if "plantRoundTime" in round else sys.maxint
                )
                index = next(
                    (
                        i
                        for i, item in enumerate(round["playerStats"])
                        if item["subject"] == uid
                    ),
                    -1,
                )
                kills = round["playerStats"][index]["kills"]
                kills = [
                    kill
                    for kill in kills
                    if kill["finishingDamage"]["damageType"] != "Bomb"
                ]
                for kill in kills:
                    if kill["roundTime"] > plant_time:
                        kill["postPlant"] = True
                        kill["plantSite"] = round["plantSite"]
                    else:
                        kill["postPlant"] = False
                game_kills += kills

            game_obj["kills"] = game_kills
            games.append(game_obj)

    return render_template("kills.html", player_id=uid, kills=games)
