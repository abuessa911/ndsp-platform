#!/bin/bash

# ============================================
# 💀 NDIP NMP ENGINE (ZONE + BEHAVIOR)
# ============================================

INPUT_FILE="$1"

if [ -z "$INPUT_FILE" ]; then
  echo "Usage: ./nmp_engine.sh input.json"
  exit 1
fi

# ============================================
# 📊 INPUT DATA
# ============================================

current_price=$(jq '.price.current' $INPUT_FILE)
open_price=$(jq '.price.open' $INPUT_FILE)
close_price=$(jq '.price.close' $INPUT_FILE)

tdl_signal=$(jq -r '.tdl_signal' $INPUT_FILE)

# ============================================
# 🧱 BUILD NMP ZONE
# ============================================

if (( $(echo "$open_price < $close_price" | bc -l) )); then
  nmp_low=$open_price
  nmp_high=$close_price
else
  nmp_low=$close_price
  nmp_high=$open_price
fi

# ============================================
# 📍 POSITION (IMPORTANT)
# ============================================

if [ "$tdl_signal" == "BULLISH" ]; then
  position="BELOW_PRICE"
else
  position="ABOVE_PRICE"
fi

# ============================================
# 🧠 BEHAVIOR ANALYSIS
# ============================================

signal="NO_SIGNAL"

# داخل المنطقة
if (( $(echo "$current_price >= $nmp_low && $current_price <= $nmp_high" | bc -l) )); then
  signal="TESTING_ZONE"

# قريب من المنطقة → continuation
elif (( $(echo "$current_price < $nmp_low + 5 && $current_price > $nmp_low - 5" | bc -l) )); then
  signal="CONTINUATION_SIGNAL"

# انعكاس محتمل
elif (( $(echo "$current_price > $nmp_high + 5" | bc -l) )); then
  signal="REVERSAL_SIGNAL"
fi

# ============================================
# 📦 OUTPUT
# ============================================

echo "{"
echo "  \"nmp_zone\": {"
echo "    \"low\": $nmp_low,"
echo "    \"high\": $nmp_high"
echo "  },"
echo "  \"position\": \"$position\","
echo "  \"signal\": \"$signal\""
echo "}"
