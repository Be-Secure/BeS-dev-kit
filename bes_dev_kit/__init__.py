"""Top-level package for BeS-dev-kit."""
# src/__init__.py

__app_name__ = "bes-dev-kit"
__version__ = "0.0.7"

(
    SUCCESS,
    DIR_ERROR,
    FILE_ERROR,
    JSON_ERROR,
    ID_ERROR,
) = range(5)

ERRORS = {
    DIR_ERROR: "config directory error",
    FILE_ERROR: "config file error",
    ID_ERROR: "to-do id error",
}
