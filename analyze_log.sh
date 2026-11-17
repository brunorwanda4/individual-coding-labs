#!/usr/bin/env bash

log_file="${1:-transit_session.log}"

if [[ ! -f "$log_file" ]]; then
    echo "Error: log file '$log_file' does not exist." >&2
    exit 1
fi

session_count=$(grep -c "===== New session started" "$log_file" || true)
zebra_count=$(grep -c "Zebra crossing!" "$log_file" || true)
lane_change_count=$(grep -c "Changing lane:" "$log_file" || true)

echo "Sessions: $session_count"
echo "Zebra crossing stops: $zebra_count"
echo "Lane changes: $lane_change_count"

latest_trip=$(grep "begins the journey" "$log_file" | tail -n 1)
if [[ -n "$latest_trip" ]]; then
    driver_name=$(printf '%s\n' "$latest_trip" | sed -E 's/^.* \] //' | sed -E 's/ begins the journey.*$//')
    echo "Latest driver: $driver_name"
fi

latest_top=$(grep "Top speed" "$log_file" | tail -n 1)
if [[ -n "$latest_top" ]]; then
    top_speed=$(printf '%s\n' "$latest_top" | sed -E 's/^.*Top speed *: *//')
    echo "Latest top speed: $top_speed"
fi
