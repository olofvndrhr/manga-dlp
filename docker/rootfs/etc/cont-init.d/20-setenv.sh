#!/usr/bin/with-contenv bash
# shellcheck shell=bash

# set all env variables for further use. If variable is unset, it will have the defaults on the right side after ":="

# custom env vars
: "${MDLP_GENERATE_SCHEDULE:=false}"
: "${MDLP_PATH:=/app/downloads}"
: "${MDLP_READ:=/app/mangas.txt}"
: "${MDLP_LANGUAGE:=en}"
: "${MDLP_CHAPTERS:=all}"
: "${MDLP_FILE_FORMAT:=cbz}"
: "${MDLP_WAIT:=0.5}"
: "${MDLP_FORCEVOL:=false}"
: "${MDLP_LOG_LEVEL:=warn}"
