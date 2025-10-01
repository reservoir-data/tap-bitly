"""Bitly tap class."""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING, Any

from singer_sdk import Tap
from singer_sdk import typing as th

from tap_bitly import streams

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override

if TYPE_CHECKING:
    from tap_bitly.client import BitlyStream


class TapBitly(Tap):
    """Singer tap for Bitly."""

    name = "tap-bitly"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "token",
            th.StringType,
            required=True,
            description="API Token for Bitly",
        ),
        th.Property(
            "include_paid_streams",
            th.BooleanType,
            default=False,
            description="Whether to sync paid streams",
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="Earliest datetime to get data from",
        ),
    ).to_dict()

    @override
    def discover_streams(self) -> list[BitlyStream[Any]]:
        bitly_streams = [
            streams.Groups(self),
            streams.Bitlinks(self),
            streams.BrandedShortDomains(self),
            streams.Campaigns(self),
            streams.Channels(self),
            streams.Organizations(self),
            streams.DailyBitlinkClicks(self),
            streams.MonthlyBitlinkClicks(self),
        ]

        if self.config.get("include_paid_streams"):
            bitly_streams.append(streams.Webhooks(self))

        return bitly_streams
