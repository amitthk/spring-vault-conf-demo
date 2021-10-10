#!/bin/bash

if [[ $# -eq 0 ]] ; then
    echo 'usage ./vault_draw_kv.sh <<VAULT_ADDR>> <<VAULT_TOKEN>>  <<VAULT_KEYS_PATH>>'
    exit 1
fi

VAULT_ADDR=$1
VAULT_TOKEN=$2
VAULT_KEYS_PATH=$3


rm -f .env

user=$(curl  -H "X-Vault-Token: $VAULT_TOKEN" \
        -X GET $VAULT_ADDR/v1/$VAULT_KEYS_PATH)

echo DB_ENDPOINT=$(echo $user | jq -r .data.data.dbendpoint) > .env
echo DB_USER=$(echo $user | jq -r .data.data.dbuser) >> .env
echo DB_PASSWORD=$(echo $user | jq -r .data.data.dbpass) >> .env