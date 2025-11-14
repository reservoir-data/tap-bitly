#!/usr/bin/env python
# /// script
# dependencies = [
#   # renovate: datasource=pypi depName=requests
#   "requests==2.32.5",
# ]
# ///

"""Update the OpenAPI schema from the Bitly API.

Copyright (c) 2025 Edgar Ramírez-Mondragón
"""

from __future__ import annotations

import json
import pathlib

import requests

OPENAPI_URL = "https://dev.bitly.com/v4/v4.json"
PATH = "tap_bitly/openapi/openapi.json"


def main() -> None:
    """Update the OpenAPI schema from the Bitly API."""
    with pathlib.Path(PATH).open("w", encoding="utf-8") as file:
        response = requests.get(OPENAPI_URL, timeout=5)
        response.raise_for_status()
        spec = response.json()

        content = json.dumps(spec, indent=2) + "\n"
        file.write(content)


if __name__ == "__main__":
    main()
