# Secure System Logger

Production-grade issue tracking infrastructure with encryption, version control, and container deployment for test bench operations.

## Overview

Enterprise logging system designed for aerospace test environments requiring:
- **Audit trail compliance** (AS9100, ISO 9001)
- **Data security** (GPG encryption for sensitive operational logs)
- **Version control** (Git commits for immutable history)
- **Portable deployment** (Docker containerization)
- **CI/CD automation** (GitHub Actions testing)

## Architecture
```
system-logger/
├── src/                      # Core logging engine
│   └── secure_logger.py      # CSV append + GPG encrypt + Git commit
├── scripts/                  # Deployment entrypoints
│   ├── entrypoint.sh         # Docker/container launcher
│   └── log-issue             # Host-based CLI
├── .devcontainer/            # VS Code remote development
│   ├── Dockerfile
│   └── devcontainer.json
├── .github/workflows/        # CI/CD automation
│   └── log-issue.yml
├── docker/                   # Container orchestration
│   ├── docker-compose.yml
│   └── docker-compose.debug.yml
├── tests/                    # Unit and integration tests
│   └── test_secure_logger.py
└── docs/                     # Architecture documentation
    └── architecture.md
```

## Features

### Core Functionality
- **Structured CSV logging**: Timestamp, category, issue description, operator ID
- **GPG encryption**: Automatic encryption of sensitive entries
- **Git version control**: Every log entry creates atomic commit
- **Immutable audit trail**: Tamper-evident history via Git SHA verification

### DevOps Infrastructure
- **Docker containerization**: Reproducible deployment across test benches
- **GitHub Actions CI**: Automated testing on every commit
- **VS Code devcontainer**: Consistent development environment
- **Debug configurations**: Integrated debugging support

### Production Hardening
- **Error handling**: Graceful failure modes with operator feedback
- **Input validation**: Schema enforcement before commit
- **Rollback capability**: Git revert for error correction
- **Multi-user support**: Concurrent logging with merge conflict resolution

## Use Case

Originally developed for systematic issue tracking in aerospace production test environment (2022-2025):

**Problem:** Test bench issues logged in Excel spreadsheets, no version control, no encryption, no audit trail

**Solution:** Automated logging system that:
1. Operator runs `log-issue` command
2. Enters: timestamp (auto), category (dropdown), description, operator ID
3. System appends to CSV, encrypts sensitive entries (GPG), commits to Git
4. Result: Immutable, encrypted, version-controlled audit trail

**Impact:**
- Root-cause analysis via Git history (when did issue first appear?)
- Compliance evidence for AS9100 audits (tamper-evident logs)
- Trend analysis via CSV export (most common failure modes)
- Security for proprietary test data (GPG encryption)

## Technical Stack

- **Python 3.x**: Core logging engine
- **Docker & Docker Compose**: Containerization
- **GPG (GnuPG)**: Encryption
- **Git**: Version control and audit trail
- **GitHub Actions**: CI/CD
- **Shell scripting**: Deployment automation

## Quick Start

### Docker Deployment (Recommended)
```bash
docker-compose up -d
docker exec -it system-logger ./scripts/log-issue
```

### Host Execution
```bash
./scripts/log-issue
# Follow prompts: category, description, operator ID
```

### Development (VS Code)
1. Open folder in VS Code
2. Click "Reopen in Container"
3. Run tests: `python -m pytest tests/`

## Configuration

Edit `config/` files for:
- GPG key ID (for encryption)
- Git remote repository (for centralized log backup)
- Category dropdown options (customize for your environment)
- CSV schema (add custom fields)

## Production Context

**Development period:** 2022-2025  
**Environment:** Aerospace test bench operations  
**Status:** Production-tested in AS9100-certified facility  
**License:** MIT (personal project, not company IP)

Built on personal time to solve systematic problem: test bench issues were lost in email threads and Excel files. This infrastructure enables:
- Traceability for compliance audits
- Root-cause analysis for recurring failures  
- Trend visibility for process improvement
- Security for sensitive operational data

Generic infrastructure pattern - no proprietary test procedures or customer data included.

## Author

**Andile Mjwara**  
[github.com/andilemj](https://github.com/andilemj)

## Languages

- Python: 64.9%
- Shell: 20.9%
- Dockerfile: 14.2%

---

*Built to demonstrate systematic approach to test bench infrastructure, DevOps practices, and security-conscious data handling in production aerospace environment.*
