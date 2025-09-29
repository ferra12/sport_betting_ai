import pydantic


class Bet(pydantic.BaseModel):
    team1: str
    team2: str
    quote: float
    result: str
    date_place: str
    date_event: str
    sport: str
    league: str
