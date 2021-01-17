import json
import sqlalchemy

from ecoround.utils import get_files_by_uid
from ecoround.models.match import Match, Player, Round, Economy, Account
from ecoround import db, app


def migrate(player_id: str):
    files = get_files_by_uid(player_id)

    with app.app_context():
        for file_path in files:
            with open(file_path, "r") as game_file:
                game_data = json.load(game_file)
                match_info = game_data["matchInfo"]
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
                db.session.merge(match)

                players = {}
                for game_player in game_data["players"]:
                    account = Account(
                        account_id=game_player["subject"],
                        game_name=game_player["gameName"],
                        tag_line=game_player["tagLine"],
                    )
                    player = Player(
                        account_id=game_player["subject"],
                        match_id=match_info["matchId"],
                        team_id=game_player["teamId"],
                        party_id=game_player["partyId"],
                        character_id=game_player["characterId"],
                        player_card=game_player["playerCard"],
                        player_title=game_player["playerTitle"],
                        kills=game_player["stats"]["kills"],
                        deaths=game_player["stats"]["deaths"],
                        assists=game_player["stats"]["assists"],
                        rounds_played=game_player["stats"]["roundsPlayed"],
                        score=game_player["stats"]["score"],
                    )
                    db.session.merge(account)
                    db.session.add(player)
                    db.session.flush()
                    players[player.account_id] = player.player_id

                for game_round in game_data["roundResults"]:
                    round = Round(
                        match_id=match_info["matchId"],
                        round_num=game_round["roundNum"],
                        winning_team=game_round["winningTeam"],
                        round_result_code=game_round["roundResultCode"],
                        round_ceremony=game_round["roundCeremony"],
                    )
                    db.session.add(round)
                    db.session.flush()
                    for game_player in game_round["playerStats"]:
                        economy = Economy(
                            match_id=match_info["matchId"],
                            round_id=round.round_id,
                            player_id=players[game_player["subject"]],
                            loadout_value=game_player["economy"]["loadoutValue"],
                            spent=game_player["economy"]["spent"],
                            remaining=game_player["economy"]["remaining"],
                            weapon_id=game_player["economy"]["weapon"],
                            armor_id=game_player["economy"]["armor"],
                        )
                    db.session.merge(economy)
            db.session.commit()
