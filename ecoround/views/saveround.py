from flask import Flask, render_template, request

from ecoround import app, utils

import os
import sys
import json


@app.route("/user/<uid>/firstround")
def first_round(uid: str = ""):
    files = utils.get_files_by_uid(uid)
    for file_path in files:
        with open(file_path, "r") as file:
            game_data = json.load(file)
            if game_data["matchInfo"]["queueID"] == "deathmatch":
                continue

            player_team = utils.get_player_team(uid, game_data)
            first_round = game_data["roundResults"][0]

            team_won = first_round["winningTeam"] == player_team.value
            team_won_by = first_round["roundResult"]
            print(team_won)
    return "asdf"


@app.route("/user/<uid>/firstround")
def first_round(uid: str = ""):
    files = utils.get_files_by_uid(uid)
    for file_path in files:
        with open(file_path, "r") as file:
            game_data = json.load(file)
            if game_data["matchInfo"]["queueID"] != "competitive":
                continue

            player_team = utils.get_player_team(uid, game_data)
            first_round = game_data["roundResults"][0]
            second_round = game_data["roundResults"][1]

            team_won_first_round = first_round["winningTeam"] == player_team.value
            second_rounds_after_win = []
            if team_won_first_round:
                print("yay")

    return "asdf"
