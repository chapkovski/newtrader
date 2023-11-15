
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
To start the application:
1. Run `otree devserver`.
2. If first-time running, remove older files:
   ```
   rm -rf __temp_migrations
   rm -rf db.sqlite3
   ```

## Contributing
Contributions are welcome. Please refer to the contribution guidelines for more details.

## License
This project is licensed under [appropriate license], allowing use and distribution per license terms.

## Acknowledgements
This project supports research by Chapkovski, Khapko, and Zoican (2023). For more information, [refer to the paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3971868).
