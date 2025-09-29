import pytest

from betting_ai.bet_simulator.bet_mng import BetManager
from betting_ai.models.bet_model import Bet


# Dummy bet per i test
def sample_bet():
    return Bet(
        team1="Milan",
        team2="Inter",
        quote=1.95,
        result="pending",
        date_place="2025-09-29",
        date_event="2025-09-30",
        sport="calcio",
        league="Serie A",
    )


@pytest.fixture
def bet_manager():
    # Usa test=True per non toccare i dati reali
    return BetManager(test=True)


def test_place_bet(bet_manager):
    bet = sample_bet()
    result = bet_manager.place_bet(bet)
    assert result is True


def test_find_bet(bet_manager):
    bet = sample_bet()
    bet_manager.place_bet(bet)
    found = bet_manager.find_bet({"team1": bet.team1, "team2": bet.team2})
    assert found is not None
    assert found["team1"] == bet.team1
    assert found["team2"] == bet.team2


def test_move_old_bets(bet_manager):
    bet = sample_bet()
    bet_manager.place_bet(bet)
    result = bet_manager.move_old_bets(bet)
    assert result is True


def test_delete_bet(bet_manager):
    bet = sample_bet()
    bet_manager.place_bet(bet)
    found = bet_manager.find_bet({"team1": bet.team1, "team2": bet.team2})
    assert found is not None

    delete_result = bet_manager.delete_bet(found["_id"])
    assert delete_result is True

    after_delete = bet_manager.find_bet({"_id": found["_id"]})
    assert after_delete is None
