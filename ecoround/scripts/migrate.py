import json

from ecoround.utils import get_files_by_uid
from ecoround.models.match import Match
from ecoround import db, app


def migrate(player_id: str):
    files = get_files_by_uid(player_id)

    for file_path in files:
        with open(file_path, "r") as game_file:
            match_info = json.load(game_file)["matchInfo"]
            match = Match(
                match_id=match_info["matchId"],
                map_id=match_info["mapId"],
                game_version=match_info["gameVersion"],
                game_pod_id=match_info["gamePodId"],
                game_length_millis=match_info["gameLengthMillis"],
                game_start_millis=match_info["gameStartMillis"],
                queue_id=match_info["queueID"],
                is_ranked=match_info["isRanked"],
                season_id=match_info["seasonId"],
                completion_state=match_info["completionState"],
            )
            with app.app_context():
                db.session.add(match)
                db.session.commit()
