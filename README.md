# SysGuard — System Health Monitor & Auto-Alert Tool

Cross-platform (Windows + Linux) system monitoring CLI tool built with Python, psutil, and rich. Tracks CPU, RAM, and disk usage in real time, logs history to SQLite, sends desktop alerts, optionally emails on threshold breaches, generates auto-start schedulers, and produces daily summary reports.

## Features
- Live CLI dashboard (rich table with CPU%, RAM%, Disk%, per-core)
- Local SQLite history (timestamp, cpu, ram, disk)
- Threshold alerts (desktop + optional email)
- Background scheduling (cron/Task Scheduler)
- Daily summary report (terminal + CSV export)

## Quick Start
1. Clone repo: git clone <repo> 
2. pip install -r requirements.txt
3. python monitor.py

## Config
- config.yaml — adjust thresholds and interval
- .env (copy from .env.example) — SMTP settings for email alerts

## Reports
- python report.py — print daily summary (use --csv to export)
