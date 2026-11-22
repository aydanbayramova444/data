# Customer Support SLA Analysis

Why are support tickets resolved late, and what should the team fix first?

> The data is **synthetic**: `src/generate.py` creates it, including the patterns and the errors.
> The findings demonstrate an analysis method and do not describe a real company.
> Built with the help of an AI coding assistant (Claude Code).

**Tools:** Python (standard library), SQL (SQLite, window functions), ETL, SVG charts

## Pipeline

1. **Extract:** read a messy export of 6,120 rows
2. **Transform:** remove 120 duplicates and 60 invalid durations, fix category names and two date formats
3. **Load:** write 5,940 clean rows to SQLite and CSV
4. **Analyse:** answer the questions in [analysis.sql](sql/analysis.sql)

## Findings

| Question | Finding | Recommendation |
|---|---|---|
| How are we doing? | 67.7% of tickets meet the SLA | Track the rate weekly |
| Which channel is weakest? | Email meets the SLA 36.6% of the time, the call center 79.6% | Triage the email queue first |
| When are we slow? | Night 57.9%, day 77.6% | Review night staffing |
| What causes most late tickets? | Card (24.8%) and Transfer (23.3%) | Write playbooks for both |
| Does being late matter? | Satisfaction is 2.82 for late and 3.84 for on-time tickets | Warn customers about delays early |

These are associations. They do not prove what causes the delays.

![SLA by channel](reports/sla_by_channel.svg)
![Late tickets by category](reports/late_by_category.svg)

All tables: [results.md](reports/results.md)

## Run

Python 3.9+ with SQLite 3.25+, nothing to install:

```
python3 main.py
python3 -m unittest
```

`data/tickets_clean.csv` can also be imported into Power BI or Excel.
