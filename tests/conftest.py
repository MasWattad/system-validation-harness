import subprocess

def _sh(cmd: str) -> None:
    subprocess.run(cmd, shell=True, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def pytest_runtest_setup(item):
    # Always clear any leftover traffic shaping before EVERY test
    _sh("tc qdisc del dev eth0 root || true")