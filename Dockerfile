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
COPY system_issue_logger.py .

# Make sure entrypoint has execute perms
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Default entrypoint
ENTRYPOINT ["./entrypoint.sh"]
