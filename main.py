"""Entry point: run `python main.py --help` from the repository root."""

import sys
from pathlib import Path

# Make the src-layout package importable even if it has not been pip-installed.
_SRC_DIR = Path(__file__).resolve().parent / "src"
if _SRC_DIR.is_dir() and str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

from crypto_app.cli import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
