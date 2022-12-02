from datetime import datetime
from typing import List, TypedDict

# constants

position_dict = {'1': "GK", '2': "DEF", '3': "MID", '4': "FWD"}

# ------------------------------
# player classes
# ------------------------------

class PlayerIndex(TypedDict):
    value: float
    rank: int
    postion_rank: int


class PlayerIndexes(TypedDict):
    ict: PlayerIndex
    influence: PlayerIndex
    creativity: PlayerIndex
    threat: PlayerIndex

# alternative format to allow use of 'in'
class PlayerTransferStats: TypedDict('PlayerTransferStats', {
    'balance': int,
    'in': int,
    'out': int
})


class PlayerTransfers(TypedDict):
    total: PlayerTransferStats
    current: PlayerTransferStats
    history: List[PlayerTransferStats]


class PlayerStats(TypedDict):
    minutes: int
    goals: int
    assists: int
    clean_sheets: int
    conceeded: int
    own_goals: int
    penalties_saved: int
    penalties_missed: int
    yellow_cards: int
    red_cards: int
    saves: int
    points: int
    bonus: int
    bps: int

class Player(TypedDict):
    id: int
    code: int
    first_name: str
    last_name: str
    display_name: str
    position: int
    team: int
    price: int
    stats: PlayerStats
    transfers: PlayerTransfers
    indexes: PlayerIndexes

class Players:
    """"""

    def __init__(self) -> None:
        pass

# ------------------------------
# player summary classes
# ------------------------------

class PlayerFixture(TypedDict):
    id: int
    code: int
    gameweek: int
    kickoff: datetime
    kickoff_finalized: bool
    finished: bool
    home: bool
    stats: PlayerStats

class PlayerSeason(TypedDict):
    name: str
    stats: PlayerStats
    indexes: PlayerIndexes

class PlayerSummary(TypedDict):
    fixtures: List[PlayerFixture]
    seasons: List[PlayerSeason]

# ------------------------------
# position classes
# ------------------------------

class PositionDetails(TypedDict):
    id: int
    name: str
    name_short: str
    select: int
    min_play: int
    max_play: int

# ------------------------------
# private methods
# ------------------------------

def _format_stats(element) -> PlayerStats:
    return {
        "minutes": element["minutes"],
        "goals": element["goals_scored"],
        "assists": element["assists"],
        "clean_sheets": element["clean_sheets"],
        "conceded": element["goals_conceded"],
        "own_goals": element["own_goals"],
        "penalties_saved": element["penalties_saved"],
        "penalties_missed": element["penalties_missed"],
        "saves": element["saves"],
        "yellow_cards": element["yellow_cards"],
        "red_cards": element["red_cards"],
        "points": element["total_points"],
        "bonus": element["bonus"],
        "bps": element["bps"]
    }

def _format_index(element, name) -> PlayerIndex:
    return {
        "value": float(element[f"{name}"]),
        "rank": element[f"{name}_rank"],
        "position_rank": element[f"{name}_rank_type"]
    }

def _format_indexes(element) -> PlayerIndexes:
    return {
        "ict": _format_index(element, "ict_index"),
        "influence": _format_index(element, "influence"),
        "creativity": _format_index(element, "creativity"),
        "threat": _format_index(element, "threat"),
    }

def _format_player(element) -> Player:
    return {
        "id": element["id"],
        "code": element["code"],
        "first_name": element["first_name"],
        "second_name": element["second_name"],
        "display_name": element["web_name"],
        "position": position_dict[element["element_type"]],
        "team": element["team"],
        "price": element["now_cost"],
        "selected": float(element["selected_by_percent"]),
        "stats": _format_stats(element),
        "indexes": _format_indexes(element),
        "transfers": {
            "total": {
                "balance": (element["transfers_in"] - element["transfers_out"]),
                "in": element["transfers_in"],
                "out": element["transfers_out"]
            },
            "current": {
                "balance": (element["transfers_in_event"] - element["transfers_out_event"]),
                "in": element["transfers_in_event"],
                "out": element["transfers_out_event"]
            }
        },

    }


def _format_player_fixture(fixture):
    pass

def _format_player_season(season):
    return {
        "name": season["season_name"],
        "price": {
            "start": season["start_cost"],
            "end": season["end_cost"],
            "change": (season["end_cost"] - season["start_cost"])
        },
        "stats": _format_stats(season)
    }

def _format_player_summary(summary):
    return {
        "gameweeks": [],
        "seasons": [_format_player_season(s) for s in summary["history_past"]]
    }

# ------------------------------
# public methods
# ------------------------------

def players(self, ids: List[int] = None, summary: bool = False) -> List[Player]:
    if ids: return [p for p in self.static.players if p["id"] in ids]
    return self.static.players

def player(self, id: int, summary: bool = False) -> Player:
    return next((p for p in self.static.players if p["id"] == id), None)

def position(self, id: int) -> int:
    return next((p["position"] for p in self.static.players if p["id"] == id), None)
