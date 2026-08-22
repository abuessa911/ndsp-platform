#!/usr/bin/env python3
import json, re, sys
from pathlib import Path
root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
errors = []
ids = set()
allowed_status = {'DRAFT','DISCOVERED','VERIFIED','REVIEWED','APPROVED','ACTIVE','DEPRECATED','RETIRED','ARCHIVED','CONFLICTED','UNVERIFIED','DOCUMENTATION_ONLY','DESIGN_REFERENCE_ONLY','PROPOSED'}
allowed_class = {'VERIFIED_FROM_SOURCE','VERIFIED_FROM_RUNTIME_READ_ONLY','INFERRED_FROM_SOURCE','DOCUMENTATION_ONLY','DESIGN_REFERENCE_ONLY','HISTORICAL_REFERENCE','PROPOSED_NOT_IMPLEMENTED','PARTIALLY_IMPLEMENTED','CONFLICTING_IMPLEMENTATION','NOT_FOUND','REQUIRES_HUMAN_REVIEW'}
for path in root.glob('**/*.contract.json'):
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
    except Exception as exc:
        errors.append(f'{path}: invalid JSON: {exc}')
        continue
    cid = data.get('contract_id')
    if not cid: errors.append(f'{path}: missing contract_id')
    elif cid in ids: errors.append(f'{path}: duplicate contract_id {cid}')
    ids.add(cid)
    if data.get('status') not in allowed_status: errors.append(f'{path}: invalid status')
    if data.get('classification') not in allowed_class: errors.append(f'{path}: invalid classification')
    if not data.get('evidence'): errors.append(f'{path}: missing evidence')
    if data.get('status') in {'APPROVED','ACTIVE'}: errors.append(f'{path}: generated contract must not be approved/active')
    text = json.dumps(data, ensure_ascii=False)
    if re.search(r'(sk_live_|sk_test_|pk_live_|pk_test_)[A-Za-z0-9_]+', text): errors.append(f'{path}: possible secret')
if errors:
    print('\n'.join(errors))
    sys.exit(1)
print(f'OK: {len(ids)} contract files validated')
