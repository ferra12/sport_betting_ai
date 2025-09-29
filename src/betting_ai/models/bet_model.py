import pydantic


class Bet(pydantic.BaseModel):
    team1: str
    team2: str
    quote: float
    result: str
    date: str
    sport: str
    league: str
