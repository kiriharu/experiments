#!/bin/bash
set -e
set -u
set -o pipefail

export RESTIC_REPOSITORY=""
export RESTIC_PASSWORD=""
export WEBSITE_PATH=""

restic backup $WEBSITE_PATH
restic forget --prune --keep-weekly 3