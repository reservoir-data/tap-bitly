#!/usr/bin/env python

"""Update the OpenAPI schema from the Bitly API.

Copyright (c) 2025 Edgar Ramírez-Mondragón
"""

from __future__ import annotations

import json
import pathlib
import urllib.request


def main() -> None:
    """Update the OpenAPI schema from the Bitly API."""
    with (
        pathlib.Path("tap_bitly/openapi/openapi.json").open("w") as f_out,
        urllib.request.urlopen("https://dev.bitly.com/v4/v4.json") as f_req,
    ):
        spec = json.load(f_req)
        content = json.dumps(spec, indent=2) + "\n"
        f_out.write(content)


if __name__ == "__main__":
    main()
