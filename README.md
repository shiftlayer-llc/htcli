# htcli

**htcli** is a command-line interface (CLI) tool for interacting with the [Hypertensor](http://github.com/hypertensor-blockchain/) ecosystem. It provides a unified terminal interface to manage subnets, interact with wallets, and retrieve chain-level data — all in a modular and developer-friendly way.

---

## 🚀 Features

- 🧠 Launch and manage Hypertensor subnets
- 🔐 Select and use wallets for operations
- 🌐 Query chain information, peers, and environment
- 🧰 Uses lightweight in-memory configuration — no files, no persistence

---

## 📁 Project Structure
```bash
htcli/
├── htcli/
│   ├── main.py                  # CLI entrypoint
│   ├── core/
│   │   └── config.py            # In-memory runtime config
│   └── commands/
│       ├── subnet.py            # Subnet commands
│       ├── wallet.py            # Wallet commands
│       └── chain.py             # Chain info
├── tests/                       # Optional unit tests
├── pyproject.toml               # Poetry config & metadata
├── README.md                    # Project README file
```

## 📦 Installation

### From PyPI (after release)
```bash
pip install htcli
```

### From source (with Poetry)
```bash
git clone https://github.com/shiftlayer-llc/htcli.git
cd htcli
poetry install
```

Run the CLI:
```bash
poetry run htcli --help
```
or simply run:
```bash
htcli --help
```

## 🧑‍💻 CLI Usage
### Subnet Commands
```bash
htcli subnet info
```
### Wallet Commands
```bash
htcli wallet create
```
### Chain Commands
```bash
htcli chain info
```

Each command provides `--help`:
```bash
htcli subnet --help
```

## ⚙️ Configuration

htcli uses a pure in-memory configuration model that resets between sessions. This makes it ideal for quick, ephemeral workflows.
You can set values like the wallet or environment using CLI options:
```bash
htcli subnet activate --env testnet --wallet.name alice
```
The selected values remain accessible to subsequent commands in the session through a shared internal runtime config.

## 🧪 Testing
Run tests with:
```bash
pytest
```