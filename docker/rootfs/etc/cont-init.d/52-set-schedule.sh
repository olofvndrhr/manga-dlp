#!/usr/bin/with-contenv bash
# shellcheck shell=bash

# source env variables
source /etc/cont-init.d/20-setenv.sh

custom_args=(
    --path "${MDLP_PATH}"
    --read "${MDLP_READ}"
    --language "${MDLP_LANGUAGE}"
    --chapters "${MDLP_CHAPTERS}"
    --format "${MDLP_FILE_FORMAT}"
    --wait "${MDLP_WAIT}"
)

function prepare_vars() {
    # set log level
    case "${MDLP_LOG_LEVEL}" in
        "warn")
            custom_args+=("--warn")
            ;;
        "debug")
            custom_args+=("--debug")
            ;;
        *)
            if [[ -n "${MDLP_LOG_LEVEL}" ]]; then
                custom_args+=("--loglevel" "${MDLP_LOG_LEVEL}")
            fi
            ;;
    esac

    # check if forcevol should be used
    if [[ "${MDLP_FORCEVOL,,}" == "true" ]]; then
        custom_args+=("--forcevol")
    fi
}

# set schedule with env variables
function set_vars() {
    cat << EOF > "/app/schedules/daily.sh"
#!/bin/bash

python3 /app/manga-dlp.py ${custom_args[@]}

EOF
}

# check if schedule should be generated
if [[ "${MDLP_GENERATE_SCHEDULE,,}" == "true" ]]; then
    echo "Generating schedule"
    prepare_vars
    set_vars
fi
