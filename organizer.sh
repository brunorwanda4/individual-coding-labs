#!/usr/bin/env bash

set -e

if [[ ! -d "archive" ]]; then
    mkdir "archive"
fi

if [[ ! -f "grades.csv" ]]; then
    echo "Error: grades.csv does not exist in the current directory." >&2
    exit 1
fi

timestamp=$(date +"%Y%m%d-%H%M%S")
archived_name="grades_${timestamp}.csv"

mv "grades.csv" "archive/$archived_name"
: > "grades.csv"

printf "%s | original: grades.csv | archived: archive/%s\n" "$timestamp" "$archived_name" >> organizer.log
echo "Archived grades.csv as archive/$archived_name"
