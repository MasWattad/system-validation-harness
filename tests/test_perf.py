import json
import subprocess
from pathlib import Path

REPORTS_DIR = Path("reports")
REPORTS_DIR.mkdir(exist_ok=True)

def run_json(cmd: str) -> dict:
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if p.returncode != 0:
        raise AssertionError(f"Command failed: {cmd}\nSTDOUT:\n{p.stdout}\nSTDERR:\n{p.stderr}")
    try:
        return json.loads(p.stdout)
    except json.JSONDecodeError as e:
        raise AssertionError(f"Expected JSON output but couldn't parse it.\nError: {e}\nRaw output:\n{p.stdout}")

def test_throughput_sla():
    # -J = JSON output, -t 2 seconds to keep it fast
    data = run_json("iperf3 -c server -t 2 -J")

    # Extract sender bitrate in bits/sec and convert to Gbits/sec
    bps = data["end"]["sum_sent"]["bits_per_second"]
    gbps = bps / 1e9

    metrics = {"throughput_gbps": round(gbps, 3)}
    (REPORTS_DIR / "metrics.json").write_text(json.dumps(metrics, indent=2))

    # SLA threshold (conservative). We'll tune later.
    assert gbps >= 5.0, f"Throughput too low: {gbps:.2f} Gbps (< 5.0)"