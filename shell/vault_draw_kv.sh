#!/bin/bash

if [[ $# -eq 0 ]] ; then
    echo 'usage ./vault_draw_kv.sh <<VAULT_ENDPOINT>> <<VAULT_TOKEN>>  <<KEYS_PATH>>'
    exit 1
fi

VAULT_ENDPOINT=$1
VAULT_TOKEN=$2
KEYS_PATH=$3


rm -f .env

user=$(curl  -H "X-Vault-Token: $VAULT_TOKEN" \
        -X GET $VAULT_ENDPOINT/v1/$KEYS_PATH)

echo DB_ENDPOINT=$(echo $user | jq -r .data.data.dbendpoint) > .env
echo DB_USER=$(echo $user | jq -r .data.data.dbuser) >> .env
echo DB_PASSWORD=$(echo $user | jq -r .data.data.dbpass) >> .env