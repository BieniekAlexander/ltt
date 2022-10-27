#!/bin/bash
# Backup the MongoDB instance to a local backup directory
# Set the MONGODB_URI variable - TODO document this better
DATE=$(printf '%(%Y_%m_%d_%H_%M)T' -1)
mongodump -o ../../backups/${DATE}_mongodb_backup --uri=$MONGODB_URI --forceTableScan