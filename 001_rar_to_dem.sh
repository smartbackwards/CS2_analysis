#!/bin/bash

ZIP_DIR=$1
TARGET_DIR=$2

mkdir -p "$TARGET_DIR"

for rar_file in "$ZIP_DIR"/*.rar; do
    echo "Extracting $rar_file to $TARGET_DIR..."
    unrar x "$rar_file" "$TARGET_DIR"
done