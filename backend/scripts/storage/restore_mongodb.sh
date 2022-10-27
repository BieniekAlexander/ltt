#!/bin/bash
# delete what currently exists in MongoDB and restore it with the most recent backup
# Set the MONGODB_URI variable - TODO document this better
MOST_RECENT_BACKUP_PATH=../../backups/$(ls ../../backups | sort -V | tail -n 1)

for db in auth polish ; do
    mongo $MONGODB_URI <<EOF
    use $db
    db.dropDatabase()
EOF
done

mongorestore --uri=$MONGODB_URI $MOST_RECENT_BACKUP_PATH