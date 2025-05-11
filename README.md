# 🛡️ Secure System Issue Logger

A tamper-resistant, version-controlled system issue logging tool built with Git, Docker, and GPG encryption. Designed for high-integrity operational environments where auditability, traceability, and minimal attack surface are required.

---

## 🔍 Purpose

Traditional logging tools or spreadsheets are easy to overwrite or falsify. This tool provides a structured, secure, and traceable method for logging system issues — ideal for:

- Technical audit preparation
- Aerospace/defense subsystems
- Manufacturing test benches
- Environments with insider threat concerns

---

## 🔧 How It Works

1. **Run the container** via a single command or shortcut (`log-issue`)
2. The container:
   - Clones the repo via SSH
   - Pulls latest changes with rebase and autostash
   - Prompts for log entry input (CSV format)
   - Appends to `system_issue_log.csv` and `.audit.log`
   - Encrypts `system_issue_log.csv` using GPG + `LOG_PW`
   - Auto-commits and pushes back to GitHub

3. **Audit log** tracks each submission with timestamps and usernames
4. **Encrypted logs** ensure that only authorized viewers can read the contents
5. **Force-pushes** to a mirror repo (optional) for redundancy

---

## 📦 Key Features

| Feature                    | Description                                                   |
|----------------------------|---------------------------------------------------------------|
| 🔐 GPG Encryption          | CSV log entries are symmetrically encrypted before push       |
| 🔁 Auto Commit & Push      | All writes are tracked, committed, and published via Git      |
| 🪪 SSH-Based Auth          | No passwords or HTTPS — clean agent-forwarded SSH only        |
| 🐳 Dockerized              | No local installs; containerized for consistency & isolation  |
| 💥 Self-Destructs          | Container exits and leaves no secret data behind              |
| ✅ Git Safe Directory      | Avoids Git errors inside container (safe.directory applied)   |
| 🔁 Auto-Rebase Pull        | Prevents diverging history when collaborating                 |

---

## 🚀 Quick Start

### 1. Build the image

```bash
docker build -t yourname/secure-logger:latest .
