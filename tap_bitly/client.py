"""REST client handling, including BitlyStream base class."""

from __future__ import annotations

import sys
from typing import Generic, TypeVar

from singer_sdk import RESTStream
from singer_sdk.authenticators import BearerTokenAuthenticator

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override


_T = TypeVar("_T")


class BitlyStream(RESTStream[_T], Generic[_T]):
    """Bitly stream class."""

    url_base = "https://api-ssl.bitly.com"
    records_jsonpath = "$[*]"
    _page_size = 100

    @override
    @property
    def authenticator(self) -> BearerTokenAuthenticator:
        return BearerTokenAuthenticator(token=self.config["token"])
