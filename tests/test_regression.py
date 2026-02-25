import json
from pathlib import Path

BASELINE_PATH = Path("baselines/baseline.json")
METRICS_PATH = Path("reports/metrics.json")

def test_throughput_regression():
    assert BASELINE_PATH.exists(), f"Missing baseline: {BASELINE_PATH}"
    assert METRICS_PATH.exists(), f"Missing metrics: {METRICS_PATH}"

    baseline = json.loads(BASELINE_PATH.read_text())
    current = json.loads(METRICS_PATH.read_text())

    base = float(baseline["throughput_gbps"])
    cur = float(current["throughput_gbps"])

    # Allow up to 20% drop vs baseline
    max_drop_pct = 0.20
    min_allowed = base * (1 - max_drop_pct)

    assert cur >= min_allowed, (
        f"Throughput regression: baseline={base:.3f} Gbps, current={cur:.3f} Gbps "
        f"(allowed >= {min_allowed:.3f} Gbps)"
    )