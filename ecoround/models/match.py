from flask_sqlalchemy import SQLAlchemy

from ecoround import db


class Match(db.Model):
    __tablename__ = "match"

    match_id = db.Column(db.String(40), nullable=False, primary_key=True)
    map_id = db.Column(db.String(50), nullable=False)
    game_version = db.Column(db.String(40), nullable=False)
    game_pod_id = db.Column(db.String(60), nullable=False)
    game_length_millis = db.Column(db.Integer, nullable=False)
    game_start_millis = db.Column(db.BigInteger, nullable=False)
    queue_id = db.Column(db.String(20), nullable=False)
    is_ranked = db.Column(db.Boolean(), nullable=False)
    season_id = db.Column(db.String(40), nullable=False)
    completion_state = db.Column(db.String(20), nullable=False)

    players = db.relationship("Player", backref="match", lazy=True)
    rounds = db.relationship("Round", backref="match", lazy=True)
    events = db.relationship("Event", backref="match", lazy=True)
    economies = db.relationship("Economy", backref="match", lazy=True)

    def __init__(
        self,
        match_id,
        map_id,
        game_version,
        game_pod_id,
        game_length_millis,
        game_start_millis,
        queue_id,
        is_ranked,
        season_id,
        completion_state,
    ):
        self.match_id = match_id
        self.map_id = map_id
        self.game_version = game_version
        self.game_pod_id = game_pod_id
        self.game_length_millis = game_length_millis
        self.game_start_millis = game_start_millis
        self.queue_id = queue_id
        self.is_ranked = is_ranked
        self.season_id = season_id
        self.completion_state = completion_state


class Player(db.Model):
    __tablename__ = "player"
    __table_args__ = (db.UniqueConstraint("player_id", "match_id"),)

    player_id = db.Column(db.String(40), nullable=False, primary_key=True)
    match_id = db.Column(db.String(40), db.ForeignKey("match.match_id"), nullable=False)
    team_id = db.Column(db.String(40), nullable=False)
    party_id = db.Column(db.String(40), nullable=False)
    character_id = db.Column(db.String(40), nullable=False)
    player_card = db.Column(db.String(40), nullable=False)
    player_title = db.Column(db.String(40), nullable=False)
    kills = db.Column(db.Integer(), nullable=False)
    deaths = db.Column(db.Integer(), nullable=False)
    assists = db.Column(db.Integer(), nullable=False)
    rounds_played = db.Column(db.Integer(), nullable=False)
    score = db.Column(db.Integer(), nullable=False)

    def __init__(
        self,
        player_id,
        match_id,
        team_id,
        party_id,
        character_id,
        player_card,
        player_title,
        kills,
        deaths,
        assists,
        rounds_played,
        score,
    ):
        self.player_id = player_id
        self.match_id = match_id
        self.team_id = team_id
        self.party_id = party_id
        self.character_id = character_id
        self.player_card = player_card
        self.player_title = player_title
        self.kills = kills
        self.deaths = deaths
        self.assists = assists
        self.rounds_played = rounds_played
        self.score = score


class Round(db.Model):
    __tablename__ = "round"
    __table_args__ = (db.UniqueConstraint("round_num", "match_id"),)

    round_id = db.Column(db.BigInteger(), autoincrement=True, primary_key=True)
    match_id = db.Column(db.String(40), db.ForeignKey("match.match_id"), nullable=False)
    round_num = db.Column(db.Integer(), nullable=False)
    winning_team = db.Column(db.String(40), nullable=False)
    round_result_code = db.Column(db.String(40), nullable=False)
    round_ceremony = db.Column(db.String(40), nullable=False)
    events = db.relationship("Event", backref="round", lazy=True)
    economies = db.relationship("Economy", backref="round", lazy=True)

    def __init__(
        self,
        round_id,
        match_id,
        round_num,
        winning_team,
        round_result_code,
        round_ceremony,
    ):
        self.round_id = round_id
        self.match_id = match_id
        self.round_num = round_num
        self.winning_team = winning_team
        self.round_result_code = round_result_code
        self.round_ceremony = round_ceremony


class Event(db.Model):
    __tablename__ = "event"
    __table_args__ = (
        db.UniqueConstraint("round_id", "match_id", "round_time", "victim_id"),
    )

    event_id = db.Column(db.BigInteger(), autoincrement=True, primary_key=True)
    match_id = db.Column(db.String(40), db.ForeignKey("match.match_id"), nullable=False)
    round_id = db.Column(
        db.BigInteger(), db.ForeignKey("round.round_id"), nullable=False
    )
    player_id = db.Column(
        db.String(40), db.ForeignKey("player.player_id"), nullable=False
    )
    type = db.Column(db.String(20), nullable=False)
    victim_id = db.Column(db.String(40), db.ForeignKey("player.player_id"))
    round_time = db.Column(db.Integer(), nullable=False)
    location_x = db.Column(db.Integer(), nullable=False)
    location_y = db.Column(db.Integer(), nullable=False)
    finishing_damage_type = db.Column(db.String(40))
    finishing_damage_item = db.Column(db.String(40))
    plant_site = db.Column(db.String(1))

    def __init__(
        self,
        event_id,
        match_id,
        round_id,
        player_id,
        type,
        round_time,
        location_x,
        location_y,
        victim_id=None,
        finishing_damage_type=None,
        finishing_damage_item=None,
        plant_site=None,
    ):
        self.event_id = event_id
        self.match_id = match_id
        self.round_id = round_id
        self.player_id = player_id
        self.type = type
        self.victim_id = victim_id
        self.round_time = round_time
        self.location_x = location_x
        self.location_y = location_y
        self.finishing_damage_type = finishing_damage_type
        self.finishing_damage_item = finishing_damage_item
        self.plant_site = plant_site


class Economy(db.Model):
    __tablename__ = "economy"
    __table_args__ = (db.UniqueConstraint("match_id", "round_id", "player_id"),)

    economy_id = db.Column(db.BigInteger(), autoincrement=True, primary_key=True)
    match_id = db.Column(db.String(40), db.ForeignKey("match.match_id"), nullable=False)
    round_id = db.Column(
        db.BigInteger(), db.ForeignKey("round.round_id"), nullable=False
    )
    player_id = db.Column(
        db.String(40), db.ForeignKey("player.player_id"), nullable=False
    )
    loadout_value = db.Column(db.Integer(), nullable=False)
    spent = db.Column(db.Integer(), nullable=False)
    remaining = db.Column(db.Integer(), nullable=False)
    weapon_id = db.Column(db.String(40))
    armor_id = db.Column(db.String(40))

    def __init__(
        self,
        economy_id,
        match_id,
        round_id,
        player_id,
        loadout_value,
        spent,
        remaining,
        weapon_id=None,
        armor_id=None,
    ):
        self.economy_id = economy_id
        self.match_id = match_id
        self.round_id = round_id
        self.player_id = player_id
        self.loadout_value = loadout_value
        self.spent = spent
        self.remaining = remaining
        self.weapon_id = weapon_id
        self.armor_id = armor_id


class Damage(db.Model):
    __tablename__ = "damage"
    __table_args__ = (
        db.UniqueConstraint("match_id", "round_id", "player_id", "victim_id"),
    )

    damage_id = db.Column(db.BigInteger(), autoincrement=True, primary_key=True)
    match_id = db.Column(db.String(40), db.ForeignKey("match.match_id"), nullable=False)
    round_id = db.Column(
        db.BigInteger(), db.ForeignKey("round.round_id"), nullable=False
    )
    player_id = db.Column(
        db.String(40), db.ForeignKey("player.player_id"), nullable=False
    )
    victim_id = db.Column(
        db.String(40), db.ForeignKey("player.player_id"), nullable=False
    )
    event_id = db.Column(db.BigInteger(), db.ForeignKey("event.event_id"))
    damage = db.Column(db.SmallInteger(), nullable=False)
    headshots = db.Column(db.SmallInteger(), nullable=False)
    bodyshots = db.Column(db.SmallInteger(), nullable=False)
    legshots = db.Column(db.SmallInteger(), nullable=False)

    def __init__(
        self,
        damage_id,
        round_id,
        player_id,
        victim_id,
        damage,
        headshots,
        bodyshots,
        legshots,
        event_id=None,
    ):
        self.damage_id = damage_id
        self.match_id = match_id
        self.round_id = round_id
        self.player_id = player_id
        self.victim_id = victim_id
        self.event_id = event_id
        self.damage = damage
        self.headshots = headshots
        self.bodyshots = bodyshots
        self.legshots = legshots


"""
class Weapon(db.Model):
    __tablename__ = "weapon"


class Armor(db.Model):
    __tablename__ = "armor"


class Character(db.Model):
    __tablename__ = "character"
"""
