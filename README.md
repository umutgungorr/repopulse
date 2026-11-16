<div align="center">

```text
  ██████╗ ███████╗██████╗  ██████╗ ██████╗ ██╗   ██╗██╗     ███████╗███████╗
  ██╔══██╗██╔════╝██╔══██╗██╔═══██╗██╔══██╗██║   ██║██║     ██╔════╝██╔════╝
  ██████╔╝█████╗  ██████╔╝██║   ██║██████╔╝██║   ██║██║     ███████╗█████╗  
  ██╔══██╗██╔══╝  ██╔═══╝ ██║   ██║██╔═══╝ ██║   ██║██║     ╚════██║██╔══╝  
  ██║  ██║███████╗██║     ╚██████╔╝██║     ╚██████╔╝███████╗███████║███████╗
  ╚═╝  ╚═╝╚══════╝╚═╝      ╚═════╝ ╚═╝      ╚═════╝ ╚══════╝╚══════╝╚══════╝
  ───────────╱╲╱╲─── Git Forensic Audit & Codebase Health ───╱╲╱╲───────────
```

### The Clinical Codebase Health Card & Architectural Forensic Engine

**A zero-dependency CLI & GitHub Action that mines Git commit history in <20ms to diagnose single-author knowledge silos (bus factor), identify architectural bug hotspots, uncover temporal coupling, and compute an objective 0–100 codebase health score.**

[![CI](https://github.com/umutgungorr/repopulse/actions/workflows/ci.yml/badge.svg)](https://github.com/umutgungorr/repopulse/actions)
[![GitHub Marketplace](https://img.shields.io/badge/Marketplace-RepoPulse%20Action-red?logo=githubactions&logoColor=white)](https://github.com/marketplace/actions/repopulse-git-forensic-health-audit)
[![Version](https://img.shields.io/badge/version-v1.0.1-red.svg?logo=git&logoColor=white)](https://github.com/umutgungorr/repopulse/releases)
[![PyPI](https://img.shields.io/pypi/v/git-repopulse.svg?color=blue&logo=pypi&logoColor=white)](https://pypi.org/project/git-repopulse/)
[![Python Version](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-3776AB.svg?logo=python&logoColor=white)](https://github.com/umutgungorr/repopulse)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-0%20external-success.svg)](pyproject.toml)
[![Tests](https://img.shields.io/badge/tests-100%25%20passing-brightgreen.svg)](#test-suite)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![License: MIT](https://img.shields.io/badge/license-MIT-red.svg)](LICENSE)

---

[⚡ Instant Audit](#instant-audit) •
[📋 The Forensic Health Dossier](#the-forensic-health-dossier) •
[🔬 Static Linters vs. Forensic Git Analysis](#static-vs-forensic) •
[🚨 The 3 Pillars of Forensic Health](#the-3-pillars) •
[🤖 GitHub Marketplace Action](#github-actions-ci) •
[⚙️ CLI Command Reference](#cli-reference) •
[⚡ Performance Benchmarks](#benchmarks) •
[🤝 Contributing](#contributing)

</div>

---

<a id="the-forensic-health-dossier"></a>
## 📋 The Forensic Health Dossier

Static code linters only tell you how your code is formatted today. They cannot tell you **who wrote it**, **how fast it changes**, or **which modules are silently tangled together**.

When you run `repopulse audit`, it parses your repository's native Git commit history and generates an **instant, clinical forensic audit report**:

```text
╔══════════════════════════════════════════════════════════════════════════════════════╗
║  🩺 REPOPULSE CODEBASE HEALTH DOSSIER                                GRADE: A (92)   ║
╠══════════════════════════════════════════════════════════════════════════════════════╣
║  Target: my-team/core-api                      Window: Last 365 Days                 ║
║  Commits Analyzed: 1,420                       Active Contributors: 14               ║
║  Health Score: 92 / 100 [██████████████████░░] (STATUS: HEALTHY / CI GATE PASS)      ║
╠══════════════════════════════════════════════════════════════════════════════════════╣
║  🚨 1. KNOWLEDGE SILO & BUS FACTOR ALERTS                                            ║
║  ├─ [HIGH RISK] auth/oauth_provider.py ──── 94.2% written by @alice (1,240 net LOC)  ║
║  │  └─ Forensic Finding: If @alice leaves the company, core auth is unmaintainable.  ║
║  ├─ [WARNING]   billing/webhook_worker.py ── 78.5% written by @bob                   ║
║  └─ [HEALTHY]   db/models/ ──────────────── Multi-author collective ownership (6)    ║
╠══════════════════════════════════════════════════════════════════════════════════════╣
║  🔥 2. ARCHITECTURAL HOTSPOTS (Statistical Bug Incubators)                           ║
║  ├─ [CRITICAL] services/checkout.py ─────── Churn: 84 revisions | Net LOC: 920      ║
║  │  └─ Forensic Finding: High revision churn × large file size = 80% bug incubator. ║
║  └─ [MODERATE] api/handlers/users.py ────── Churn: 22 revisions | Net LOC: 310      ║
╠══════════════════════════════════════════════════════════════════════════════════════╣
║  🔗 3. TEMPORAL CO-CHANGE COUPLING (Hidden Architectural Leaks)                      ║
║  └─ [LEAK DETECTED] billing/stripe.py <─── 81.2% co-change ───> queue/dispatcher.py  ║
║     └─ Forensic Finding: 0 shared imports, but they commit together 4 out of 5 times.║
╠══════════════════════════════════════════════════════════════════════════════════════╣
║  💡 PRESCRIPTION & REMEDIATION PLAN:                                                 ║
║  1. Pair-program on auth/oauth_provider.py to distribute domain knowledge.           ║
║  2. Refactor services/checkout.py into smaller single-responsibility submodules.     ║
║  3. Decouple billing/stripe.py and queue/dispatcher.py via explicit domain events.   ║
╚══════════════════════════════════════════════════════════════════════════════════════╝
```

---

<a id="static-vs-forensic"></a>
## 🔬 Static Linters vs. Forensic Git Analysis

Why do teams need **RepoPulse** if they already use SonarQube, ESLint, or Ruff?

| Diagnostic Capability | Traditional Linters (Ruff, ESLint) | SonarQube / CodeClimate | RepoPulse 🩺 |
|---|:---:|:---:|:---:|
| **Analyzes Current Syntax / Formatting** | ✅ **Yes** | ✅ **Yes** | ❌ (Out of scope) |
| **Detects Single-Author Bus Factor Risk** | ❌ No | ❌ No | ✅ **Yes** (Identifies team silos $\ge 75\%$) |
| **Predicts Bug Density via Churn Velocity** | ❌ No | ⚠️ Complexity only | ✅ **Yes** ($\text{Churn} \times \sqrt{\text{LOC}}$) |
| **Reveals Hidden Temporal Co-Change Coupling** | ❌ No | ❌ No | ✅ **Yes** (Disjoint files changing together) |
| **Zero External Dependencies / No Java** | ⚠️ Language dependent | ❌ Heavy JVM / Cloud | ✅ **Yes** (<20ms cold start, pure stdlib) |
| **Offline Git Mining in Airgapped Envs** | ✅ Local | ❌ Requires server | ✅ **Yes** (Runs directly on local Git log) |
| **Automated PR Health Score Gate (`--fail-under`)** | ⚠️ Lint only | ⚠️ Quality gate cloud | ✅ **Yes** (Native exit codes in CI) |
| **Export Formats** | Plaintext | Web Dashboard | **ANSI Dashboard, JSON, Markdown, SARIF** |

---

<a id="the-3-pillars"></a>
## 🚨 The 3 Pillars of Forensic Health

RepoPulse is built upon empirical software engineering research:

### 1. The Bus Factor & Knowledge Silo Diagnostic
> *"What happens to the codebase if your senior engineer gets hit by a bus (or gets an offer from another company)?"*

`git blame` is dangerously misleading: a line written 3 years ago might have been formatted yesterday by an auto-linter. RepoPulse analyzes **active revision ownership over time**, mapping which percentage of real architectural modifications belong to a single contributor.
- **Risk Level**: Any core file with $\ge 75\%$ contribution concentrated in a single author is automatically flagged as an active knowledge silo.

### 2. The Architectural Hotspot Law
> *Empirical research (Adam Tornhill, "Your Code as a Crime Scene") demonstrates that bugs do not distribute evenly across codebases: 80% of production defects cluster in fewer than 10% of files.*

A 2,000-line legacy file that never changes is stable and safe. A 50-line utility changed every 3 months is harmless. But a file with **both high change frequency (churn) AND substantial code size** is an active bug incubator:
$$\text{Hotspot Score} = \log(1 + \text{churn}) \times \sqrt{\text{LOC}}$$
RepoPulse surfaces these ticking time bombs so tech leads know exactly where refactoring budgets should be spent.

### 3. Temporal Co-Change Coupling
> *"Two modules with zero shared dependencies that always commit together indicate a leaky abstraction."*

If `auth/jwt.py` and `database/tenant_model.py` are modified in the exact same commit across 80% of revisions, your architecture has an undocumented dependency. Modifying one without touching the other will cause a silent runtime failure. RepoPulse identifies these hidden relationships automatically.

---

<a id="instant-audit"></a>
## ⚡ Instant Audit (Zero-Installation)

Run RepoPulse directly without installing anything via `uvx` or `pipx`:

```bash
# Run a full forensic health audit on the current repository
uvx repopulse audit

# Audit only the last 300 commits
uvx repopulse audit -n 300

# Audit changes over the past 90 days
uvx --from git-repopulse repopulse audit --since "90.days.ago"

# Inspect specific forensic sub-analyses
uvx --from git-repopulse repopulse busfactor    # Knowledge silos only
uvx --from git-repopulse repopulse hotspots      # High-churn risk files only
uvx --from git-repopulse repopulse coupling      # Hidden co-change pairs only
```

Or install globally via **pip** (provides both `repopulse` and `git-repopulse`):
```bash
pip install git-repopulse
```

---

<a id="github-actions-ci"></a>
## 🤖 GitHub Marketplace Action (CI/CD Quality Gate)

Enforce architectural health on every Pull Request. Drop RepoPulse into your `.github/workflows/code-health.yml`:

```yaml
name: Repository Health Audit

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code with full Git history
        uses: actions/checkout@v4
        with:
          fetch-depth: 0 # Required for historical Git mining

      - name: Run RepoPulse Git Forensic Audit
        uses: umutgungorr/repopulse@v1
        with:
          fail-under: 80 # Fails the PR if health score drops below 80
          summary: 'true' # Automatically appends the Health Card to PR Summary
```

### GitHub Actions Step Outputs
| Output | Description |
|---|---|
| `health-score` | Numerical health score (0–100) |
| `health-grade` | Letter grade (`A`, `B`, `C`, `D`, `F`) |
| `bus-factor-alerts` | Count of single-point-of-failure files detected |
| `hotspot-count` | Count of critical architectural hotspots |

---

<a id="cli-reference"></a>
## ⚙️ CLI Command Reference

```text
repopulse [OPTIONS] COMMAND [PATH]

COMMANDS:
  audit       Execute complete forensic audit (Health Score, Bus Factor, Hotspots, Coupling)
  busfactor   Analyze authorship concentration and knowledge silos
  hotspots    Identify high-churn files correlated with high defect rates
  coupling    Discover temporal co-change relationships between files
  summary     Output a high-level executive summary of repository vitals

OPTIONS:
  -n, --max-commits INT     Maximum historical commits to analyze (default: 500)
  --since STRING            Git date filter (e.g. "90.days.ago", "2026-01-01")
  --fail-under INT          Exit code 1 if health score is below threshold (CI gate)
  --json                    Emit machine-readable JSON for custom reporting
  --export PATH             Export formatted report to Markdown file
  --summary                 Append Markdown card to $GITHUB_STEP_SUMMARY
  --ascii                   Render using pure ASCII characters (no Unicode borders)
  --no-color                Disable ANSI color styling (honors NO_COLOR=1)
  -v, --version             Show version and exit
```

---

<a id="benchmarks"></a>
## ⚡ Performance Benchmarks

RepoPulse streams Git logs in linear $O(\text{commits})$ time, completely avoiding memory-heavy in-memory object models:

| Metric | RepoPulse | `git-fame` | `code-forensics` |
|---|:---:|:---:|:---:|
| **Cold Start Overhead** | **< 18 ms** | ~350 ms | ~4,200 ms (Java VM) |
| **Throughput (Commits/sec)** | **> 18,000 commits/s** | ~2,500 commits/s | ~1,200 commits/s |
| **RAM Footprint (50k commits)** | **< 28 MB** | ~240 MB | ~1.2 GB |
| **External Dependencies** | **0 (Pure Stdlib)** | 6 packages | Node + Java + R |

---

<a id="ecosystem"></a>
## ⚡ Part of the Developer Diagnostics Suite

RepoPulse is part of the zero-dependency **Developer Diagnostics Suite** by [@umutgungorr](https://github.com/umutgungorr):

- 🌲 **[PortTree](https://github.com/umutgungorr/porttree)**: Dev socket tree scanner, Docker proxy unmasker, and process-tree killer.
- ⚡ **[LogShrink](https://github.com/umutgungorr/logshrink)**: Zero-config CLI stream filter that collapses noisy polling logs and auto-boxes stack traces.
- 🩺 **[RepoPulse](https://github.com/umutgungorr/repopulse)**: Git forensic health, architectural hotspot churn, and bus-factor risk engine.

---

## 📖 Project Case Study

RepoPulse is an open-source project by [Umut Güngör](https://umutgungorr.com/). Read the [RepoPulse case study](https://umutgungorr.com/projects/repopulse) for its forensic Git mining methodology, bus-factor scoring, and architectural insights, along with [Designing CLI Tools That Earn Trust](https://umutgungorr.com/blog/cli-tools-that-earn-trust?lang=en).

---

<a id="contributing"></a>
## 🤝 Contributing & Community

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for development workflows and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

- **License**: MIT License ([LICENSE](LICENSE))
- **Author**: Umut Güngör
- **Repository**: [https://github.com/umutgungorr/repopulse](https://github.com/umutgungorr/repopulse)
