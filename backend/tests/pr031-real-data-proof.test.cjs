'use strict';

const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const assert = require('node:assert/strict');

const root = path.resolve(__dirname, '..', '..');
const records = [{"capability_id": "CAP-4FF90CCC6DFE", "capability_name": "Tdl V2 Policy Admin", "closure_state": "REMAINS_OPEN", "data_source": "UNKNOWN", "data_state": "UNKNOWN", "endpoint": "", "connector_evidence": "backend/tests/pr028-quick-wins-contracts.test.cjs", "payload_sha256": "", "payload_bytes": 0, "root_item_count": 0, "remaining_missing_evidence": "REAL_DATA"}, {"capability_id": "CAP-8A9DD9B6E7D5", "capability_name": "Tdl V2 Policy Admin", "closure_state": "REMAINS_OPEN", "data_source": "UNKNOWN", "data_state": "UNKNOWN", "endpoint": "", "connector_evidence": "backend/tests/pr028-quick-wins-contracts.test.cjs", "payload_sha256": "", "payload_bytes": 0, "root_item_count": 0, "remaining_missing_evidence": "REAL_DATA"}];

for (const record of records) {
  test(`PR-031 real-data proof: ${record.capability_id}`, () => {
    assert.ok(record.capability_id);
    assert.ok(record.capability_name);

    if (record.closure_state === 'CLOSED_MACHINE_VERIFIED') {
      assert.ok(record.data_source);
      assert.match(record.data_state, /^REAL_(LIVE|SNAPSHOT)$/);
      assert.ok(record.endpoint);
      assert.ok(record.connector_evidence);
      assert.ok(
        fs.existsSync(path.join(root, record.connector_evidence)),
        `connector source missing: ${record.connector_evidence}`,
      );
      assert.match(record.payload_sha256, /^[a-f0-9]{64}$/);
      assert.ok(Number(record.payload_bytes) > 0);
      assert.ok(Number(record.root_item_count) > 0);
      assert.equal(record.remaining_missing_evidence, '');
    } else {
      assert.equal(record.remaining_missing_evidence, 'REAL_DATA');
    }
  });
}
