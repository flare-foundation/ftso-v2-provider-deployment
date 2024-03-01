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

## Register accounts

Note: Account registration is required for FTSOv2 participation and must be done before starting any further deployment steps.

To avoid nonce conflicts, **System Client** uses separate addresses for sending transactions at each voting round stage.
Each data provider in the FTSOv2 system must set up and register the following 5 accounts:

TODO: Describe accounts

- `Identity`. Main account.
- `Submit`. Used for sending commit and reveal transactions.
- `SubmitSignatures`. Used for sending voting round result signature transactions.
- `SigningPolicy`. 
- `Delegation`.

Account registration is handled by the `EntityManager` smart contract, which for Coston can be accessed [here](https://coston-explorer.flare.network/address/0x35E74af3AfC322e1fCf187cB4970126D76fF9Dcd/write-contract#address-tabs).

The required contract invocation steps can be found in this [deployment task](https://github.com/flare-foundation/flare-smart-contracts-v2/blob/main/deployment/tasks/register-entities.ts#L33). You can check out the smart contract repo and run the task itself, or register accounts manually via the explorer UI link above. (It only needs to be done once).

Instructions for the Hardhat deployment task:
- Check out repo: https://github.com/flare-foundation/flare-smart-contracts-v2/
- Build repo: `yarn c`
- Create a JSON file with account keys:
```
[
  {
    "identity": {
      "address": "0xca84d6086c5b32212a0cf1638803355d7be31482",
      "privateKey": "<private key hex>"
    },
    "submit": {
      "address": "0x7961de7ad159106a79187379a22d21c1e5a924db",
      "privateKey": "<private key hex>"
    },
    "submitSignatures": {
      "address": "0x7570c09c17f79aa50bab7ba385c0d5ca12c5b4d3",
      "privateKey": "<private key hex>"
    },
    "signingPolicy": {
      "address": "0x9ffa9cf5f677e925b6ecacbf66caefd7e1b9883a",
      "privateKey": "<private key hex>"
    },
    "delegation": {
      "address": "0x95288e962ff1893ef6c32ad4143fffb12e1eb15f",
      "privateKey": "<private key hex>"
    },
  }
]
```
- Set the following env vars in `.env`:
```
CHAIN_CONFIG="coston"
ENTITIES_FILE_PATH="<path to account keys JSON>"
```
- Run task:
```
yarn hardhat --network coston register-entities
```

## Install dependencies

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
- `c-chain-indexer-db` - MySQL instance.
- `c-chain-indexer` – **Indexer**.
- `flare-system-client` **System Client**.
- `ftso-scaling` - **Data Provider**.

There will also be config files generated for everything inside `./mounts` directory.

## Feed value provider

Start your own feed value provider or alternatively use example provider shipped with `ftso-scaling` project
```bash
docker run --rm --env-file "mounts/scaling/.env" -p 3101:3101 "ftso-v2-deployment/ftso-scaling" yarn start example_provider
```

Once the container is running, you can find the API spec at: http://localhost:3101/api-doc.