<div align="center">

# tap-bitly

<div>
  <a href="https://results.pre-commit.ci/latest/github/reservoir-data/tap-bitly/main">
    <img alt="pre-commit.ci status" src="https://results.pre-commit.ci/badge/github/reservoir-data/tap-bitly/main.svg"/>
  </a>
  <a href="https://github.com/reservoir-data/tap-bitly/blob/main/LICENSE">
    <img alt="License" src="https://img.shields.io/github/license/reservoir-data/tap-bitly"/>
  </a>
  <a href="https://github.com/astral-sh/ruff">
    <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json" alt="Ruff" style="max-width:100%;">
  </a>
  <a href="https://github.com/astral-sh/uv">
   <img alt="uv" src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json"/>
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
uv tool install --with tox-uv tox
```

### Create and Run Tests

Run all tests:

```bash
tox run-parallel
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

Your project comes with a custom `meltano.yml` project file already created. Go ahead and [install Meltano](https://docs.meltano.com/getting-started/installation/) if you haven't already.

1. Install all plugins

   ```bash
   meltano install
   ```

2. Check that the extractor is working properly

   ```bash
   meltano invoke tap-bitly --version
   ```

3. Execute an ELT pipeline

   ```bash
   meltano run tap-bitly target-jsonl
   ```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to
develop your own taps and targets.
