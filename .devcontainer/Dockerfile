# Use a minimal Python base
FROM python:3.11-slim
# … earlier in your Dockerfile …
RUN apt-get update \
 && apt-get install -y git gnupg openssh-client \
 # Pre-create root’s SSH folder
 && mkdir -p /root/.ssh \
 && chmod 700 /root/.ssh \
 # Add GitHub’s host key so ssh never prompts
 && ssh-keyscan github.com >> /root/.ssh/known_hosts \
 && chmod 644 /root/.ssh/known_hosts \
 && rm -rf /var/lib/apt/lists/*
# Set workdir
#WORKDIR /app

# Copy in your logger script
COPY src/system_issue_logger.py .

# Make sure entrypoint has execute perms
COPY scripts/entrypoint.sh /usr/local/bin/entrypoint.sh
# Make sure entrypoint has execute perms
RUN chmod +x /usr/local/bin/entrypoint.sh

COPY scripts/log-issue /usr/local/bin/log-issue
RUN chmod +x /usr/local/bin/log-issue

# Default entrypoint
WORKDIR /workspace
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
