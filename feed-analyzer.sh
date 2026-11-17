#!/usr/bin/env bash

csv_file="${1:-twitter_dataset.csv}"

if [[ ! -f "$csv_file" ]]; then
    echo "Error: CSV file '$csv_file' does not exist." >&2
    exit 1
fi

header=$(head -n 1 "$csv_file")
IFS=',' read -r -a columns <<< "$header"
username_field=0

for i in "${!columns[@]}"; do
    normalized=$(printf '%s' "${columns[$i]}" | tr -d '\r' | tr '[:upper:]' '[:lower:]')
    if [[ "$normalized" == "username" ]]; then
        username_field=$((i + 1))
        break
    fi
done

if [[ "$username_field" -eq 0 ]]; then
    echo "Error: the CSV does not contain a Username column." >&2
    exit 1
fi

tail -n +2 "$csv_file" |
    cut -d',' -f"$username_field" |
    sed '/^[[:space:]]*$/d' |
    sort |
    uniq -c |
    sort -rn |
    head -n 5
