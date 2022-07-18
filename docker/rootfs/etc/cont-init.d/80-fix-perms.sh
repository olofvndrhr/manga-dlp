#!/usr/bin/with-contenv bash
# shellcheck shell=bash

# source env variables
source /etc/cont-init.d/20-setenv.sh

# fix permissions
find '/app' -type 'd' \( -not -perm 775 -and -not -path '/app/downloads*' \) -exec chmod 775 '{}' \+
find '/app' -type 'f' \( -not -perm 664 -and -not -path '/app/downloads*' \) -exec chmod 664 '{}' \+

find '/app' \( -not -user abc -and -not -path '/app/downloads*' \) -exec chown abc '{}' \+
find '/app' \( -not -group abc -and -not -path '/app/downloads*' \) -exec chown :abc '{}' \+

# fix schedules
chmod -R +x /app/schedules
