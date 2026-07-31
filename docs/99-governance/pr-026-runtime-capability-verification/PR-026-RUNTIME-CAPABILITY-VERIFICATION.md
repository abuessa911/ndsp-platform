# PR-026 — Runtime Capability Verification

- Total capabilities: `526`
- Runtime verified: `0`
- Runtime pending: `526`
- Systemd service records: `290`
- HTTP probes: `13333`
- Accepted HTTP probes: `1264`
- Mutating requests executed: `0`
- Services restarted: `0`
- Environment values read: `false`
- UI_COMPLETE records created: `0`

## Missing evidence

| Evidence | Count |
|---|---:|
| CALCULATION | 164 |
| ENDPOINT | 327 |
| REAL_DATA | 216 |
| SERVICE | 326 |
| SOURCE | 362 |
| TEST | 526 |
| UI | 337 |

Runtime verification requires the full chain:

`source → active service → responsive endpoint → real data → calculation → test → UI`
