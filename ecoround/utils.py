import os
from typing import List
from ecoround.models.game import TeamColor


def get_files_by_uid(uid: str) -> List[str]:
    path = os.path.dirname(os.path.abspath(__file__))

    return [
        os.path.join(f"{path}/../data/{uid}", file)
        for file in os.listdir(f"{path}/../data/{uid}")
    ]


def get_player_team(uid: str, game_data: dict) -> TeamColor:
    index = next(
        (i for i, item in enumerate(game_data["players"]) if item["subject"] == uid),
        -1,
    )
    return TeamColor(game_data["players"][index]["teamId"])
