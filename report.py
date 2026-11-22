"""Run the SQL and save tables and charts."""
import re


def bar_chart(path, title, rows, column):
    top = max(r[column] for r in rows)
    svg = [f'<text x="10" y="26" font-size="17" font-weight="bold">{title}</text>']
    for i, r in enumerate(rows):
        y, width = 45 + i * 38, 400 * r[column] / top
        svg += [f'<text x="10" y="{y + 18}">{r[0]}</text>',
                f'<rect x="140" y="{y}" width="{width:.0f}" height="26" fill="#2563a6"/>',
                f'<text x="{148 + width:.0f}" y="{y + 18}">{r[column]}%</text>']
    height = 55 + 38 * len(rows)
    path.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="640" height="{height}" '
                    'font-family="Arial" font-size="13">'
                    f'<rect width="100%" height="100%" fill="white"/>{"".join(svg)}</svg>\n')


def build(db, quality, sql_path, out):
    md = ["# Results", "", "## Data quality", ""]
    md += [f"- {key}: {value}" for key, value in quality.items()]
    results = {}
    for name, sql in re.findall(r"-- name: (\w+)\n(.*?;)", sql_path.read_text(), re.S):
        cursor = db.execute(sql)
        head, rows = [c[0] for c in cursor.description], cursor.fetchall()
        results[name] = rows
        md += ["", f"## {name}", "", "| " + " | ".join(head) + " |", "|---" * len(head) + "|"]
        md += ["| " + " | ".join(map(str, r)) + " |" for r in rows]
    (out / "results.md").write_text("\n".join(md) + "\n")
    bar_chart(out / "sla_by_channel.svg", "Tickets resolved within SLA", results["by_channel"], 2)
    bar_chart(out / "late_by_category.svg", "Share of all late tickets", results["by_category"], 3)
