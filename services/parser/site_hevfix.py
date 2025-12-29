"""Removed parsing utilities.

The original implementation used requests, pandas and numpy to parse a
table from a remote web page. That functionality was removed from the
project; this module is left as a harmless placeholder to avoid
import-time side effects.
"""

def fetch_hev_reference_rates_removed(*args, **kwargs):
    raise RuntimeError(
        "fetch_hev_reference_rates has been removed from the project and is unavailable"
    )
