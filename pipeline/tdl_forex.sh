#!/bin/bash

INPUT_FILE="$1"

asset_managers_long=$(jq '.cot.asset_managers.long' $INPUT_FILE)
asset_managers_short=$(jq '.cot.asset_managers.short' $INPUT_FILE)

other_long=$(jq '.cot.other_reportables.long' $INPUT_FILE)
other_short=$(jq '.cot.other_reportables.short' $INPUT_FILE)

nonrep_long=$(jq '.cot.nonreportable.long' $INPUT_FILE)
nonrep_short=$(jq '.cot.nonreportable.short' $INPUT_FILE)

leveraged_long=$(jq '.cot.leveraged_funds.long' $INPUT_FILE)
leveraged_short=$(jq '.cot.leveraged_funds.short' $INPUT_FILE)

dealers_long=$(jq '.cot.dealers.long' $INPUT_FILE)
dealers_short=$(jq '.cot.dealers.short' $INPUT_FILE)

tdl_lm=$((asset_managers_long - asset_managers_short \
        + other_long - other_short \
        + nonrep_long - nonrep_short))

tdl_s=$((leveraged_long - leveraged_short \
       + dealers_long - dealers_short))

if [ "$tdl_lm" -gt "$tdl_s" ]; then
  dominant="TDL-L&M"
elif [ "$tdl_s" -gt "$tdl_lm" ]; then
  dominant="TDL-S"
else
  dominant="NEUTRAL"
fi

echo "{ \"tdl_lm_score\": $tdl_lm, \"tdl_s_score\": $tdl_s, \"dominant\": \"$dominant\" }"
