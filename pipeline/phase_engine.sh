#!/bin/bash

INPUT_FILE="$1"

total=$(jq '.tdl_lm_score_total' $INPUT_FILE)
change=$(jq '.tdl_lm_score_change' $INPUT_FILE)

if [ "$total" -gt 0 ] && [ "$change" -gt 0 ]; then
  phase="NDIP_GOLDEN_SIGNAL"
elif [ "$total" -gt 0 ] && [ "$change" -lt 0 ]; then
  phase="PULLBACK"
elif [ "$total" -lt 0 ] && [ "$change" -gt 0 ]; then
  phase="REVERSAL_POTENTIAL"
else
  phase="RANGE"
fi

echo "{ \"phase\": \"$phase\" }"
