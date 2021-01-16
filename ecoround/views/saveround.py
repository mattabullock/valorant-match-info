from flask import Flask, render_template, request

from ecoround import app, utils

import os
import sys
import json


@app.route("/user/<uid>/secondround")
def second_round(uid: str = ""):
    files = utils.get_files_by_uid(uid)
    second_rounds_after_win = []
    for file_path in files:
        with open(file_path, "r") as file:
            game_data = json.load(file)
            if game_data["matchInfo"]["queueID"] != "competitive":
                continue

            player_team = utils.get_player_team(uid, game_data)
            first_round = game_data["roundResults"][0]
            second_round = game_data["roundResults"][1]

            team_won_first_round = first_round["winningTeam"] == player_team
            if team_won_first_round:
                second_rounds_after_win.append(second_round)

    return "asdf"
