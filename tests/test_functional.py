import subprocess


def run(cmd: str) -> str:
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise AssertionError(
            f"Command failed: {cmd}\n"
            f"STDOUT:\n{result.stdout}\n"
            f"STDERR:\n{result.stderr}"
        )

    return result.stdout


def test_ping_server():
    output = run("ping -c 2 server")
    assert "0% packet loss" in output