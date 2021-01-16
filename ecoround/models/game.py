from enum import Enum
from typing import List
from pydantic import BaseModel


class TeamColor(str, Enum):
    Red = "Red"
    Blue = "Blue"


class Player(BaseModel):
    id: str
    name: str
    tagLine: str
    characterId: str
    competitiveTier: int


class Team(BaseModel):
    color: TeamColor
    players: List[Player]
    player_ids: List[str]
