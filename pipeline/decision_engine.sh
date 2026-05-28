#!/bin/bash

INPUT_FILE="$1"

phase=$(jq -r '.phase' $INPUT_FILE)

if [ "$phase" == "NDIP_GOLDEN_SIGNAL" ]; then
  decision="BUY"
elif [ "$phase" == "PULLBACK" ]; then
  decision="WAIT_FOR_ENTRY"
elif [ "$phase" == "REVERSAL_POTENTIAL" ]; then
  decision="CAUTION"
else
  decision="NO_TRADE"
fi

echo "{ \"decision\": \"$decision\" }"
