#!/usr/bin/env bash
set -euo pipefail

# 0) Mark workspace safe
git config --global --add safe.directory /workspace || git config --global --add safe.directory /data/repo

# 1) Configure SSH
mkdir -p /root/.ssh

# (The host machine will bind-mount your private key there)
# You can also add GitHub’s host key to known_hosts for strict checking:

# 2) Clone or update via SSH
if [[ ! -d "/workspace/.git" ]]; then
  git clone git@github.com:Just-Pace/system_logging.git /workspace
else
  git -C /workspace pull --rebase origin main
fi

# 3) Run your Python logger
cd /workspace
python src/system_issue_logger.py

# 4) Push back via SSH
git -C /workspace push origin main
