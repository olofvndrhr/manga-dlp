#!/usr/bin/with-contenv bash
# shellcheck shell=bash

# source env variables
source /etc/cont-init.d/20-setenv.sh

# check schedule
[[ -f "/app/schedules/daily.sh" ]] && DAILYSH=true
[[ -f "/app/schedules/daily" ]] && DAILY=true
# check crontab
if grep -q -e "/app/schedules/daily.sh\s" /etc/cron.d/mangadlp; then
    CRONSH=true
elif grep -q -e "/app/schedules/daily\s" /etc/cron.d/mangadlp; then
    CRON=true
fi

# fix new .sh schedule if its not synced with the crontab
if [[ "${CRONSH}" == "true" ]] && [[ "${DAILYSH}" != "true" ]]; then
    echo "Fixing new .sh schedule"
    if ! ln -s /app/schedule/daily /app/schedule/daily.sh; then
        echo "Cant fix schedule. Maybe the file is missing."
    fi
elif [[ "${CRON}" == "true" ]] && [[ "${DAILY}" != "true" ]]; then
    echo "Fixing new .sh schedule"
    if ! ln -s /app/schedule/daily.sh /app/schedule/daily; then
        echo "Cant fix schedule. Maybe the file is missing."
    fi
fi
