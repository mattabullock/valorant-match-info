import os
import json
from ValorantAPI import ValorantAPI


def main():
    creds_file = open("credentials.json", "r")
    creds = json.load(creds_file)
    creds_file.close()

    api = ValorantAPI(creds["username"], creds["password"], "na")
    data = api.get_match_history()
    matchIDs = [obj["MatchID"] for obj in data["History"]]

    if not os.path.exists("data"):
        os.makedirs("data")

    user_folder = f"data/{api.user_info}"
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)

    for match_id in matchIDs:
        data_file = open(user_folder + "/" + match_id + ".json", "w")
        match_details = api.get_match_details(matchIDs[0])
        data_file.write(json.dumps(match_details))


if __name__ == "__main__":
    main()
