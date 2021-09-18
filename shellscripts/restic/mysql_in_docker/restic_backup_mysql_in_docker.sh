#!/bin/bash
set -e
set -u
set -o pipefail


docker exec $DOCKER_CONTAINER mysqldump -p$MYSQL_PASSWORD $MYSQL_DATABASE | restic backup --stdin --stdin-filename $BACKUP_FILE
restic forget -q --prune --keep-daily 3
