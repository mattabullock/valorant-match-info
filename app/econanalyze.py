import json
import os
from os.path import join


def main():
    thrifty_count = 0
    thrifty_mode_dict = {}
    largest_lower_loadout_value = 0
    largest_lower_spend = 0
    for root, _, files in os.walk("data"):
        for filename in files:
            file_path = join(root, filename)

            match_file = open(
                file_path,
                "r",
            )

            data = json.load(match_file)
            red_team_ids = []
            blue_team_ids = []
            for player in data["players"]:
                if player["teamId"] == "Blue":
                    blue_team_ids.append(player["subject"])
                if player["teamId"] == "Red":
                    red_team_ids.append(player["subject"])

            thrifty_rounds = []
            for round in data["roundResults"]:
                red_team_econ = []
                blue_team_econ = []
                if round["roundCeremony"] == "CeremonyThrifty":
                    # print(f"Round Number: {round['roundNum']}")
                    if round["roundNum"] not in thrifty_mode_dict.keys():
                        thrifty_mode_dict[round["roundNum"]] = 1
                    else:
                        thrifty_mode_dict[round["roundNum"]] += 1

                    for player in round["playerStats"]:
                        if player["subject"] in red_team_ids:
                            red_team_econ.append(player["economy"])
                        if player["subject"] in blue_team_ids:
                            blue_team_econ.append(player["economy"])

                    blue_team_spent = 0
                    blue_team_loadout_value = 0
                    red_team_spent = 0
                    red_team_loadout_value = 0
                    for econ in red_team_econ:
                        red_team_spent += econ["spent"]
                        red_team_loadout_value += econ["loadoutValue"]

                    for econ in blue_team_econ:
                        blue_team_spent += econ["spent"]
                        blue_team_loadout_value += econ["loadoutValue"]

                    if (
                        min(blue_team_loadout_value, red_team_loadout_value)
                        > largest_lower_loadout_value
                    ):
                        largest_lower_loadout_value = min(
                            blue_team_loadout_value, red_team_loadout_value
                        )
                        loadout_value_file = file_path
                        loadout_value_round = round["roundNum"]

                    if min(blue_team_spent, red_team_spent) > largest_lower_spend:
                        largest_lower_spend = min(blue_team_spent, red_team_spent)
                        spend_file = file_path
                        spend_round = round["roundNum"]

                    # print(f"Blue Team Spent: {blue_team_spent}")
                    # print(f"Blue Team Loadout Value: {blue_team_loadout_value}")

                    # print(f"Red Team Spent: {red_team_spent}")
                    # print(f"Red Team Loadout Value: {red_team_loadout_value}")
                    # print("-------")
                    thrifty_count += 1
    print(f"Thrifty rounds analyzed: {thrifty_count}")
    print(f"Largest thrifty loadout value: {largest_lower_loadout_value}")
    print(f"{loadout_value_file} - round {loadout_value_round}")
    print(f"Largest thrifty spend: {largest_lower_spend}")
    print(f"{spend_file} - round {spend_round}")
    print(f"Thrifty rounds analyzed: {json.dumps(thrifty_mode_dict, indent=1)}")


if __name__ == "__main__":
    main()
