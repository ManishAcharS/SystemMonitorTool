"""Verify the real (non-fake) desktop notification path fires exactly once
per breach, and that multiple simultaneous breaches coalesce into one popup.
"""
import time

import alert
import config

print("thresholds in use:", config.get_thresholds())
print("plyer available:", alert.notification is not None)
print()

# ---- 1. real notification, single metric, sustained breach ----
alert.reset_alert_state()
print("Firing a REAL notification (cpu=99, sustained 5 samples)...")
for i in range(5):
    fired = alert.check_alerts(cpu=99.0, ram=0.0, disk=0.0)
    print(f"  sample {i + 1}: cpu=99.0 -> fired={bool(fired)}")
    time.sleep(0.4)
print()

# ---- 2. multi-metric breach should coalesce into ONE notification ----
alert.reset_alert_state()
captured = []
alert.check_alerts(cpu=99.0, ram=99.0, disk=99.0, notifier=lambda t, m: captured.append(m))
print("All three metrics breaching at once -> messages sent:", len(captured))
print("  message:", captured[0])

print()
print("Real-notifier test complete (watch for a single Windows toast above).")