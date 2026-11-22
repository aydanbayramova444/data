from pathlib import Path

from src import etl, generate, report

root = Path(__file__).parent
data, out = root / "data", root / "reports"
data.mkdir(exist_ok=True)
out.mkdir(exist_ok=True)

generate.generate(data / "tickets_raw.csv")
db, quality = etl.run(data / "tickets_raw.csv", data / "tickets_clean.csv", data / "tickets.db")
report.build(db, quality, root / "sql" / "analysis.sql", out)
db.close()
print("Done:", quality)
