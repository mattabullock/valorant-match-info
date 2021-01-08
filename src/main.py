import os
import sys
import json
from ValorantAPI import ValorantAPI


def main():
    creds_file = open("credentials.json", "r")
    creds = json.load(creds_file)
    creds_file.close()

    api = ValorantAPI(creds["username"], creds["password"], "na")

    start_index = 0
    end_index = 20
    total_games = sys.maxsize

    if not os.path.exists("data"):
        os.makedirs("data")

    user_folder = f"data/{api.user_info}"

    if not os.path.exists(user_folder):
        os.makedirs(user_folder)

    while start_index < total_games:
        data = api.get_match_history(start_index, end_index)
        if total_games == sys.maxsize:
            total_games = data["Total"]
        matchIDs = [obj["MatchID"] for obj in data["History"]]

        for match_id in matchIDs:
            match_file_path = f"{user_folder}/{match_id}.json"
            if not os.path.exists(match_file_path):
                data_file = open(match_file_path, "w")
                match_details = api.get_match_details(match_id)
                data_file.write(json.dumps(match_details))

        if len(matchIDs) < 20:
            break

        start_index = end_index
        end_index = start_index + 20


if __name__ == "__main__":
    main()
