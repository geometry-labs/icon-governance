<p align="center">
  <h2 align="center">ICON Governance Service</h2>
</p>

[![loopchain](https://img.shields.io/badge/ICON-API-blue?logoColor=white&logo=icon&labelColor=31B8BB)](https://shields.io) [![GitHub Release](https://img.shields.io/github/release/geometry-labs/icon-governance.svg?style=flat)]() ![](https://github.com/geometry-labs/icon-governance/workflows/push-main/badge.svg?branch=main) [![codecov](https://codecov.io/gh/geometry-labs/icon-governance/branch/main/graph/badge.svg)](https://codecov.io/gh/geometry-labs/icon-governance) ![](https://img.shields.io/docker/pulls/geometrylabs/icon-governance-api.svg) ![](https://img.shields.io/github/license/geometry-labs/icon-governance)

Off chain indexer for the ICON Blockchain serving the **governance** context of the [icon-explorer](https://github.com/geometry-labs/icon-explorer). Service is broken up into API and worker components that are run as individual docker containers. It depends on data coming in from [icon-etl](https://github.com/geometry-labs/icon-etl) over a Kafka message queue with persistence on a postgres database.


### Endpoints

TODO: Links and table

### Deployment

Service can be run in the following ways:

1. Independently from this repo with docker compose:
```bash
docker-compose -f docker-compose.db.yml -f docker-compose.yml up -d
# Or alternatively
make up
```

2. With the whole stack from the main [icon-explorer]() repo.

3. With the helm chart.

**Please note this is for advanced users who are capable of setting external DBs / Strimzi and configuring them properly.**

TODO:

```bash
helm add
helm install
```

Run `make help` for more options.

### Development

For local development, you will want to run the `docker-compose.db.yml` as you develop. To run the tests,

```bash
make test
```

### License

Apache 2.0
