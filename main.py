import os
import sys
import time
import json
from ecoround.api.ValorantAPI import ValorantAPI


def main():
    player_id = "a8192f46-4bba-5fa7-994d-f9c95055f3e1"
    creds_file = open("credentials.json", "r")
    creds = json.load(creds_file)
    creds_file.close()

    api = ValorantAPI(creds["username"], creds["password"], "na")
    # download_match_history(api, player_id, 1)
    # get_latest_match(api, player_id)
    print(api.get_competitive_match_history("1059a895-5eb7-543c-93de-f1cf1204311b"))


def get_latest_match(api, user_id):
    print("Downloading latest match for {user_id}")
    if not os.path.exists("temp"):
        os.makedirs("temp")
    data = api.get_match_history()
    match_id = data["History"][0]["MatchID"]
    match_file_path = f"temp/{match_id}.json"
    match_details = api.get_match_details(match_id)
    data_file = open(match_file_path, "w")
    data_file.write(json.dumps(match_details))
    data_file.close()


def download_match_history(api, user_id, depth=0):
    print(f"Downloading history for {user_id}")
    players = set()

    start_index = 0
    end_index = 20
    total_games = sys.maxsize

    if not os.path.exists("data"):
        os.makedirs("data")

    user_folder = f"data/{user_id}"

    if not os.path.exists(user_folder):
        os.makedirs(user_folder)

    while start_index < total_games:
        data = api.get_match_history(user_id, start_index, end_index)
        if total_games == sys.maxsize:
            total_games = data["Total"]
        matchIDs = [obj["MatchID"] for obj in data["History"]]

        for match_id in matchIDs:
            match_file_path = f"{user_folder}/{match_id}.json"
            if not os.path.exists(match_file_path):
                while True:
                    match_details = api.get_match_details(match_id)
                    time.sleep(1)
                    if match_details:
                        break
                    print(f"Retrying id: {match_id}")

                data_file = open(match_file_path, "w")
                data_file.write(json.dumps(match_details))
                data_file.close()

                for player in match_details["players"]:
                    players.add(player["subject"])
            else:
                data_file = open(match_file_path, "r")
                match_details = json.load(data_file)
                for player in match_details["players"]:
                    players.add(player["subject"])

        if len(matchIDs) < 20:
            break

        start_index = end_index
        end_index = start_index + 20

    if depth > 0:
        for player_id in players:
            download_match_history(api, player_id, depth - 1)


if __name__ == "__main__":
    main()
