# Copyright 2025 Edgar Ramirez
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
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
