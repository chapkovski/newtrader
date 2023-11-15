
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

## Data
In addition to the standard oTree data structure, the `trader_wrapper` app in this project includes an additional model to record every client-side event during trading sessions. The data model `Event` is defined as follows:

```python
class Event(djmodels.Model):
    class Meta:
        ordering = ['timestamp']
        get_latest_by = 'timestamp'

    part_number = models.IntegerField()
    owner = djmodels.ForeignKey(
        to=Player, on_delete=djmodels.CASCADE, related_name='events')
    name = models.StringField()
    timestamp = djmodels.DateTimeField(null=True, blank=True)
    body = models.StringField()
    balance = models.FloatField()  # Current state of bank account
    tick_number = models.IntegerField()
    n_transactions = models.IntegerField()
```

This model captures details such as the type of event (e.g., GAME_STARTS, awardForTransaction, GAME_ENDS, buy, sell), the exact timestamp, the update counter number, the number of transactions that have occurred so far, and the current balance. Each event is linked to the specific player (`owner`) who generated it.

All this data can be downloaded in CSV format via the `Data -> Third-party data export -> Events export` option.

## Contributing
Contributions are welcome. Please refer to the contribution guidelines for more details.

## License
This project is licensed under [appropriate license], allowing use and distribution per license terms.

## Acknowledgements
This project supports research by Chapkovski, Khapko, and Zoican (2023). For more information, [refer to the paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3971868).
