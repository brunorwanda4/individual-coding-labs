# Individual Coding Labs

This repository contains the three individual coding labs for Introduction to Python Programming and Databases.

## Lab 1 - Kigali Road Simulation

Run:

```bash
python road_simulation.py
```

The analyser is optional:

```bash
bash analyze_log.sh
# or
bash analyze_log.sh custom.log
```

## Lab 2 - Grade Evaluator

Run:

```bash
python grade-evaluator.py
```

Enter `grades.csv` when prompted. The organiser moves the current CSV into `archive/` and creates a fresh empty `grades.csv`:

```bash
bash organizer.sh
```

## Lab 3 - Social Media Data Detective

Place the provided Kaggle `twitter_dataset.csv` in this directory, then run:

```bash
python data-detective.py
bash feed-analyzer.sh twitter_dataset.csv
```
