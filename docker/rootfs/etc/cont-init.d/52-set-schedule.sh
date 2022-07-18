#!/usr/bin/with-contenv bash
# shellcheck shell=bash

# source env variables
source /etc/cont-init.d/20-setenv.sh

function prepare_vars() {
    # set log level
    case "${MDLP_LOG_LEVEL}" in
        "lean")
            MDLP_LOG_LEVEL_FLAG="    --lean"
            ;;
        "verbose")
            MDLP_LOG_LEVEL_FLAG="    --verbose"
            ;;
        "debug")
            MDLP_LOG_LEVEL_FLAG="    --debug"
            ;;
    esac

    # check if forcevol should be used
    if [[ "${MDLP_FORCEVOL,,}" == "true" ]]; then
        # add backslash if log level is also specified
        if [[ -n "${MDLP_LOG_LEVEL_FLAG}" ]]; then
            MDLP_FORCEVOL_FLAG="\n    --forcevol \\"
        else
            MDLP_FORCEVOL_FLAG="\n    --forcevol"
        fi
    fi
}

# set schedule with env variables
function set_vars() {
    echo -ne "#!/bin/bash\n
python3 /app/manga-dlp.py \\
    --path ${MDLP_PATH} \\
    --read ${MDLP_READ} \\
    --language ${MDLP_LANGUAGE} \\
    --chapters ${MDLP_CHAPTERS} \\
    --format ${MDLP_FILE_FORMAT} \\
    --wait ${MDLP_WAIT}" \
        > /app/schedules/daily.sh

    # set forcevol or log level if specified
    if [[ -n "${MDLP_FORCEVOL_FLAG}" ]] || [[ -n "${MDLP_LOG_LEVEL_FLAG}" ]]; then
        sed -i 's/--wait '"${MDLP_WAIT}"'/--wait '"${MDLP_WAIT}"' \\/g' /app/schedules/daily.sh
        echo -e "${MDLP_FORCEVOL_FLAG:-}" >> /app/schedules/daily.sh
        echo -e "${MDLP_LOG_LEVEL_FLAG:-}" >> /app/schedules/daily.sh
    else
        # add final newline of not added before
        echo -ne "\n" >> /app/schedules/daily.sh
    fi
}

# check if schedule should be generated
if [[ "${MDLP_GENERATE_SCHEDULE,,}" == "true" ]]; then
    echo "Generating schedule"
    prepare_vars
    set_vars
fi
