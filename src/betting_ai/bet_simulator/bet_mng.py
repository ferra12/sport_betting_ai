from ..conn.mongo_conn import MongoDBManager
from ..models.bet_model import Bet
from ..utils.config import config
from ..utils.logging import logger


class BetManager:
    def __init__(self):
        self.bet_conn = MongoDBManager(
            config.mongodb_uri, config.mongodb_db_name, config.mongodb_bet_collection
        )
        self.old_bet_conn = MongoDBManager(
            config.mongodb_uri,
            config.mongodb_db_name,
            config.mongodb_old_bet_collection,
        )

    def place_bet(self, bet: Bet):
        """Carica una nuova scommessa sul database."""
        try:
            self.bet_conn.insert_one(bet.model_dump())
            return True
        except Exception as e:
            logger.error(f"Errore place_bet {bet}: {e}")
            return False

    def find_bet(self, query: dict, many: bool = False):
        """Esegue una query sulla collezione delle scommesse."""
        if many:
            return self.bet_conn.find(query, many)
        else:
            return self.bet_conn.find_one(query)

    def move_old_bets(self, bet: Bet):
        bet_return = self.find_bet(
            {
                "team1": bet.team1,
                "team2": bet.team2,
                "sport": bet.sport,
                "league": bet.league,
                "date_event": bet.date_event,
                "date_place": bet.date_place,
            },
            many=False,
        )
        if bet_return:
            self.bet_conn.delete_by_query({"_id": bet_return["_id"]})
            self.old_bet_conn.insert_one(bet.model_dump())
