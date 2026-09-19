import sys
from pathlib import Path

# No pyproject.toml/pytest.ini exists yet anywhere in the repo, so make sure
# `backend/` (which contains the `app` package) is importable regardless of
# the directory pytest is invoked from.
BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
