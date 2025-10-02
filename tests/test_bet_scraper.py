import json

import pytest

from betting_ai.bet_scraper.bet_scraper import BetScraper


@pytest.mark.parametrize("save_to_file", [True, False])
def test_get_bookmaker_map_integration(save_to_file):
    """Test reale che interroga l'API Sisal e opzionalmente salva i dati su file."""
    scraper = BetScraper()
    data = scraper.get_bookmaker_map()

    # Controlliamo che sia arrivato un dict valido
    assert data is not None
    assert isinstance(data, dict)

    # Queste chiavi dovrebbero essere sempre presenti nella risposta Sisal
    assert "disciplinaMap" in data
    assert "manifestazioneMap" in data

    if save_to_file:
        out_file = "tests/data/bookmaker_map.json"
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        # ricontrollo che il file sia coerente
        with open(out_file, "r", encoding="utf-8") as f:
            saved = json.load(f)
        assert "disciplinaMap" in saved
        assert "manifestazioneMap" in saved


@pytest.mark.parametrize("save_to_file", [True, False])
def test_get_league_quotes_integration(save_to_file):
    """Test reale che interroga l'API Sisal e opzionalmente salva i dati su file."""
    scraper = BetScraper()
    data = scraper.get_league_quotes(sport_id=1, league_id=209)

    # Controlliamo che sia arrivato un dict valido
    assert data is not None
    assert isinstance(data, dict)

    assert "clusterMenu" in data

    if save_to_file:
        out_file = "tests/data/league_quotes.json"
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        # ricontrollo che il file sia coerente
        with open(out_file, "r", encoding="utf-8") as f:
            saved = json.load(f)
        assert "clusterMenu" in saved


@pytest.mark.parametrize("save_to_file", [True, False])
def test_get_match_quotes_integration(save_to_file):
    """Test reale che interroga l'API Sisal e opzionalmente salva i dati su file."""
    scraper = BetScraper()
    data_league = scraper.get_league_quotes(sport_id=1, league_id=209)

    quote_id = list(data_league["scommessaMap"].keys())[0]

    schedule_id = data_league["scommessaMap"][quote_id]["codicePalinsesto"]
    event_id = data_league["scommessaMap"][quote_id]["codiceAvvenimento"]

    data = scraper.get_match_quotes(schedule_id=schedule_id, event_id=event_id)

    # Controlliamo che sia arrivato un dict valido
    assert data is not None
    assert isinstance(data, dict)

    assert "clusterMenu" in data
    assert "scommessaMap" in data

    if save_to_file:
        out_file = "tests/data/match_quotes.json"
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        # ricontrollo che il file sia coerente
        with open(out_file, "r", encoding="utf-8") as f:
            saved = json.load(f)
        assert "clusterMenu" in saved
        assert "scommessaMap" in saved


def test_get_unique_events_unit():
    mock = {
        "scommessaMap": {
            "35401-1630-18": {},
            "35401-1630-19": {},
            "35401-1631-18": {},
            "35401-1631-19": {},
        }
    }

    scraper = BetScraper()
    data = scraper.get_unique_events(mock)

    # Controlliamo che sia arrivato un dict valido
    assert data is not None
    assert isinstance(data, set)
    assert len(data) == 2
    assert data == {"35401-1630", "35401-1631"}


@pytest.fixture
def sample_match_quotes():
    return {
        "scommessaMap": {"35401-1636-12192": {"codiceManifestazione": 209}},
        "infoAggiuntivaMap": {
            "35401-1636-12192-150": {
                "descrizione": "1X2 + U/O 1.5",
                "codiceScommessa": 12192,
                "soglia": "1.5",
                "esitoList": [
                    {
                        "codiceEsito": 1,
                        "descrizione": "1 + U",
                    },
                    {
                        "codiceEsito": 2,
                        "descrizione": "X + U",
                    },
                    {
                        "codiceEsito": 3,
                        "descrizione": "2 + U",
                    },
                    {
                        "codiceEsito": 4,
                        "descrizione": "1 + O",
                    },
                    {
                        "codiceEsito": 5,
                        "descrizione": "X + O",
                    },
                    {
                        "codiceEsito": 6,
                        "descrizione": "2 + O",
                    },
                ],
            }
        },
    }


@pytest.fixture
def sample_clean_bets():
    return [
        {
            "sport_id": 0,
            "bet_id": 0,
            "bet_desc": "TEST",
            "threshold": "1.5",
            "outcomes": ["1 + E", "X + E", "2 + E", "1 + T", "X + T", "2 + T"],
            "outcomes_id": [1, 2, 3, 4, 5, 6],
        }
    ]


@pytest.mark.parametrize("save_to_file", [True, False])
def test_get_clean_bets_unit(save_to_file, sample_match_quotes):

    scraper = BetScraper()
    data = scraper.get_clean_bets(sample_match_quotes)

    # Controlliamo che sia arrivato un dict valido
    assert data is not None
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["outcomes"] == ["1 + U", "X + U", "2 + U", "1 + O", "X + O", "2 + O"]
    assert data[0]["outcomes_id"] == [1, 2, 3, 4, 5, 6]

    if save_to_file:
        out_file = "tests/data/clean_bets.json"
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        # ricontrollo che il file sia coerente
        with open(out_file, "r", encoding="utf-8") as f:
            saved = json.load(f)
        assert "sport_id" in saved[0]
        assert "bet_id" in saved[0]
        assert "bet_desc" in saved[0]
        assert "threshold" in saved[0]
        assert "outcomes" in saved[0]
        assert "outcomes_id" in saved[0]


def test_update_covered_bets_integration(sample_clean_bets):

    scraper = BetScraper()
    scraper.update_covered_bets(sample_clean_bets)
    assert sample_clean_bets[0]["sport_id"] == 0
    assert sample_clean_bets[0]["bet_id"] == 0
