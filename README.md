# ftso v2 provider deployment

## dependencies

You will need:
- [jq](https://jqlang.github.io/jq/)
    - `brew install jq`
    - `apt-get install jq`
    - `pacman -S jq`
- [envsubst](https://www.gnu.org/software/gettext/manual/html_node/envsubst-Invocation.html)
    - (macOS only) `brew install gettext`
- [docker](https://www.docker.com/)

## setup repos and docker images

- you will need a gitlab user with access to following repositories until they are made public:
    - [ftso-scaling](https://gitlab.com/flarenetwork/ftso-scaling)
    - [flare-system-client](https://gitlab.com/flarenetwork/flare-system-client)
    - [flare-system-c-chain-indexer](https://gitlab.com/flarenetwork/flare-system-c-chain-indexer)

- use `.env.example` to create `.env` file, eg.: using `cp .env.example .env`

- use `./repos pull` to clone (first time) or pull (when cloned directories exist) projects. If you switch branches in .env file or you get errors while using `./repos pull` command, use `./repos clean` to delete files followed by `./repos pull` to clone them again. 

- use `./build.sh` to build docker images for all projects.

## start provider stack

using `./run run` 4 services will start:
- c-chain-indexer-db
- c-chain-indexer
- flare-system-client
- ftso-scaling data provider

there will also be config files generated for everything inside `./mounts` directory

## price provider

start your own price provider or alternatively use example provider shipped with `ftso-scaling` project
```bash
docker run --rm --env-file "mounts/scaling/.env" -p 3101:3101 "ftso-v2-deployment/ftso-scaling" yarn start example_provider
```

