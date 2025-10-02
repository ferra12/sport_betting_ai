from typing import Literal, Optional

from pydantic import BaseModel


class Bet(BaseModel):
    team1: str
    team2: str
    bet_option: str
    bet_label: str
    quote: float
    result: Literal[-1, 0, 1]
    date_place: str
    date_event: str
    sport_id: int
    sport: str
    league_id: int
    league: str
    event_id: int
    expire_after: Optional[int]


class BetMap(BaseModel):
    sport_id: int
    bet_id: int
    bet_desc: str
    outcomes: list[str]
    outcomes_id: list[int]
    threshold: str
    expire_after: Optional[int]
