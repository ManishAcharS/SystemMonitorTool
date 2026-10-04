"""Ad-hoc debounce proof: drives alert.check_alerts with a fake notifier.

Simulates a CPU value that climbs above the threshold, stays high for many
refresh cycles, then drops below and climbs again.
"""
import alert

alert.reset_alert_state()

fired = []


def fake_notifier(title, message):
    fired.append((title, message))
    print(f"  NOTIFICATION #{len(fired)}: {title} | {message}")


TH = 50.0
seq = [
    ("below", 30.0),
    ("crosses up", 70.0),
    ("still high", 75.0),
    ("still high", 80.0),
    ("still high", 85.0),
    ("still high", 90.0),
    ("drops below", 40.0),
    ("crosses up again", 72.0),
    ("still high", 99.0),
]

print(f"Simulating CPU samples against threshold {TH}%\n")
for label, cpu in seq:
    result = alert.check_alerts(
        cpu=cpu,
        ram=0.0,
        disk=0.0,
        notifier=fake_notifier,
    )
    state = alert.get_alert_state()["CPU"]
    print(f"cpu={cpu:5.1f}% [{label:17}] alerting={state!s:5} fired_this_sample={bool(result)}")

print(f"\nTotal notifications fired: {len(fired)} (expected 2)")
print("PASS" if len(fired) == 2 else "FAIL")