#!/usr/bin/env python3
"""
system_issue_logger.py
A streamlined, persistent-clone system issue logger with encrypted log entries and audit trail.
"""
import os
import csv
import subprocess
import sys
import getpass
from datetime import datetime

# === CONFIGURATION ===
REPO_PATH = os.getenv("REPO_PATH", "/workspace")
USER_NAME = os.getenv("LOGGER_USER", getpass.getuser())
USER_EMAIL = os.getenv("LOGGER_EMAIL", f"{getpass.getuser()}@example.com")


def get_passphrase():
    # First, try environment variable
    pw = os.getenv("LOG_PW")
    if pw:
        return pw
    # Fallback to interactive prompt
    while True:
        pw = getpass.getpass("Enter GPG passphrase: ")
        if pw:
            return pw
        print("Passphrase cannot be empty.")


def ensure_repo_up_to_date():
    # Pull latest changes and ensure we're on main
    subprocess.run([
        "git", "-C", REPO_PATH,
        "pull", "--rebase", "origin", "main"
    ], check=True)


def append_csv_entry(entry, filename="system_issue_log.csv"):
    # Safely append to CSV, replacing invalid characters
    path = os.path.join(REPO_PATH, filename)
    log_exists = os.path.exists(path)
    with open(path, 'a', newline='', encoding='utf-8', errors='replace') as f:
        writer = csv.writer(f)
        if not log_exists:
            writer.writerow([
                "Date", "System Node", "Issue Observed",
                "Root Cause", "Remedial Action",
                "Status", "Comments", "Tags"
            ])
        # Replace invalid surrogates before writing
        safe_entry = [str(item).encode('utf-8', 'replace').decode('utf-8') for item in entry]
        writer.writerow(safe_entry)


def encrypt_csv(filename="system_issue_log.csv", enc_file="system_issue_log.csv.gpg"):
    # Encrypt plaintext CSV into GPG file
    pw = get_passphrase()
    subprocess.run([
        "gpg", "--batch", "--yes", "--passphrase", pw,
        "--symmetric", "--cipher-algo", "AES256",
        "-o", enc_file, filename
    ], check=True)


def append_audit_log(entry, filename=".audit.log"):
    # Append to audit log, replacing invalid characters
    path = os.path.join(REPO_PATH, filename)
    with open(path, 'a', encoding='utf-8', errors='replace') as f:
        safe_entry = str(entry).encode('utf-8', 'replace').decode('utf-8')
        f.write(f"[{datetime.now().isoformat()}] {safe_entry}\n")


def git_commit_and_push():
    # Configure local Git identity
    subprocess.run(["git", "-C", REPO_PATH, "config", "user.name", LOGGER_USERUSER], check=True)
    subprocess.run(["git", "-C", REPO_PATH, "config", "user.email", LOGGER_EMAIL], check=True)

    # Stage encrypted log and audit trace
    subprocess.run(["git", "-C", REPO_PATH, "add", "system_issue_log.csv.gpg", ".audit.log"], check=True)
    msg = f"[secure-log] entry added: {datetime.now().isoformat()}"
    subprocess.run(["git", "-C", REPO_PATH, "commit", "-m", msg], check=True)
    subprocess.run(["git", "-C", REPO_PATH, "push", "origin", "main"], check=True)


def run_logger():
    # Ensure working copy is up to date
    ensure_repo_up_to_date()
    print("Enter system issue details (leave blank to accept defaults):\n")

    today = datetime.today().strftime('%Y-%m-%d')
    date_str = input(f"Date [{today}]: ") or today
    node    = input("System Node: ").strip()
    issue   = input("Issue Observed: ").strip()
    cause   = input("Root Cause (if known): ").strip()
    action  = input("Remedial Action Taken: ").strip()
    status  = input("Status (Open/In Progress/Mitigated/Closed): ").strip()
    comments= input("Comments: ").strip()
    tags    = input("Tags (comma-separated): ").strip()

    entry = [date_str, node, issue, cause, action, status, comments, tags]
    append_csv_entry(entry)

    # Change to repo path for encryption
    cwd = os.getcwd()
    os.chdir(REPO_PATH)
    encrypt_csv()
    append_audit_log(f"Logged issue for {node or '<no-node>'} by {USER_NAME}")
    git_commit_and_push()
    print("Log entry encrypted and pushed successfully.")
    os.chdir(cwd)


if __name__ == "__main__":
    run_logger()
