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


# Hysteresis / debounce state.
# Maps metric name -> True while that metric is currently above its threshold.
# A notification is only sent on the False -> True transition, so a sustained
# breach notifies once instead of on every single sample.
_alerting = {}


def reset_alert_state():
    """Forget which metrics are currently breaching (used by tests)."""
    _alerting.clear()


def get_alert_state():
    """Return a copy of the current debounce state."""
    return dict(_alerting)


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
    except Exception:
        return False


def check_alerts(cpu: float, ram: float, disk: float, notifier=None):
    """Evaluate the three samples and notify on newly-crossed thresholds.

    Returns only the metrics that *newly* crossed their threshold on this
    sample. Metrics that stay above their threshold stay silent until they
    drop back below and cross again.
    """
    thresholds = get_thresholds()
    samples = (("CPU", cpu), ("RAM", ram), ("DISK", disk))

    newly_breached = []
    for metric, value in samples:
        limit = thresholds[metric.lower()]
        above = value >= limit
        was_alerting = _alerting.get(metric, False)

        if above and not was_alerting:
            newly_breached.append((metric, value, limit))

        _alerting[metric] = above

    if newly_breached:
        title = "SysGuard Alert"
        lines = "; ".join(
            f"{metric} {value:.1f}% >= {limit:.1f}%"
            for metric, value, limit in newly_breached
        )
        send = notifier if notifier is not None else send_desktop_notification
        send(title, lines)

    return newly_breached