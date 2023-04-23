#!/bin/sh
set -eu

while true; do
    python3.9 backup.py;
    sleep ${BACKUP_DELAY_IN_SECONDS};
done
