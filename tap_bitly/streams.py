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
"""Stream type classes for tap-bitly."""

from __future__ import annotations

import sys
from importlib import resources
from typing import TYPE_CHECKING, Any
from urllib.parse import ParseResult, parse_qs

from singer_sdk import OpenAPISchema, StreamSchema
from singer_sdk import typing as th
from singer_sdk.pagination import BaseHATEOASPaginator

from tap_bitly import openapi
from tap_bitly.client import BitlyStream

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override

if TYPE_CHECKING:
    from collections.abc import Iterable

    import requests
    from singer_sdk.helpers.types import Context


OPENAPI_SCHEMA = OpenAPISchema(resources.files(openapi) / "openapi.json")


class BitlinksPaginator(BaseHATEOASPaginator):
    """Bitlinks paginator."""

    @override
    def get_next_url(self, response: requests.Response) -> str | None:
        return response.json().get("pagination", {}).get("next") or None


class Groups(BitlyStream[Any]):
    """Users stream."""

    name = "groups"
    path = "/v4/groups"
    primary_keys = ("guid",)
    records_jsonpath = "$.groups[*]"
    replication_key = None

    schema = StreamSchema(OPENAPI_SCHEMA, key="Group")

    @override
    def get_child_context(
        self,
        record: dict[str, Any],
        context: Context | None = None,
    ) -> dict[str, Any]:
        return {"group_guid": record["guid"]}


class Bitlinks(BitlyStream[ParseResult]):
    """Bitlinks stream."""

    name = "bitlinks"
    path = "/v4/groups/{group_guid}/bitlinks"
    primary_keys = ("id",)
    records_jsonpath = "$.links[*]"
    replication_key = None
    parent_stream_type = Groups

    schema = StreamSchema(OPENAPI_SCHEMA, key="BitlinkBody")

    @override
    def get_new_paginator(self) -> BitlinksPaginator:
        return BitlinksPaginator()

    @override
    def get_url_params(
        self,
        context: Context | None,
        next_page_token: ParseResult | None,
    ) -> dict[str, Any]:
        params = {
            "archived": "both",
            "size": self._page_size,
        }
        if next_page_token:
            params.update(parse_qs(next_page_token.query))

        return params

    @override
    def get_child_context(
        self,
        record: dict[str, Any],
        context: Context | None,
    ) -> dict[str, Any]:
        return {"bitlink": record["id"]}


class BrandedShortDomains(BitlyStream[Any]):
    """Branded Short Domains stream."""

    name = "bsds"
    path = "/v4/bsds"
    primary_keys = ("domain",)

    schema = th.PropertiesList(
        th.Property(
            "domain",
            th.StringType,
            description="The branded short domain.",
            required=True,
        ),
    ).to_dict()

    @override
    def parse_response(self, response: requests.Response) -> Iterable[dict[str, Any]]:
        for bsd in response.json()["bsds"]:
            yield {"domain": bsd}


class Campaigns(BitlyStream[Any]):
    """Campaigns stream."""

    name = "campaigns"
    path = "/v4/campaigns"
    primary_keys = ("guid",)
    records_jsonpath = "$.campaigns[*]"

    schema = StreamSchema(OPENAPI_SCHEMA, key="Campaign")


class Channels(BitlyStream[Any]):
    """Channels stream."""

    name = "channels"
    path = "/v4/channels"
    primary_keys = ("guid",)
    records_jsonpath = "$.channels[*]"

    schema = StreamSchema(OPENAPI_SCHEMA, key="Channel")


class Organizations(BitlyStream[Any]):
    """Organizations stream."""

    name = "organizations"
    path = "/v4/organizations"
    primary_keys = ("guid",)
    records_jsonpath = "$.organizations[*]"

    schema = StreamSchema(OPENAPI_SCHEMA, key="Organization")

    @override
    def get_child_context(
        self,
        record: dict[str, Any],
        context: Context | None,
    ) -> dict[str, Any]:
        return {"organization_guid": record["guid"]}


class Webhooks(BitlyStream[Any]):
    """Webhooks stream."""

    name = "webhooks"
    path = "/v4/organizations/{organization_guid}/webhooks"
    primary_keys = ("guid",)
    records_jsonpath = "$.webhooks[*]"
    parent_stream_type = Organizations

    schema = StreamSchema(OPENAPI_SCHEMA, key="Webhook")


class DailyBitlinkClicks(BitlyStream[Any]):
    """Daily bitlink clicks."""

    name = "daily_bitlink_clicks"
    path = "/v4/bitlinks/{bitlink}/clicks"
    primary_keys = ("date", "bitlink")
    records_jsonpath = "$.link_clicks[*]"
    parent_stream_type = Bitlinks

    schema = th.PropertiesList(
        th.Property("clicks", th.IntegerType, description="The number of clicks."),
        th.Property("date", th.DateTimeType, description="The date."),
        th.Property("bitlink", th.StringType, description="The bitlink."),
    ).to_dict()


class MonthlyBitlinkClicks(DailyBitlinkClicks):
    """Monthly bitlink clicks."""

    name = "montly_bitlink_clicks"

    @override
    def get_url_params(
        self,
        context: Context | None,
        next_page_token: Any | None,
    ) -> dict[str, Any]:
        return {"unit": "month"}
