#!/bin/bash
set -e
set -u
set -o pipefail

export RESTIC_REPOSITORY=""
export RESTIC_PASSWORD=""

export MYSQL_PASSWORD=""
export MYSQL_DATABASE=""
export BACKUP_FILE=""

mysqldump -p$MYSQL_PASSWORD $MYSQL_DATABASE | restic backup --stdin --stdin-filename $BACKUP_FILE
restic forget --prune --keep-weekly 3
