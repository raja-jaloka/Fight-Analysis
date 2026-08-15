# Fight-Analysis

A UFC fight outcome prediction pipeline: scrape fighter/fight data from public stats sites, engineer features (career stats + a custom Elo-style rating + recent-form averages), and train classifiers to predict fight winners.

## Pipeline

The project runs as a sequence of standalone scripts rather than a single entry point. Run them in this order:

### 1. Scraping (`Scraped-Dataset/`)
- `fighters.py` — scrapes the base fighter roster (name, height, weight, reach, stance, record) from ufcstats.com → `fighters.json`
- `fighter_stats.py` — enriches each fighter with detailed page stats → `fighter_stats.json`
- `Extra_fighter_url.py` / `Extra_fighters_stats.py` — scrapes a second fighter source (ufc.com) for supplemental stats → `Extra_fighters_url.json`, `Extra_fighters_stats.json`
- `events_url.py` / `per_event.py` — scrapes UFC event listings and per-event fight cards from sports-statistics.com → `events_url.json`, `fights_per_event.json`
- `fight_stats.py` — scrapes round-by-round stats for each individual fight → `stats_per_fight.json`

### 2. Grouping & feature prep (`Data_grouping/`)
- `fight_group_dict.py` — flattens per-event fight stats into a dict keyed by fight link → `fight_group_dict.json`
- `group_fighter_fights.py` — groups fight links by fighter → `fighter_fights_group.json`
- `set_fighter_rating.py` — initializes every fighter at a 1500 Elo rating
- `elo_rating.py` — replays fight history chronologically to compute Elo ratings from outcomes
- `Output_elo_rating.py` — prints fighters ranked by rating (debug/inspection utility)
- `updated_stats_per_fight.py` — attaches resolved fighter IDs to each fight record
- `final_usable_data.py` — flattens everything into one row per fight → `usable_data.json`
- `json_to_csv.py` — converts the JSON dataset to CSV → `usable_data.csv`
- `fighter_matcher.py` — experimental script for reconciling fighter identities across the two scraped sources (currently dead code, fully commented out)

### 3. Processing & modeling
- `data-processing/data-processing.py` — fills missing values (0 for round-stat NaNs, column mean for physical attributes) → `processed_data.csv`
- `data-understanding/data_und.py` — a single exploratory histogram (body-target strikes)
- `data-processing/data_preprocessing.py` — the actual training script. Drops round-by-round columns, does an 80/20 train/test split, and benchmarks 5 model configs (Logistic Regression, Logistic Regression + Quantile Transformer, Decision Tree, Random Forest, XGBoost) on accuracy/precision/recall/log-loss/ROC-AUC/calibration. Saves the two winning pipelines as `lrqt.joblib` (Logistic Regression + Quantile Transformer — best log-loss/calibration tradeoff) and `rfc.joblib` (Random Forest — used for the hard win/loss call).

### 4. Inference (`Logic_engine/`)
- `engine.py` — loads both saved models, builds a feature vector for two named fighters (static stats + last-5-fight rolling averages), and prints a win probability plus a hard prediction. Currently hardcoded to run five example matchups at the bottom of the file rather than exposing a callable interface.

## Data files

The repo currently ships its intermediate and final artifacts directly (`fighters.json`, `usable_data.csv`, `processed_data.csv`, `lrqt.joblib`, `rfc.joblib`, etc.) so you can run the modeling and inference stages without re-scraping.

## Setup

```bash
git clone https://github.com/raja-jaloka/Fight-Analysis.git
cd Fight-Analysis
python -m venv .venv
source .venv/bin/activate  # .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## Usage

To re-run predictions with the existing trained models:

```bash
cd Logic_engine
python engine.py
```

Edit the `fighter_prob(name1, name2)` calls at the bottom of `engine.py` to try other matchups (names must match entries in `pri-fighter-link.json`).

To retrain from scratch, run the pipeline stages above in order — scraping first, then `Data_grouping/`, then `data-processing/data-processing.py`, then `data-processing/data_preprocessing.py`.


## License

No license file is currently included.
