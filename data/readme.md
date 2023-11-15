
## Data Folder File Descriptions

### `blocks.yaml`
Describes the parameters of platform design for each of the four trading rounds (excluding the first training round) in the experiment.

### `financial_quiz.yaml`
Contains the financial quiz used in the experiment.

### `treatments.yaml`
Details the differences in price generation and gamification between participants, outlining the experiment's mixed within/between subject design.

### `prices_markov_main_*.csv` & `prices_markov_robust_*.csv`
These files contain pregenerated prices based on either pure Markov or martingale pricing models. The indices in the file names (e.g., 0, 1, 2, etc.) correspond to the round number minus one. For example, `prices_markov_robust_0.csv` defines the prices encountered in the training round (round 1) for participants assigned to a treatment with martingale pricing.
