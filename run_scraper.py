import argparse

from betting_ai.bet_scraper.bet_scraper import BetScraper


def main():
    parser = argparse.ArgumentParser(description="Sisal Scraper CLI intelligente")
    parser.add_argument("--sport_id", type=int, help="ID dello sport")
    parser.add_argument("--league_id", type=int, help="ID della lega")
    parser.add_argument("--schedule_id", type=int, help="ID del match schedule")
    parser.add_argument("--event_id", type=int, help="ID dell'evento")
    parser.add_argument(
        "--update_db", action="store_true", help="Aggiorna il DB con le bets del match"
    )
    parser.add_argument(
        "--update_bet_sport",
        type=int,
        help="Inizializza la bet map per lo sport specificato",
    )
    args = parser.parse_args()

    scraper = BetScraper()

    # Comando per inizializzare la bet map per uno sport
    if args.update_bet_sport:
        print(f"Inizializzando la bet map per lo sport {args.update_bet_sport}...")
        result = scraper.initialize_bet_map_by_sport(args.update_bet_sport)
        print(f"Bet map aggiornata, {result} bets inserite/aggiornate.")
        return

    # Nessun argomento → scarica mappa completa dei bookmaker
    if not any([args.sport_id, args.league_id, args.schedule_id, args.event_id]):
        print("Scaricando la mappa dei bookmaker...")
        data = scraper.get_bookmaker_map()
        print(data)
        return

    # Quote lega
    if args.sport_id and args.league_id:
        print(f"Scaricando quote per sport {args.sport_id} lega {args.league_id}...")
        league_quotes = scraper.get_league_quotes(args.sport_id, args.league_id)
        print(league_quotes)

    # Quote match e aggiornamento DB
    if args.schedule_id and args.event_id:
        print(f"Scaricando quote per match {args.schedule_id}-{args.event_id}...")
        match_quotes = scraper.get_match_quotes(args.schedule_id, args.event_id)
        print(match_quotes)

        if args.update_db and match_quotes:
            print("Pulendo e aggiornando le bets nel DB...")
            clean_bets = scraper.get_clean_bets(match_quotes)
            scraper.update_covered_bets(clean_bets)
            print(f"{len(clean_bets)} bets aggiornate nel DB.")


if __name__ == "__main__":
    main()
