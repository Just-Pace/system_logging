# Use a minimal Python base
FROM python:3.11-slim

# Install Git and GPG
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      git \
      gnupg \
 && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy in your logger script
COPY src/system_issue_logger.py .

# Make sure entrypoint has execute perms
COPY scripts/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x entrypoint.sh

COPY scripts/log-issue /usr/local/bin/log-issue
RUN chmod +x /usr/local/bin/log-issue

# Default entrypoint
WORKDIR /workspace
ENTRYPOINT [".scripts/entrypoint.sh"]
