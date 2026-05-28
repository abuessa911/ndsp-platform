#!/bin/bash

INPUT_FILE="$1"

phase=$(jq -r '.phase' $INPUT_FILE)
day=$(jq -r '.day' $INPUT_FILE)

if [[ "$day" == "Monday" || "$day" == "Tuesday" || "$day" == "Wednesday" ]]; then
  timing="Mon-Wed"
else
  timing="Thu-Fri"
fi

if [[ "$phase" == "NDIP_GOLDEN_SIGNAL" && "$timing" == "Thu-Fri" ]]; then
  entry="CONFIRMED_ENTRY"
elif [[ "$phase" == "NDIP_GOLDEN_SIGNAL" && "$timing" == "Mon-Wed" ]]; then
  entry="EARLY_ENTRY"
elif [[ "$phase" == "PULLBACK" && "$timing" == "Mon-Wed" ]]; then
  entry="OPTIMAL_ENTRY"
elif [[ "$phase" == "PULLBACK" && "$timing" == "Thu-Fri" ]]; then
  entry="LATE_ENTRY"
elif [[ "$phase" == "REVERSAL_POTENTIAL" ]]; then
  entry="WAIT_CONFIRMATION"
else
  entry="NO_ENTRY"
fi

echo "{ \"entry_signal\": \"$entry\" }"
