# System Validation Harness

## Overview

This project implements a containerized validation framework designed to simulate, measure, and verify networked system behavior under controlled and reproducible conditions. It provides an isolated client–server environment where automated tests evaluate functionality, performance, regression stability, and system robustness under injected network impairments.

The framework reflects validation workflows used in infrastructure software, networking systems, and hardware-adjacent environments, where deterministic testing, automation, and continuous verification are critical.

---

## Technologies

* Python
* pytest
* Docker / Docker Compose
* Linux Networking (tc / netem, iperf3)
* GitHub Actions (CI/CD)
* JSON Metrics & JUnit Reporting

---

## Architecture

The validation environment consists of two Docker containers connected through a virtual network:

```id="6r4q2p"
Client Container (Python + pytest)
            │
            │ Validation logic + fault injection
            ▼
Server Container (iperf3 service)
```

The client container executes automated tests against the server container while collecting metrics and enforcing validation rules. Network conditions can be dynamically modified using Linux traffic control to simulate adverse scenarios.

Project structure:

* **docker/** — container orchestration and network topology
* **harness/** — validation utilities and fault-injection controls
* **tests/** — automated validation suites
* **baselines/** — stored performance reference metrics
* **reports/** — generated validation outputs and CI artifacts

---

## Validation Scope

The framework validates multiple dimensions of system behavior.

### Functional Validation

Verifies connectivity and service availability between client and server components to ensure baseline system operation.

### Performance Validation

Measures throughput using `iperf3` and records performance metrics for automated evaluation. Results are stored in structured output for analysis and comparison.

### Regression Detection

Compares current performance results against stored baseline metrics and identifies degradation beyond predefined thresholds, enabling automated detection of performance regressions.

### Fault Injection

Network impairments are introduced using Linux traffic control (`tc` / netem) to simulate real-world conditions, including:

* Packet loss
* Artificial latency
* Bandwidth limitation

These scenarios validate system resilience under non-ideal network conditions.

---

## Continuous Integration

A GitHub Actions pipeline automatically performs validation on every repository change. The pipeline:

1. Deploys the containerized environment
2. Installs dependencies inside the test container
3. Executes the automated test suite
4. Publishes validation artifacts and reports

This ensures reproducibility and continuous verification of system behavior.

---

## Execution

Start the validation environment:

```bash
docker compose -f docker/docker-compose.yml up -d
```

Install dependencies inside the client container:

```bash
docker exec svh_client bash -lc "
apt-get update && apt-get install -y iputils-ping iperf3 curl iproute2
python -m pip install --upgrade pip
pip install -r requirements.txt
"
```

Run the validation suite:

```bash
docker exec svh_client bash -lc "pytest"
```

---

## Outputs

Execution generates validation artifacts including:

* Throughput metrics
* JUnit test reports
* CI execution logs

These outputs provide measurable verification of system behavior and enable automated regression tracking.
