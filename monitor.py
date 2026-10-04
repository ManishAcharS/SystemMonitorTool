import time
import platform
import psutil
from rich.console import Console
from rich.table import Table
from rich.live import Live

from config import load_config, get_interval, get_thresholds
from db import init_db, insert_record
from alert import check_alerts


console = Console()


def get_disk_usage():
    try:
        usage = psutil.disk_usage("/")
    except Exception:
        try:
            usage = psutil.disk_usage("C:\\")
        except Exception:
            try:
                usage = psutil.disk_usage(".")
            except Exception:
                return 0.0
    return usage.percent


def get_ram_usage():
    try:
        return psutil.virtual_memory().percent
    except Exception:
        return 0.0


def get_cpu_usage():
    try:
        return psutil.cpu_percent(interval=0.0)
    except Exception:
        return 0.0


def get_per_core_cpu():
    try:
        return psutil.cpu_percent(interval=0.0, percpu=True)
    except Exception:
        return []


def build_table():
    table = Table(title="SysGuard - System Health Monitor")
    table.add_column("Metric", style="bold")
    table.add_column("Usage", style="bold")
    table.add_column("Per-core", style="dim")

    cpu = get_cpu_usage()
    ram = get_ram_usage()
    disk = get_disk_usage()
    cores = get_per_core_cpu()

    table.add_row("CPU", f"{cpu:.1f}%", ", ".join([f"{c:.1f}%" for c in cores]) or "-")
    table.add_row("RAM", f"{ram:.1f}%", "-")
    table.add_row("Disk", f"{disk:.1f}%", "-")

    return table, cpu, ram, disk


def main():
    init_db()
    cfg = load_config()
    interval = get_interval()
    if interval < 0.1:
        interval = 0.5

    with Live(build_table()[0], console=console, refresh_per_second=2) as live:
        try:
            while True:
                table, cpu, ram, disk = build_table()
                live.update(table)
                try:
                    insert_record(cpu, ram, disk)
                except Exception:
                    pass
                try:
                    check_alerts(cpu, ram, disk)
                except Exception:
                    pass
                time.sleep(interval)
        except KeyboardInterrupt:
            console.print("\n[bold]SysGuard stopped.[/bold]")


if __name__ == "__main__":
    main()
