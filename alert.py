import platform
from config import get_thresholds

try:
    from plyer import notification
except Exception:
    notification = None

try:
    from win10toast import ToastNotifier
    toast = ToastNotifier()
except Exception:
    toast = None


def send_desktop_notification(title: str, message: str):
    system = platform.system()
    try:
        if notification is not None:
            notification.notify(title=title, message=message, timeout=10)
            return True
        if system == "Windows" and toast is not None:
            toast.show_toast(title, message, duration=10, threaded=True)
            return True
        if system == "Linux":
            import subprocess
            subprocess.run(["notify-send", title, message], check=False)
            return True
        return False
    except Exception as e:
        return False


def check_alerts(cpu: float, ram: float, disk: float):
    th = get_thresholds()
    alerts = []
    if cpu >= th["cpu"]:
        alerts.append(("CPU", cpu, th["cpu"]))
    if ram >= th["ram"]:
        alerts.append(("RAM", ram, th["ram"]))
    if disk >= th["disk"]:
        alerts.append(("DISK", disk, th["disk"]))
    if alerts:
        title = "SysGuard Alert"
        lines = "; ".join([f"{name} {val:.1f}% >= {t:.1f}%" for name, val, t in alerts])
        send_desktop_notification(title, lines)
    return alerts
