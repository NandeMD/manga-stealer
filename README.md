# Manga Stealer

A command‑line tool to download webtoon/manga from various sources.

## Installation

### Prerequisites

- **Git**  
  - Windows: Download and install from https://git-scm.com/download/win  
  - macOS:  
    ```bash
    brew install git
    ```  
  - Ubuntu/Linux:  
    ```bash
    sudo apt update && sudo apt install git
    ```

- **uv**  
  - Windows (enter these commands to terminal/cmd):
    ```powershell
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```
  - MacOS & Linux (enter these commands to terminal):
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh

    # Or if you don't have curl:
    wget -qO- https://astral.sh/uv/install.sh | sh
    ```

### Clone the repository

```bash
git clone https://github.com/NandeMD/manga-stealer.git
cd manga-stealer
```

### Install dependencies

Option 1: Sync with UV (Recommended)

```bash
uv sync
```

Option 2: Install the package directly

```bash
pip install .
```

## Usage

```bash
uv run main.py <source_url> [options]
```

Options:

- `-o`, `--output`  Specify the output directory (default: current directory)  
- `-c`, `--chapters`  Select chapters as `start:end` (e.g. `12:22.5`) or `all` (start is inclusive, end is exclusive)

Example:

```bash
uv run main.py  https://asuracomic.net/series/genius-prismatic-mage-b20baf26 \
  -o ./downloads \
  -c 1:10
```

This will download chapters 1 through 9 of **Genius Prismatic Mage** into `./downloads/Genius-Prismatic-Mage`.

## License

MIT License. See [LICENSE](LICENSE) for details.