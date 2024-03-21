#!/usr/bin/env bash

set -eu

ROOT_DIR="$(pwd)"

CHAIN_CONFIG="${ROOT_DIR}/config/config.coston.json"
DEPLOYED_CONTRACTS="${ROOT_DIR}/config/contracts.coston.json"
INITIAL_REWARD_EPOCH="${ROOT_DIR}/config/initial_reward_epoch.coston.txt"

wait_for_file() {
    file="$1"
    if ! [[ -f "$file" ]]; then
        echo -n "waiting for $(basename \"$file\") "
        until [[ -f "$file" ]]; do
            sleep 1
            echo -n "."
        done
        echo
    fi
}

get_address_by_name() {
    name="$1"
    echo $(jq -r ".[] | select(.name == \"$name\") | .address" "$DEPLOYED_CONTRACTS")
}

write_c_chain_config() {
    export SUBMISSION=$(get_address_by_name "Submission")
    export RELAY=$(get_address_by_name "Relay")
    export FLARE_SYSTEMS_MANAGER=$(get_address_by_name "FlareSystemsManager")
    export VOTER_REGISTRY=$(get_address_by_name "VoterRegistry")
    export FLARE_SYSTEMS_CALCULATOR=$(get_address_by_name "FlareSystemsCalculator")
    export FTSO_REWARD_OFFERS_MANAGER=$(get_address_by_name "FtsoRewardOffersManager")

    mkdir -p "mounts/indexer/"
    CONFIG_FILE="mounts/indexer/config.toml"
    envsubst < "template-configs/indexer.template.toml" > "$CONFIG_FILE"
}

write_system_client_config() {
    export SUBMISSION=$(get_address_by_name "Submission")
    export FLARE_SYSTEMS_MANAGER=$(get_address_by_name "FlareSystemsManager")
    export VOTER_REGISTRY=$(get_address_by_name "VoterRegistry")
    export RELAY=$(get_address_by_name "Relay")

    mkdir -p "mounts/client"
    CONFIG_FILE="mounts/client/config.toml"
    envsubst < "template-configs/client.template.toml" > "$CONFIG_FILE"
}

write_ftso_scaling_config() {
    export FLARE_SYSTEMS_MANAGER=$(get_address_by_name "FlareSystemsManager")
    export FTSO_REWARD_OFFERS_MANAGER=$(get_address_by_name "FtsoRewardOffersManager")
    export REWARD_MANAGER=$(get_address_by_name "RewardManager")
    export SUBMISSION=$(get_address_by_name "Submission")
    export RELAY=$(get_address_by_name "Relay")
    export FLARE_SYSTEMS_CALCULATOR=$(get_address_by_name "FlareSystemsCalculator")
    export VOTER_REGISTRY=$(get_address_by_name "VoterRegistry")

    export FIRST_VOTING_EPOCH_START_SEC=$(jq -r .firstVotingRoundStartTs "$CHAIN_CONFIG")
    export VOTING_EPOCH_DURATION_SEC=$(jq -r .votingEpochDurationSeconds "$CHAIN_CONFIG")
    export FIRST_REWARD_EPOCH_START_VOTING_ID=$(jq -r .firstRewardEpochStartVotingRoundId "$CHAIN_CONFIG")
    export REWARD_EPOCH_DURATION_IN_VOTING_EPOCHS=$(jq -r .rewardEpochDurationInVotingEpochs "$CHAIN_CONFIG")
    export INITIAL_REWARD_EPOCH_ID=$(cat "$INITIAL_REWARD_EPOCH")

    mkdir -p "mounts/scaling"
    CONFIG_FILE="mounts/scaling/.env"
    envsubst < template-configs/scaling.env > "$CONFIG_FILE"
}

main() {
    source <(grep -v '^#' "./.env" | sed -E 's|^(.+)=(.*)$|: ${\1=\2}; export \1|g')

    if [ -d "mounts" ] || [ -f "mounts" ]; then
        echo "cleaning configs from previous runs:"
        echo "rm -r mounts"
        rm -r "mounts"
    fi
    echo ""

    mount_dirs=(
        "mounts/client/"
        "mounts/client/credentials/"
        "mounts/indexer/"
        "mounts/scaling/"
    )

    echo "preparing mount dirs:"
    for dest in "${mount_dirs[@]}"; do
        echo "mkdir -p $dest"
        mkdir -p "$dest"
    done
    echo ""

    echo "writing configs for indexer, client and scaling"
    write_c_chain_config
    write_system_client_config
    write_ftso_scaling_config
}

main
