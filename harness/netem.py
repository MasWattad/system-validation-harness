import subprocess


def sh(cmd: str) -> str:
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(
            f"Command failed: {cmd}\n"
            f"STDOUT:\n{p.stdout}\n"
            f"STDERR:\n{p.stderr}"
        )
    return p.stdout


def clear(iface: str = "eth0") -> None:
    sh(f"tc qdisc del dev {iface} root || true")


def set_latency(ms: int, jitter_ms: int = 0, iface: str = "eth0") -> None:
    clear(iface)
    sh(f"tc qdisc add dev {iface} root netem delay {ms}ms {jitter_ms}ms")


def set_loss(pct: float, iface: str = "eth0") -> None:
    clear(iface)
    sh(f"tc qdisc add dev {iface} root netem loss {pct}%")


def set_rate(mbit: int, iface: str = "eth0") -> None:
    clear(iface)
    sh(f"tc qdisc add dev {iface} root tbf rate {mbit}mbit burst 32kbit latency 400ms")