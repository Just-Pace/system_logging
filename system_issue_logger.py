#!/usr/bin/env python3
"""
secure_issue_logger_refactored.py
A streamlined, persistent-clone system issue logger with encrypted log entries and audit trail.
"""
import getpass
import os
import csv
import subprocess
import sys
from datetime import datetime

def ensure_git_repo():
    # Pull latest changes and ensure we're on main
    subprocess.run(["git", "pull", "origin", "main"], check=True)


def append_csv_entry(entry, filename="system_issue_log.csv"):
    # Append to local CSV (not committed)
    log_exists = os.path.exists(filename)
    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        if not log_exists:
            writer.writerow([
                "Date", "System Node", "Issue Observed",
                "Root Cause", "Remedial Action",
                "Status", "Comments", "Tags"
            ])
        writer.writerow(entry)


def encrypt_csv(filename="system_issue_log.csv", enc_file="system_issue_log.csv.gpg"):
    # Encrypt plaintext CSV into GPG file; requires LOG_PW env var
    pw = os.getenv("LOG_PW")
    if not pw:
         # fall back to interactive prompt
        pw = getpass.getpass("Enter GPG passphrase: ")
        sys.exit(1)
    subprocess.run([
        "gpg", "--batch", "--yes", "--passphrase", pw,
        "--symmetric", "--cipher-algo", "AES256",
        "-o", enc_file, filename
    ], check=True)


def append_audit_log(entry, filename=".audit.log"):
    with open(filename, 'a') as f:
        f.write(f"[{datetime.now().isoformat()}] {entry}\n")


def git_commit_and_push():
    # Stage encrypted log and audit trace
    subprocess.run(["git", "add", "system_issue_log.csv.gpg", ".audit.log"], check=True)
    msg = f"[secure-log] entry added: {datetime.now().isoformat()}"
    subprocess.run(["git", "commit", "-m", msg], check=True)
    subprocess.run(["git", "push", "origin", "main"], check=True)


def run_logger():
    ensure_git_repo()
    print("Enter system issue details (leave blank to accept defaults):\n")

    # Interactive prompts
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
    # Write and encrypt
    append_csv_entry(entry)
    encrypt_csv()

    # Audit and push
    append_audit_log(f"Logged issue for {node} by {os.getlogin()}")
    git_commit_and_push()
    print("Log entry encrypted and pushed successfully.")


if __name__ == "__main__":
    run_logger()

