from pymongo import MongoClient
from pymongo.errors import PyMongoError

from ..utils.logging import logger


class MongoConnection:
    """Gestisce una sola connessione condivisa (singleton)."""

    _client = None

    @classmethod
    def get_client(cls, uri: str):
        if cls._client is None:
            cls._client = MongoClient(uri)
            logger.debug("Connessione MongoDB inizializzata")
        return cls._client


class MongoDBManager:
    """Gestore di una specifica collezione."""

    def __init__(self, uri: str, db_name: str, collection_name: str):
        client = MongoConnection.get_client(uri)
        self._db = client[db_name]
        self._collection = self._db[collection_name]
        logger.debug(
            f"""MongoDBManager collegato al database '{db_name}',
            collezione '{collection_name}'"""
        )

    def find(self, query: dict, limit: int = 0):
        """
        Esegue una query sulla collezione specificata e
        restituisce i risultati.

        Parametri:
            query (dict): Filtro della query.
            limit (int, opzionale): Numero massimo di
                risultati da restituire.

        Ritorna:
            list: Risultato della query.
        """
        cursor = self._collection.find(query)
        if limit > 0:
            cursor = cursor.limit(limit)
        return list(cursor)

    def find_one(self, query: dict):
        """
        Esegue una query sulla collezione specificata e
        restituisce il primo risultato trovato.

        Parametri:
            query (dict): Filtro della query.

        Ritorna:
            dict: Il primo documento trovato,
                o None se non esiste.
        """
        return self._collection.find_one(query)

    def insert(self, data: list):
        """
        Inserisce molti elementi nella collezione specificata.

        Parametri:
            data (list): Lista di documenti da inserire.

        Ritorna:
            InsertManyResult: Risultato dell'inserimento.
        """
        return self._collection.insert_many(data)

    def insert_one(self, data: dict):
        """
        Inserisce un singolo elemento nella collezione specificata.

        Parametri:
            data (dict): Dati dell'elemento da inserire.

        Ritorna:
            InsertOneResult: Risultato dell'inserimento.
        """
        return self._collection.insert_one(data)

    def delete_by_query(self, query: dict, many: bool = False) -> int:
        """
        Elimina elementi dalla collezione specificata
        sulla base di un filtro di query.

        Parametri:
            query (dict): Filtro della query.
            many (bool, opzionale): Se True, elimina
                tutti gli elementi corrispondenti.
                Se False, elimina solo il primo elemento corrispondente.

        Ritorna:
            int: Numero di elementi eliminati.
        """
        try:
            if many:
                result = self._collection.delete_many(query)
            else:
                result = self._collection.delete_one(query)
            return result.deleted_count
        except PyMongoError as e:
            logger.error(f"Errore durante l'eliminazione: {e}")
            return 0
