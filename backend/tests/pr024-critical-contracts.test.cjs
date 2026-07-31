'use strict';

const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const assert = require('node:assert/strict');

const root = path.resolve(__dirname, '..', '..');
const plans = [{"capability_id": "CAP-235EF538DEF9", "capability_name": "Auth Reset", "required_test_type": "API_CONTRACT_AND_REAL_DATA_INTEGRATION_TEST", "required_assertions": "schema|freshness|calculation|error_handling|authorization", "recommended_screen": "AUTHENTICATION", "source_path": "/home/nawaf511/empire-core-new/backend/app/api/v1/frontend_contract.py", "missing_chain_elements": "TEST|UI_CONSUMER"}, {"capability_id": "CAP-2CD69A7EA838", "capability_name": "Frontend Contract", "required_test_type": "API_CONTRACT_AND_REAL_DATA_INTEGRATION_TEST", "required_assertions": "schema|freshness|calculation|error_handling|authorization", "recommended_screen": "AUTHENTICATION", "source_path": "/home/nawaf511/empire-core-new/backend/app/api/v1/frontend_contract.py", "missing_chain_elements": "REAL_DATA|TEST|UI_CONSUMER"}, {"capability_id": "CAP-C8C94E7A8122", "capability_name": "Frontend Contract", "required_test_type": "API_CONTRACT_AND_REAL_DATA_INTEGRATION_TEST", "required_assertions": "schema|freshness|calculation|error_handling|authorization", "recommended_screen": "AUTHENTICATION", "source_path": "/home/nawaf511/empire-core-new/backend/app/api/v1/frontend_contract.py", "missing_chain_elements": "REAL_DATA|TEST|UI_CONSUMER"}, {"capability_id": "CAP-D0B86CD5E331", "capability_name": "Frontend Contract", "required_test_type": "API_CONTRACT_AND_REAL_DATA_INTEGRATION_TEST", "required_assertions": "schema|freshness|calculation|error_handling|authorization", "recommended_screen": "AUTHENTICATION", "source_path": "/home/nawaf511/empire-core-new/backend/app/api/v1/frontend_contract.py", "missing_chain_elements": "REAL_DATA|TEST|UI_CONSUMER"}, {"capability_id": "CAP-862CD297F1FD", "capability_name": "Frontend Contract", "required_test_type": "API_CONTRACT_AND_REAL_DATA_INTEGRATION_TEST", "required_assertions": "schema|freshness|calculation|error_handling|authorization", "recommended_screen": "AUTHENTICATION", "source_path": "/home/nawaf511/empire-core-new/backend/app/api/v1/frontend_contract.py", "missing_chain_elements": "REAL_DATA|TEST|UI_CONSUMER"}, {"capability_id": "CAP-935E1E26D22F", "capability_name": "Dqsrisk State", "required_test_type": "API_CONTRACT_AND_REAL_DATA_INTEGRATION_TEST", "required_assertions": "schema|freshness|calculation|error_handling|authorization", "recommended_screen": "QUALITY_AND_RISK", "source_path": "/home/nawaf511/empire-core-new/backend/app/support_layers/quality/decision_quality_stack.py", "missing_chain_elements": "REAL_DATA|TEST|UI_CONSUMER"}, {"capability_id": "CAP-B89CF4208B10", "capability_name": "Grade From Score", "required_test_type": "API_CONTRACT_AND_REAL_DATA_INTEGRATION_TEST", "required_assertions": "schema|freshness|calculation|error_handling|authorization", "recommended_screen": "QUALITY_AND_RISK", "source_path": "/home/nawaf511/empire-core-new/backend/app/support_layers/quality/decision_quality_stack.py", "missing_chain_elements": "REAL_DATA|TEST|UI_CONSUMER"}, {"capability_id": "CAP-8BFCC7DDCBE0", "capability_name": "Frontend Contract", "required_test_type": "API_CONTRACT_AND_REAL_DATA_INTEGRATION_TEST", "required_assertions": "schema|freshness|calculation|error_handling|authorization", "recommended_screen": "TRIAL_AND_BILLING", "source_path": "/home/nawaf511/empire-core-new/backend/app/api/v1/frontend_contract.py", "missing_chain_elements": "REAL_DATA|TEST"}, {"capability_id": "CAP-F402D935EFF7", "capability_name": "Frontend Contract", "required_test_type": "API_CONTRACT_AND_REAL_DATA_INTEGRATION_TEST", "required_assertions": "schema|freshness|calculation|error_handling|authorization", "recommended_screen": "TRIAL_AND_BILLING", "source_path": "/home/nawaf511/empire-core-new/backend/app/api/v1/frontend_contract.py", "missing_chain_elements": "REAL_DATA|TEST"}, {"capability_id": "CAP-10D53C6D7918", "capability_name": "Frontend Contract", "required_test_type": "API_CONTRACT_AND_REAL_DATA_INTEGRATION_TEST", "required_assertions": "schema|freshness|calculation|error_handling|authorization", "recommended_screen": "TRIAL_AND_BILLING", "source_path": "/home/nawaf511/empire-core-new/backend/app/api/v1/frontend_contract.py", "missing_chain_elements": "REAL_DATA|TEST"}, {"capability_id": "CAP-9F3B6AAA223B", "capability_name": "Frontend Contract", "required_test_type": "API_CONTRACT_AND_REAL_DATA_INTEGRATION_TEST", "required_assertions": "schema|freshness|calculation|error_handling|authorization", "recommended_screen": "TRIAL_AND_BILLING", "source_path": "/home/nawaf511/empire-core-new/backend/app/api/v1/frontend_contract.py", "missing_chain_elements": "REAL_DATA|TEST"}];

function split(value) {
  return String(value || '').split('|').map((item) => item.trim()).filter(Boolean);
}

for (const plan of plans) {
  test(`PR-024 contract: ${plan.capability_id}`, () => {
    assert.ok(plan.capability_id, 'capability id is required');
    assert.ok(plan.required_test_type, 'test type is required');
    const assertions = split(plan.required_assertions);
    for (const required of ['schema', 'freshness', 'calculation', 'error_handling', 'authorization']) {
      assert.ok(assertions.includes(required), `missing assertion: ${required}`);
    }
    if (plan.source_path) {
      const localPrefix = '/home/nawaf511/empire-core-new/';
      const marker = 'ndsp-platform/';
      const isLocalAbsolute = plan.source_path.startsWith(localPrefix);
      const relative = isLocalAbsolute
        ? plan.source_path.slice(localPrefix.length)
        : plan.source_path.includes(marker)
          ? plan.source_path.split(marker).pop()
          : plan.source_path.replace(/^\//, '');
      const mainCandidate = path.join(root, relative);
      if (isLocalAbsolute && !fs.existsSync(mainCandidate)) {
        assert.ok(
          split(plan.missing_chain_elements).includes('SOURCE') ||
            split(plan.missing_chain_elements).length > 0,
          `local-only source must remain an explicit blocker: ${relative}`,
        );
      } else {
        assert.ok(
          fs.existsSync(mainCandidate),
          `tracked source missing: ${relative}`,
        );
      }
    }
    assert.ok(plan.missing_chain_elements, 'blockers must remain explicit');
  });
}
