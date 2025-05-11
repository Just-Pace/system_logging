#!/usr/bin/env bash
set -euo pipefail

# 0) Mark workspace safe
git config --global --add safe.directory /workspace || git config --global --add safe.directory /data/repo

# 1) Configure SSH
mkdir -p /root/.ssh

# 2) Clone or update via SSH
if [[ ! -d "/workspace/.git" ]]; then
  git clone git@github.com:Just-Pace/system_logging.git /workspace
else
  git -C /workspace pull --rebase --autostash origin main
fi

# 3) Run your Python logger
cd /workspace
python src/system_issue_logger.py

# 4) Stage and commit log files
cd /workspace
git add system_issue_log.csv .audit.log

# Only commit if there are staged changes
if ! git diff --cached --quiet; then
  git commit -m "[log] entry added: $(date -Iseconds)"
fi

# 5) Push back via SSH
git push origin main
