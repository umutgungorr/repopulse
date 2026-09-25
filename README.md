# 🩺 RepoPulse

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://python.org)
[![Dependencies: 0](https://img.shields.io/badge/Dependencies-Zero-orange.svg)](pyproject.toml)
[![Git Powered](https://img.shields.io/badge/Git-Native%20Engine-black.svg)](https://git-scm.com)

> **Zero-dependency Git forensic health, architectural hotspot churn, and bus-factor risk engine.**

RepoPulse mines your repository's native Git history to uncover hidden architectural debt, team knowledge silos, and co-change coupling before they turn into production incidents.

---

## 🌟 Key Capabilities

- 🚨 **Bus Factor & Knowledge Silo Alerts**: Identifies critical files with $\ge 75\%$ contribution concentrated in a single author who might leave or be out of office.
- 🔥 **Architectural Hotspots (Churn + Complexity)**: Detects code areas that change most frequently with high net line volume (high bug density correlation).
- 🔗 **Temporal Coupling (Hidden Dependencies)**: Pinpoints pairs of files that unexpectedly commit together in $\ge 50\%$ of revisions, revealing architectural leaks.
- ⚡ **Zero External Dependencies**: Powered solely by Python's built-in standard library. No pandas, no gitpython, no C-extensions required.
- 🛡️ **CI/CD Quality Gate**: Set a hard threshold with `--fail-under 75` to break builds if codebase health drops.
- 📊 **Multi-Format Output**: Rich colorized terminal dashboard, machine-readable JSON, or PR-ready Markdown tables.

---

## 🚀 Installation

```bash
pip install repopulse
```

Or run directly with `uvx` / `pipx`:

```bash
uvx repopulse audit .
```

---

## 💻 CLI Usage

### 1. Basic Health Audit
```bash
# Audit the current repository
repopulse audit .

# Audit a specific repo path
repopulse audit /path/to/my-repo
```

### 2. Time and Commit Window Filters
```bash
# Analyze only the last 200 commits
repopulse audit . -n 200

# Analyze commits from the past 6 months
repopulse audit . --since "6.months.ago"
```

### 3. CI/CD Pipeline Gate
```bash
# Break build if overall health score is below 70
repopulse audit . --fail-under 70
```

### 4. Export to Markdown (PR Comments / Wikis)
```bash
repopulse audit . --format markdown -o audit-report.md
```

### 5. Export to JSON (Automations & Dashboards)
```bash
repopulse audit . --format json -o health-metrics.json
```

---

## 📊 Sample Terminal Output

```text
🩺 RepoPulse - Git Forensic Health & Knowledge Silo Audit
============================================================================
Target Repository: my-project
Overall Health Score: 85 / 100 (HEALTHY)
Vitals: 342 commits | 8 author(s) | 94 active day(s)
----------------------------------------------------------------------------

🚨 Bus Factor & Knowledge Silo Alerts:
Concentration   Revisions   Top Author           File Path
----------------------------------------------------------------------------
88.5% solo      26          Alice Smith          src/auth/jwt_tokens.py
82.0% solo      18          Bob Jones            src/database/migrations.py

🔥 Architectural Hotspots (High Churn + Complexity):
Risk Level   Churn    Size (loc)   File Path
----------------------------------------------------------------------------
[HIGH]       34       450          src/api/routes/billing.py
[MEDIUM]     19       280          src/services/webhook.py

🔗 Temporal Coupling (Implicit Dependencies):
Co-Changes   Coupling %   Connected File Pair
----------------------------------------------------------------------------
14           82.4%        src/models/user.py <--> src/services/auth.py
```

---

## 📄 License

MIT License &copy; 2026 Umut Güngör
