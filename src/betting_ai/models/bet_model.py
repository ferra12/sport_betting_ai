from typing import Optional

import pydantic


class Bet(pydantic.BaseModel):
    team1: str
    team2: str
    bet_option: str
    quote: float
    result: str
    date_place: str
    date_event: str
    sport: str
    league: str
    _expire_after: Optional[int]
