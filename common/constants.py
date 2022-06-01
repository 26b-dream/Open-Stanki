from __future__ import annotations

# Common
from common.extended_path import ExtendedPath

# Unknown

# Update the value to use ExtendedPath instead of a regular path
BASE_DIR = ExtendedPath(__file__).parent.parent
DOWNLOADED_FILES_DIR = BASE_DIR / "downloaded_files"
