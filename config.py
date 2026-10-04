import os
import yaml
from pathlib import Path

CONFIG_PATH = Path("config.yaml")


def load_config():
    if not CONFIG_PATH.exists():
        return {
            "monitor": {"interval": 2, "history_limit": 100000},
            "thresholds": {"cpu": 85.0, "ram": 85.0, "disk": 80.0},
        }
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except Exception:
        return {
            "monitor": {"interval": 2, "history_limit": 100000},
            "thresholds": {"cpu": 85.0, "ram": 85.0, "disk": 80.0},
        }


def get_thresholds():
    cfg = load_config()
    th = cfg.get("thresholds", {})
    return {
        "cpu": float(th.get("cpu", 85.0)),
        "ram": float(th.get("ram", 85.0)),
        "disk": float(th.get("disk", 80.0)),
    }


def get_interval():
    cfg = load_config()
    try:
        return float(cfg.get("monitor", {}).get("interval", 2))
    except Exception:
        return 2.0
