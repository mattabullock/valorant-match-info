import os
import sys
import time
import json

from sqlalchemy.orm import aliased

from ecoround.api.ValorantAPI import ValorantAPI
from ecoround.scripts import download, migrate
from ecoround import db, app
from ecoround.models.match import Round, Economy, Player, Match


def main():
    if len(sys.argv) == 1:
        print("Usage: main.py command [uid]")

    player_id = (
        sys.argv[2] if len(sys.argv) == 3 else "b2736519-f52f-52df-8542-aa07679b7d8f"
    )

    if sys.argv[1] == "migrate":
        migrate.migrate(player_id)
    if sys.argv[1] == "get_latest":
        creds_file = open("credentials.json", "r")
        creds = json.load(creds_file)
        creds_file.close()

        api = ValorantAPI(
            creds["valorant"]["username"], creds["valorant"]["password"], "na"
        )
        download.get_latest_match(api, player_id)
    if sys.argv[1] == "download":
        creds_file = open("credentials.json", "r")
        creds = json.load(creds_file)
        creds_file.close()

        api = ValorantAPI(
            creds["valorant"]["username"], creds["valorant"]["password"], "na"
        )
        download.download_match_history(api, player_id)
    if sys.argv[1] == "mmr":
        creds_file = open("credentials.json", "r")
        creds = json.load(creds_file)
        creds_file.close()

        api = ValorantAPI(
            creds["valorant"]["username"], creds["valorant"]["password"], "na"
        )
        print(
            json.dumps(
                api.get_competitive_match_history(player_id),
                indent=4,
            )
        )
    if sys.argv[1] == "get_content":
        creds_file = open("credentials.json", "r")
        creds = json.load(creds_file)
        creds_file.close()

        api = ValorantAPI(
            creds["valorant"]["username"], creds["valorant"]["password"], "na"
        )
        download.get_content(api)

    if sys.argv[1] == "get_match_history":
        creds_file = open("credentials.json", "r")
        creds = json.load(creds_file)
        creds_file.close()

        api = ValorantAPI(
            creds["valorant"]["username"], creds["valorant"]["password"], "na"
        )
        print(json.dumps(api.get_match_history(player_id), indent=4))
    if sys.argv[1] == "test_query":
        with app.app_context():
            specific_player = aliased(Player)
            other_player = aliased(Player)
            economies = (
                Economy.query.join(Economy.round)
                .join(Round.match)
                .join(other_player)
                .join(
                    specific_player,
                    specific_player.account_id
                    == "b2736519-f52f-52df-8542-aa07679b7d8f",
                )
                .filter(
                    (Match.queue_id == "competitive")
                    & Round.round_num.in_([0])
                    & (other_player.team_id == specific_player.team_id)
                )
            )
            for economy in economies:
                print(
                    f"{economy.player.account.game_name}#{economy.player.account.tag_line} spent {economy.spent} in round {economy.round.round_num} of {economy.player.match.match_id}"
                )


if __name__ == "__main__":
    main()
