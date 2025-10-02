# sport_betting_ai
Scommesse automatiche con l'uso di Machine Learning, LLM and Deep Learning.

## Components
*bet_scraper*: Raccoglie le quote delle scommesse da un bookmaker italiano. Le quote vengono salvate in modo da avere anche uno storico con l'andamento di queste.

### Esempi di comandi per lanciare bet_scraper

#### Solo mappa bookmaker
python run_scraper.py

#### Quote lega
python run_scraper.py --sport_id 7 --league_id 12345

#### Quote match senza aggiornare DB
python run_scraper.py --schedule_id 101 --event_id 202

#### Quote match e aggiornamento DB
python run_scraper.py --schedule_id 101 --event_id 202 --update_db

*bet_simulator*: Utilizza lo storico delle scommesse per allenare e testare eventuali modelli.
