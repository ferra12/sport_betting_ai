from typing import Literal, Optional, overload

from ..conn.mongo_conn import MongoDBManager
from ..models.bet_model import Bet
from ..utils.config import config
from ..utils.logging import logger


class BetManager:
    def __init__(self, test=False):
        db_name = config.mongo_db_name
        bet_collection = (
            "test_" + config.mongo_bet_collection
            if test
            else config.mongo_bet_collection
        )
        old_bet_collection = (
            "test_" + config.mongo_old_bet_collection
            if test
            else config.mongo_old_bet_collection
        )

        self.bet_conn = MongoDBManager(config.mongo_uri, db_name, bet_collection)
        self.old_bet_conn = MongoDBManager(
            config.mongo_uri, db_name, old_bet_collection
        )

    def place_bet(self, bet: Bet):
        """Carica una nuova scommessa sul database."""
        try:
            self.bet_conn.insert_one(bet.model_dump(by_alias=True))
            return True
        except Exception as e:
            logger.error(
                f"Errore place_bet per {bet.team1} vs {bet.team2} "
                f"({bet.sport}/{bet.league}, {bet.date_event}) → {e}"
            )
            return False

    @overload
    def find_bet(self, query: dict, many: Literal[True]) -> list[dict]: ...
    @overload
    def find_bet(self, query: dict, many: Literal[False] = False) -> Optional[dict]: ...

    def find_bet(self, query: dict, many: bool = False):
        """Esegue una query sulla collezione delle scommesse."""
        if many:
            return self.bet_conn.find(query, many)
        else:
            return self.bet_conn.find_one(query)

    def delete_bet(self, bet_id) -> bool:
        try:
            self.bet_conn.delete_by_query({"_id": bet_id})
            return True
        except Exception as e:
            logger.error(f"Errore delete_bet {bet_id}: {e}")
            return False

    def move_old_bets(self, bet: Bet) -> bool:
        try:
            query = bet.model_dump(by_alias=True)
            query.pop("_id", None)
            bet_return = self.find_bet(query, many=False)
            if bet_return:
                self.delete_bet(bet_return["_id"])
                self.old_bet_conn.insert_one(bet.model_dump(by_alias=True))
            return True
        except Exception as e:
            logger.error(f"Errore move_old_bets {bet}: {e}")
            return False
