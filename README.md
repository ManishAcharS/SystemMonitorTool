# SysGuard — System Health Monitor & Auto-Alert Tool

> **SysGuard is a command-line tool — run it in a terminal; it displays a live-updating dashboard (similar to htop).** There is no GUI and no desktop app icon.

Cross-platform (Windows + Linux) system monitoring CLI tool built with Python, psutil, and rich. Tracks CPU, RAM, and disk usage in real time, logs history to SQLite, sends desktop alerts, optionally emails on threshold breaches, generates auto-start schedulers, and produces daily summary reports.

## Features
- Live CLI dashboard (rich table with CPU%, RAM%, Disk%, per-core)
- Local SQLite history (timestamp, cpu, ram, disk)
- Threshold alerts (desktop + optional email)
- Background scheduling (cron/Task Scheduler)
- Daily summary report (terminal + CSV export)

## How it works
- monitor.py — Core engine: collects CPU/RAM/disk every N seconds, writes to SQLite (history.db), renders live rich dashboard, triggers alerts.
- db.py — SQLite helpers: init history.db, insert records, fetch history.
- config.py — Loads config.yaml; reads thresholds/interval with defaults and graceful fallback.
- alert.py — Desktop notifications via plyer with fallbacks (win10toast on Windows, notify-send on Linux).
- email_alert.py — Optional SMTP email alerts (TLS) reading from .env.
- report.py — Reads history.db, prints daily summary (avg/max), exports CSV with --csv.
- scheduler.py — Generates sysguard_task.xml (Windows) or sysguard_cron.txt (Linux) with absolute paths.

## Quick Start
1. Clone repo: git clone <repo>
2. pip install -r requirements.txt
3. python monitor.py

## Config
- config.yaml — thresholds (cpu/ram/disk %) and monitor.interval (seconds). Defaults: 85/85/80, interval 2s.
- .env (copy from .env.example) — SMTP: SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASS, FROM_EMAIL, TO_EMAIL (optional).

## Reports
- python report.py — print summary (today or recent)
- python report.py --csv --out report.csv — export full history

## Scheduling
- Windows: python scheduler.py -> sysguard_task.xml; import via Task Scheduler or schtasks /Create /XML sysguard_task.xml /TN SysGuard
- Linux: python scheduler.py -> sysguard_cron.txt; install via crontab sysguard_cron.txt

## Troubleshooting
1. Desktop notifications: Windows needs win10toast (installed); Linux needs notify-send in DE. Fail silently if unavailable.
2. Email alerts: ensure .env has SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASS, TO_EMAIL; many providers need app passwords/TLS (port 587).
3. Paths/OS: code falls back for disk paths (/ not found -> C:\ or .); no hardcoded paths; scheduler uses current workdir.
4. Rich display: minimal terminals may have width issues; rich still functions in most cases.

## License
MIT License — see LICENSE for details.
