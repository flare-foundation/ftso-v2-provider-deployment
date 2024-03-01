# FTSO V2 Overview

![Overview](Overview.png)

A data provider system for FTSOv2 consists of the following components:

1. **Flare System Client**. Responsible for all interactions with the FTSOv2 smart contracts, including data collection and submission, voter registration, and additional system tasks.
2. **Data Provider**. Provides commit, reveal, and median result data to System Client for submission.
3. **Feed Value Provider**. Provides current values (prices) for a given set of feeds.
4. **Indexer**. Monitors the blockchain and records all FTSOv2 related transactions and events.

Reference implementations are provided for **Indexer**, **Flare System Client**, **Data Provider**, and providers are expected to plug in their own **Feed Value Provider** implementing a specific REST API (there is an sample implementation for testing).

## Operation

The following is a very simplified description of a single voting round operation.

**System Client** runs a scheduler which triggers voting actions every round (90s):
- On voting round start, obtain reveal data for the previous round from **Data Provider** and send to `Submission` smart contract.
- Once the reveal deadline passes (45s), obtain median result Merkle root from **Data Provider**, sign, and send to `Submission` smart contract. 
- Before the end of the voting round, obtain a feed value commit hash for the current round from the **Data Provider** (which will get processed in the following round).
- There is finalizer process which monitors the indexer database for signature transactions, and once enough signature weight for a voting round is gathered, submits the set of signatures to the `Relay` smart contract. If signature verification passes, the voting round is considered finalized. The `Relay` contract is the authoritative storage of confirmed voting round result Merkle roots.

Additionally, once in a reward epoch the **System Client** triggers voter registration, which allows participating in the following reward epoch.

**Data Provider** obtains all commit and reveal data straight from encoded transaction calldata recored in the indexer database. All calls to `Submission` contract ar simply empty function invocations, with the actual submission data provided as additional calldata on the transaction.

# Deployment

## Account preparation

TODO

## Dependencies

You will need:
- [jq](https://jqlang.github.io/jq/)
    - `brew install jq`
    - `apt-get install jq`
    - `pacman -S jq`
- [envsubst](https://www.gnu.org/software/gettext/manual/html_node/envsubst-Invocation.html)
    - (macOS only) `brew install gettext`
- [docker](https://www.docker.com/)

## Set up repos and docker images

- You will need a gitlab user with access to following repositories until they are made public:
    - [ftso-scaling](https://gitlab.com/flarenetwork/ftso-scaling)
    - [flare-system-client](https://gitlab.com/flarenetwork/flare-system-client)
    - [flare-system-c-chain-indexer](https://gitlab.com/flarenetwork/flare-system-c-chain-indexer)

- Use `.env.example` to create `.env` file, eg.: using `cp .env.example .env`

- Use `./repos pull` to clone (first time) or pull (when cloned directories exist) projects. If you switch branches in .env file or you get errors while using `./repos pull` command, use `./repos clean` to delete files followed by `./repos pull` to clone them again. 

- Use `./build.sh` to build docker images for all projects.

## Start provider stack

Using `./run run` 4 services will start:
- c-chain-indexer-db
- c-chain-indexer
- flare-system-client
- ftso-scaling data provider

There will also be config files generated for everything inside `./mounts` directory

## Price provider

Start your own price provider or alternatively use example provider shipped with `ftso-scaling` project
```bash
docker run --rm --env-file "mounts/scaling/.env" -p 3101:3101 "ftso-v2-deployment/ftso-scaling" yarn start example_provider
```
