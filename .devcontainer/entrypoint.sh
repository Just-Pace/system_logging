#!/usr/bin/env bash
set -euo pipefail

# ----------------------------------------------------------------
# 1) If you’ve passed in GITHUB_USER + GITHUB_PAT, bake them into
#    a .git-credentials file for Git’s store helper to pick up.
# ----------------------------------------------------------------
if [[ -n "${USER:-}" && -n "${PAT:-}" ]]; then
  cat > /root/.git-credentials <<EOF
https://${USER}:${PAT}@github.com
EOF
  chmod 600 /root/.git-credentials
  git config --global credential.helper store
fiif [[ -n "${USER:-}" && -n "${PAT:-}" ]]; then
  cat > /root/.git-credentials <<EOF
https://${USER}:${PAT}@github.com
EOF
  chmod 600 /root/.git-credentials
  git config --global credential.helper store
  
fi

# ----------------------------------------------------------------
# 2) SSH fallback (if you also mounted /root/.ssh/id_ed25519)
# ----------------------------------------------------------------
if [[ -f "/root/.ssh/id_ed25519" ]]; then
  mkdir -p /root/.ssh
  chmod 700 /root/.ssh
  chmod 600 /root/.ssh/id_ed25519
  ssh-keyscan github.com >> /root/.ssh/known_hosts 2>/dev/null || true
  export GIT_SSH_COMMAND='ssh -i /root/.ssh/id_ed25519 -o UserKnownHostsFile=/root/.ssh/known_hosts'
fi

if [[ ! -d "/data/repo/.git" ]]; then
  git clone git@github.com:Just-Pace/system_logging.git /data/repo
else
  cd /data/repo
  git pull --rebase origin main
fiif [[ -f "/root/.ssh/id_ed25519" ]]; then
  mkdir -p /root/.ssh
  chmod 700 /root/.ssh
  chmod 600 /root/.ssh/id_ed25519
  ssh-keyscan github.com >> /root/.ssh/known_hosts 2>/dev/null || true
  export GIT_SSH_COMMAND='ssh -i /root/.ssh/id_ed25519 -o UserKnownHostsFile=/root/.ssh/known_hosts'
fi

# ----------------------------------------------------------------
# 3) Clone or pull your repo
# ----------------------------------------------------------------
if [[ ! -d "/data/repo/.git" ]]; then
  git clone https://github.com/Just-Pace/system_logging.git /data/repo
else
  cd /data/repo
  git pull --rebase origin main
fi

cd /data/repo

# ----------------------------------------------------------------
# 4) Run the Python logger
# ----------------------------------------------------------------
python /app/system_issue_logger.py

# ----------------------------------------------------------------
# 5) Push any new commits
# ----------------------------------------------------------------
git push origin main
