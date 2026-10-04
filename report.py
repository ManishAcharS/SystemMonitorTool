import sqlite3
import csv
from datetime import datetime, date
from pathlib import Path

DB_PATH = Path("history.db")


def get_history():
    if not DB_PATH.exists():
        return []
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT timestamp, cpu, ram, disk FROM history ORDER BY timestamp ASC")
    rows = cur.fetchall()
    conn.close()
    return rows


def daily_summary(rows):
    if not rows:
        return None
    today = date.today().isoformat()
    today_rows = [r for r in rows if str(r[0]).startswith(today)]
    target = today_rows if today_rows else rows[-100:]  # fallback to recent
    cpus = [float(r[1]) for r in target]
    rams = [float(r[2]) for r in target]
    disks = [float(r[3]) for r in target]
    return {
        "count": len(target),
        "cpu_avg": sum(cpus) / len(cpus) if cpus else 0,
        "cpu_max": max(cpus) if cpus else 0,
        "ram_avg": sum(rams) / len(rams) if rams else 0,
        "ram_max": max(rams) if rams else 0,
        "disk_avg": sum(disks) / len(disks) if disks else 0,
        "disk_max": max(disks) if disks else 0,
    }


def export_csv(rows, out_path="report.csv"):
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["timestamp", "cpu", "ram", "disk"])
        w.writerows(rows)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="SysGuard daily usage report")
    parser.add_argument("--csv", action="store_true", help="export to CSV")
    parser.add_argument("--out", default="report.csv", help="CSV output path")
    args = parser.parse_args()

    rows = get_history()
    s = daily_summary(rows)
    if s is None:
        print("No history found in history.db")
        return
    print(f"SysGuard Report (based on {s['count']} records)")
    print(f"  CPU: avg={s['cpu_avg']:.1f}% max={s['cpu_max']:.1f}%")
    print(f"  RAM: avg={s['ram_avg']:.1f}% max={s['ram_max']:.1f}%")
    print(f"  Disk: avg={s['disk_avg']:.1f}% max={s['disk_max']:.1f}%")
    if args.csv:
        export_csv(rows, args.out)
        print(f"Exported to {args.out}")


if __name__ == "__main__":
    main()
