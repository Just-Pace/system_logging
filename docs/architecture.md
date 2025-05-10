system-logger/
├── src/                           # Your Python package
│   └── secure_logger.py          # Core logic: CSV append, GPG encrypt, Git commit/push
│
├── scripts/                       # Thin wrappers & entrypoints
│   ├── entrypoint.sh              # Docker/container entrypoint: credentials + exec
│   └── log-issue                  # Host launcher: docker run … or SSH command
│
├── .devcontainer/                 # VS Code / Codespaces config
│   ├── Dockerfile                 # Builds container with git, gpg, python, scripts/
│   └── devcontainer.json          # Mounts workspace, injects secrets, exposes log-issue
│
├── .github/                       # CI / Actions
│   └── workflows/
│       └── log-issue.yml          # workflow_dispatch → pulls image → runs logger
│
├── docker/                        # (Optional) Docker Compose for local dev
│   ├── docker-compose.yml
│   └── docker-compose.debug.yml
│
├── tests/                         # Unit and smoke tests against src/ only
│   └── test_secure_logger.py
│
├── docs/
│   └── architecture.md            # Diagram + explanation of this layout
│
├── .gitignore
├── .dockerignore
├── README.md
└── LICENSE
