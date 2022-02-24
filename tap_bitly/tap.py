"""Bitly tap class."""

from typing import List, Type

from singer_sdk import Stream, Tap
from singer_sdk import typing as th
from singer_sdk.streams import RESTStream

from tap_bitly.streams import (
    Bitlinks,
    BrandedShortDomains,
    Campaigns,
    DailyBitlinkClicks,
    Groups,
    MonthlyBitlinkClicks,
    Organizations,
    Webhooks,
)

STREAM_TYPES: List[Type[RESTStream]] = [
    Bitlinks,
    BrandedShortDomains,
    Campaigns,
    Groups,
    Organizations,
    Webhooks,
    DailyBitlinkClicks,
    MonthlyBitlinkClicks,
]


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
            "start_date",
            th.DateTimeType,
            description="Earliest datetime to get data from",
        ),
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams.

        Returns:
            A list of Bitly streams.
        """
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]
