#!/usr/bin/with-contenv bash
# shellcheck shell=bash

# source env variables
source /etc/cont-init.d/20-setenv.sh

# check schedule
[[ -f "/app/schedules/daily.sh" ]] && DAILY_SH_FOUND=true
[[ -f "/app/schedules/daily" ]] && DAILY_FOUND=true
# check crontab
if grep -q -e "/app/schedules/daily.sh\s" /etc/cron.d/mangadlp; then
    CRON_SH_FOUND=true
elif grep -q -e "/app/schedules/daily\s" /etc/cron.d/mangadlp; then
    CRON_FOUND=true
fi

# fix new .sh schedule if it's not synced with the crontab
if [[ "${CRON_SH_FOUND}" == "true" ]] && [[ "${DAILY_SH_FOUND}" != "true" ]]; then
    echo "Fixing new .sh schedule"
    echo "Adding symlink to daily.sh"
    if ! ln -s /app/schedule/daily /app/schedule/daily.sh; then
        echo "Can't fix schedule. Maybe the file is missing."
    fi
elif [[ "${CRON_FOUND}" == "true" ]] && [[ "${DAILY_FOUND}" != "true" ]]; then
    echo "Fixing new .sh schedule"
    echo "Adding symlink to daily"
    if ! ln -s /app/schedule/daily.sh /app/schedule/daily; then
        echo "Can't fix schedule. Maybe the file is missing."
    fi
fi
