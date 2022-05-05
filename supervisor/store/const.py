"""Constants for the add-on store."""
from enum import Enum


class StoreType(str, Enum):
    """Store Types."""

    CORE = "core"
    LOCAL = "local"
    GIT = "git"
    CASAI = "https://github.com/casai-org/cerebro-addons"
