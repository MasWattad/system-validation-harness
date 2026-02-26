import json
import subprocess
import pytest
from harness import netem


def run(cmd: str) -> str:
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    if p.returncode != 0:
        raise AssertionError(
            f"{cmd}\nSTDOUT:\n{p.stdout}\nSTDERR:\n{p.stderr}"
        )

    return p.stdout


@pytest.fixture(autouse=True)
def cleanup_netem():
    netem.clear()
    yield
    netem.clear()


def iperf_gbps() -> float:
    out = run("iperf3 -c server -t 2 -J")
    data = json.loads(out)
    return data["end"]["sum_sent"]["bits_per_second"] / 1e9


def test_injected_latency():
    netem.set_latency(80, 10)
    out = run("ping -c 5 server")
    assert "0% packet loss" in out


def test_bandwidth_cap():
    netem.set_rate(200)
    gbps = iperf_gbps()
    assert gbps < 1.0

import re

def test_packet_loss_detection():
    netem.set_loss(10.0)
    out = run("ping -c 50 -i 0.2 -W 1 server")

    m = re.search(r"(\d+)%\s+packet loss", out)
    assert m, f"Could not parse packet loss from ping output:\n{out}"

    loss_pct = int(m.group(1))
    assert loss_pct >= 1, f"Expected some packet loss, got {loss_pct}%\n{out}"
