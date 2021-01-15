from enum import Enum
from pydantic import BaseClass


class Team(BaseClass):
    color: TeamColor
    players: List[Player]
    player_ids: List[str]


class TeamColor(str, Enum):
    Red = "Red"
    Blue = "Blue"


class Player(BaseClass):
    id: str
    name: str
    tagLine: str
    characterId: str
    competitiveTier: int
