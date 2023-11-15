
# newtrader

## Overview
"newtrader" is an oTree-based project developed for the study "Trading Gamification and Investor Behavior" by Chapkovski, Khapko, and Zoican (2023). This study investigates the effects of gamification in trading platforms on investor behavior. [Read the paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3971868)

## Repository Contents
This repository, structured into three apps, includes:
- `trader_wrapper`: A gamified platform for single traders.
- `pretrade`: For displaying instructions and comprehension checks before the main program.
- `post_experimental`: Launched post-main program for demographics and financial literacy quiz.

## Requirements
- Python < 3.9 (Due to limitations in otree3.4.0)
- Dependencies in `requirements.txt`.

## Setup and Installation
1. Clone this repository.
2. Install dependencies: `pip install -r requirements.txt`.

## Usage
(Note: The following instructions are for macOS or other Linux-like systems.)
1. Run:
   ```sh
   otree devserver
   ```
2. If first-time running, remove older files:
   ```sh
   rm -rf __temp_migrations
   rm -rf db.sqlite3
   ```
3. The launched server will be available at [localhost:8000](http://localhost:8000). To change the default port, run `otree devserver 1234`, and it will then be available at `localhost:1234`.


## Game Configuration via settings.py

The experiment's configuration is mostly defined in `settings.py` through `SESSION_CONFIGS` and `SESSION_CONFIG_DEFAULTS`.

### SESSION_CONFIGS
- `post`: For running the post-experimental survey with a financial quiz.
- `full`: Runs the full set of apps (`pretrade`, `trader_wrapper`, `post_experimental`), encompassing the entire experiment.
- `trader`: To test the trading platform (`trader_wrapper`) only.

### SESSION_CONFIG_DEFAULTS
Settings with their explanations:
- `training_round_name`: Name of the training round.
- `for_prolific`: Boolean to indicate if the experiment is run on Prolific.
- `prolific_redirect_url`: URL for redirection back to Prolific after experiment completion.
- `prediction_at`: Tick number at which predictions are made.
- `trading_at`: Tick number when trading starts.
- `tick_frequency`: Seconds between ticks.
- `awards_at`: Tick numbers at which awards are given.


## Additional Configuration Files
This section includes descriptions of various configuration files used in the project:
- `blocks.yaml`: Describes platform design parameters for each trading round.
- `financial_quiz.yaml`: Contains the financial quiz.
- `treatments.yaml`: Outlines differences in price generation and gamification between participants.
- `prices_markov_main_*.csv` & `prices_markov_robust_*.csv`: Contain pregenerated prices based on Markov or martingale models, with indices corresponding to round numbers.


## Data
In addition to the standard oTree data structure, the `trader_wrapper` app in this project includes an additional model to record every client-side event during trading sessions. The data model `Event` is defined as follows:

```python
class Event(djmodels.Model):
    owner = djmodels.ForeignKey(to=Player, on_delete=djmodels.CASCADE, related_name='events')
    name = models.StringField()
    timestamp = djmodels.DateTimeField(null=True, blank=True)
    body = models.StringField()
    balance = models.FloatField()  # Current state of bank account
    tick_number = models.IntegerField()
    n_transactions = models.IntegerField()
```

This model captures details such as the type of event (e.g., GAME_STARTS, awardForTransaction, GAME_ENDS, buy, sell), the exact timestamp, the update counter number, the number of transactions that have occurred so far, and the current balance. Each event is linked to the specific player (`owner`) who generated it.

All this data can be downloaded in CSV format via the `Data -> Third-party data export -> Events export` option.


## Frontend
The platform's user interface is built using Vue 2.x. Compiled files are located in `_static/front/js` and `_static/front/css`. Gifs displayed for user awards (based on transaction numbers set in settings) are in `_static/img`.

The source code for the Vue app can be found at: [newgamifiedtrader repository](https://github.com/chapkovski/newgamifiedtrader/).

## Contributing
Contributions are welcome. Please refer to the contribution guidelines for more details.

## License
This project is licensed under [appropriate license], allowing use and distribution per license terms.

## Acknowledgements
This project supports research by Chapkovski, Khapko, and Zoican (2023). For more information, [refer to the paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3971868).
