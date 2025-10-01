import requests  # type: ignore[import]

from ..utils.logging import logger


class SisalScraper:
    def __init__(self):
        self.headers = {
            "Accept": "*/*",
            "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection": "keep-alive",
            "Origin": "https://www.sisal.it",
            "Referer": "https://www.sisal.it/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            + "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124",'
            + ' "Not-A.Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "user_data": '{"accountId":null,"token":null,"tokenJWT":null,"locale":'
            + '"it_IT","loggedIn":false,"channel":62,"brandId":175,"offerId":0}',
        }
        self.params = {
            "offerId": 0,
        }
        base_url = (
            "https://betting.sisal.it/api/lettura-palinsesto-sport/"
            + "palinsesto/prematch/"
        )
        self.uri_league = base_url + "schedaManifestazione/0/{sport_id}-{league_id}"
        self.uri_tree = base_url + "alberaturaPrematch"
        self.uri_match = base_url + "schedaAvvenimento/{schedule_id}-{event_id}"

    def get_bookmaker_map(self):
        response = requests.get(self.uri_tree, headers=self.headers)
        if response.status_code != 200:
            logger.warning("Error getting bookmaker map")
            return None
        data = response.json()
        return data

    def get_league_quotes(self, sport_id, league_id):
        response = requests.get(
            self.uri_league.format(sport_id=sport_id, league_id=league_id),
            params=self.params,
            headers=self.headers,
        )
        if response.status_code != 200:
            logger.warning(
                f"Error getting quotes for sport {sport_id} league {league_id}"
            )
            return None
        data = response.json()
        return data

    def get_match_quotes(self, schedule_id, event_id):
        response = requests.get(
            self.uri_match.format(schedule_id=schedule_id, event_id=event_id),
            params=self.params,
            headers=self.headers,
        )
        if response.status_code != 200:
            logger.warning(f"Error getting quotes for event {event_id}")
            return None
        data = response.json()
        return data

    def get_unique_events(self, league_quotes: dict) -> set[str]:
        quote_map = league_quotes.get("scommessaMap", league_quotes)
        return {
            "-".join(key.split("-", 2)[:2])  # split max 2 pezzi, poi prendo i primi due
            for key in quote_map
        }

    def get_clean_bets(self, match_quotes: dict) -> list[dict]:
        bets = match_quotes.get("infoAggiuntivaMap", match_quotes)
        quote_map = match_quotes.get("scommessaMap", match_quotes)
        first_value = next(iter(quote_map.values()))
        sport_id = first_value["codiceManifestazione"]
        clean_bets = []
        for bet in bets.values():
            temp = {}
            temp["sport_id"] = sport_id
            temp["bet_id"] = bet["codiceScommessa"]
            temp["bet_desc"] = bet["descrizione"]
            temp["threshold"] = bet["soglia"]
            temp["outcomes"] = [outcome["descrizione"] for outcome in bet["esitoList"]]
            temp["outcomes_id"] = [
                outcome["codiceEsito"] for outcome in bet["esitoList"]
            ]
            clean_bets.append(temp)
        return clean_bets
