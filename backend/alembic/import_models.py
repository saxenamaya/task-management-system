"""Import all SQLAlchemy model modules so they register on Base.metadata."""

from __future__ import annotations

import importlib
import pkgutil
from pathlib import Path
import sys

BACKEND_DIR = Path(__file__).resolve().parent.parent

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


def import_all_models() -> None:
    """Discover and import every `models.py` module under `app/`."""
    import app as app_package

    for module_info in pkgutil.walk_packages(
        app_package.__path__,
        prefix=f"{app_package.__name__}.",
    ):
        if module_info.name.endswith(".models"):
            importlib.import_module(module_info.name)
