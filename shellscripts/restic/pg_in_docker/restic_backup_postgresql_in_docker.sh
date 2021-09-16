#!/bin/bash
set -e
set -u
set -o pipefail

docker exec $DOCKER_CONTAINER pg_dump -Fc -h localhost -U $DATABASE | restic backup --stdin --stdin-filename $BACKUP_FILE
restic forget -q --prune --keep-daily 3
