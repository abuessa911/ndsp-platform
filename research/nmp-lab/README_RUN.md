# Run NMP Lab

Put OHLCV CSV files in:

research/nmp-lab/data

Required columns:
- open
- high
- low
- close

Optional:
- date/time
- volume

Run:

python3 research/nmp-lab/scripts/nmp_lab_engine.py \
  --data-dir research/nmp-lab/data \
  --out-dir research/nmp-lab/results

Results:
- *_nmp_lab_results.csv
- *_nmp_lab_summary.csv
- manifest.json
