from flask import Flask, render_template, request

from ecoround import app, utils
from ecoround.models.match import Round

import os
import sys
import json


@app.route("/user/<uid>/secondround")
def second_round(uid: str = ""):
    files = utils.get_files_by_uid(uid)
    second_rounds_after_win = []
    rounds = Round.query.filter(Round.round_num.in_([0, 1]))
    for round in rounds:
        print(round.economies)

    return "asdf"
