<div align="center">

# tap-bitly

<div>
  <a href="https://results.pre-commit.ci/latest/github/edgarrmondragon/tap-bitly/main">
    <img alt="pre-commit.ci status" src="https://results.pre-commit.ci/badge/github/edgarrmondragon/tap-bitly/main.svg"/>
  </a>
  <a href="https://github.com/edgarrmondragon/tap-bitly/blob/main/LICENSE">
    <img alt="License" src="https://img.shields.io/github/license/edgarrmondragon/tap-bitly"/>
  </a>
  <a href="https://github.com/astral-sh/ruff">
    <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json" alt="Ruff" style="max-width:100%;">
  </a>
</div>

Singer tap for [Bitly](https://bitly.com/). Built with the [Meltano Singer SDK](https://sdk.meltano.com).

</div>

## Capabilities

* `catalog`
* `state`
* `discover`
* `about`
* `stream-maps`
* `schema-flattening`

## Settings

| Setting              | Required | Default | Description                                                                                                                                 |
| :------------------- | :------: | :-----: | :------------------------------------------------------------------------------------------------------------------------------------------ |
| token                |   True   |  None   | API Token for Bitly                                                                                                                         |
| include_paid_streams |  False   |  False  | Whether to sync paid streams                                                                                                                |
| start_date           |  False   |  None   | Earliest datetime to get data from                                                                                                          |
| stream_maps          |  False   |  None   | Config object for stream maps capability. For more information check out [Stream Maps](https://sdk.meltano.com/en/latest/stream_maps.html). |
| stream_map_config    |  False   |  None   | User-defined config values to be used within map expressions.                                                                               |
| flattening_enabled   |  False   |  None   | 'True' to enable schema flattening and automatically expand nested properties.                                                              |
| flattening_max_depth |  False   |  None   | The max depth to flatten schemas.                                                                                                           |

## Supported Streams

| Stream Name              | Endpoint                                                                                           | Notes                 |
| :----------------------- | :------------------------------------------------------------------------------------------------- | :-------------------- |
| `groups`                 | [/v4/groups](https://dev.bitly.com/api-reference/#getGroups)                                       |                       |
| `bitlinks`               | [/v4/groups/{group_guid}/bitlinks](https://dev.bitly.com/api-reference/#getBitlinksByGroup)        |                       |
| `bsds`                   | [/v4/bsds](https://dev.bitly.com/api-reference/#getBSDs)                                           |                       |
| `campaigns`              | [/v4/campaigns](https://dev.bitly.com/api-reference/#getCampaigns)                                 |                       |
| `channels`               | [/v4/channels](https://dev.bitly.com/api-reference/#getChannels)                                   |                       |
| `organizations`          | [/v4/organizations](https://dev.bitly.com/api-reference/#getOrganizations)                         |                       |
| `webhooks`               | [/v4/organizations/{organization_guid}/webhooks](https://dev.bitly.com/api-reference/#getWebhooks) | Requires paid account |
| `daily_bitlink_clicks`   | [/v4/bitlinks/{bitlink}/clicks](https://dev.bitly.com/api-reference/#getClicksForBitlink)          |                       |
| `monthly_bitlink_clicks` | [/v4/bitlinks/{bitlink}/clicks](https://dev.bitly.com/api-reference/#getClicksForBitlink)          |                       |

A full list of supported settings and capabilities is available by running: `tap-bitly --about`

### Source Authentication and Authorization

Generate an access token from the [Bitly API Console](https://app.bitly.com/settings/api/).

## Usage

You can easily run `tap-bitly` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Tap Directly

```bash
tap-bitly --version
tap-bitly --help
tap-bitly --config CONFIG --discover > ./catalog.json
```

## Developer Resources

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Create and Run Tests

Create tests within the `tests` subfolder and then run:

```bash
poetry run pytest
```

You can also test the `tap-bitly` CLI interface directly using `poetry run`:

```bash
poetry run tap-bitly --help
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

Install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
pipx install meltano
# Initialize meltano within this directory
cd tap-bitly
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke tap-bitly --version
# OR run a test `elt` pipeline:
meltano elt tap-bitly target-jsonl
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to
develop your own taps and targets.
