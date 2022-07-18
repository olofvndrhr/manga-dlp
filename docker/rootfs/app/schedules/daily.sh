#!/bin/bash

python3 /app/manga-dlp.py \
    --path /app/downloads \
    --read /app/mangas.txt \
    --chapters all \
    --wait 2 \
    --lean
