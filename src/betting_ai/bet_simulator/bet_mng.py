from ..conn.mongo_conn import MongoDBManager
from ..models.bet_model import Bet
from ..utils.config import config


class BetManager:
    def __init__(self):
        self.conn = MongoDBManager(
            config.mongodb_uri, config.mongodb_db_name, config.mongodb_bet_collection
        )

    def place_bet(self, bet: Bet):
        """Carica una nuova scommessa sul database."""
        self.conn.insert_one(bet)

    def cancel_bet(self):
        pass
