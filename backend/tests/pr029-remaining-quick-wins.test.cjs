'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');

const records = [{"capability_id": "CAP-6F5DF526EE59", "capability_name": "Admin Only", "endpoint_path": "/api/admin-ui/health", "original_missing": "UI", "resolved": "UI", "remaining": ""}, {"capability_id": "CAP-753A055CFA5A", "capability_name": "Ndsp Write Alert State", "endpoint_path": "/api/admin-ui/health", "original_missing": "UI", "resolved": "UI", "remaining": ""}, {"capability_id": "CAP-7739F02602D8", "capability_name": "Get User By Id", "endpoint_path": "/api/auth/login/health", "original_missing": "UI", "resolved": "UI", "remaining": ""}, {"capability_id": "CAP-784548F2FDAD", "capability_name": "Authorize", "endpoint_path": "/api/admin-actions/users/action/health", "original_missing": "UI", "resolved": "UI", "remaining": ""}, {"capability_id": "CAP-790CBD0E1BCE", "capability_name": "Delete User Dependencies", "endpoint_path": "/api/admin/users/action/health", "original_missing": "UI", "resolved": "UI", "remaining": ""}, {"capability_id": "CAP-89CA79DDADE2", "capability_name": "Ndsp Read Alert State", "endpoint_path": "/api/admin-ui/health", "original_missing": "UI", "resolved": "UI", "remaining": ""}, {"capability_id": "CAP-9866D4AE9D59", "capability_name": "Update User Status", "endpoint_path": "/api/admin-ui/health", "original_missing": "UI", "resolved": "UI", "remaining": ""}, {"capability_id": "CAP-A231BBA8D29D", "capability_name": "Auth Required", "endpoint_path": "/health", "original_missing": "UI", "resolved": "UI", "remaining": ""}, {"capability_id": "CAP-ACFDAF4DAD5E", "capability_name": "Auth", "endpoint_path": "/api/auth/login/health", "original_missing": "UI", "resolved": "UI", "remaining": ""}, {"capability_id": "CAP-DF54F83FC9EB", "capability_name": "Authorize", "endpoint_path": "/api/admin/users/action/health", "original_missing": "UI", "resolved": "UI", "remaining": ""}, {"capability_id": "CAP-E22DBA05712A", "capability_name": "Get User By Email", "endpoint_path": "/api/auth/login/health", "original_missing": "UI", "resolved": "UI", "remaining": ""}, {"capability_id": "CAP-4FF90CCC6DFE", "capability_name": "Tdl V2 Policy Admin", "endpoint_path": "/policy", "original_missing": "REAL_DATA", "resolved": "", "remaining": "REAL_DATA"}, {"capability_id": "CAP-8A9DD9B6E7D5", "capability_name": "Tdl V2 Policy Admin", "endpoint_path": "/auth-debug", "original_missing": "REAL_DATA", "resolved": "", "remaining": "REAL_DATA"}, {"capability_id": "CAP-15C56B60B4B0", "capability_name": "Ndsp User Login Gateway", "endpoint_path": "", "original_missing": "ENDPOINT", "resolved": "", "remaining": "ENDPOINT"}, {"capability_id": "CAP-214521E6EBD1", "capability_name": "Ndsp User Login Gateway", "endpoint_path": "", "original_missing": "ENDPOINT", "resolved": "", "remaining": "ENDPOINT"}, {"capability_id": "CAP-242D8324FAD9", "capability_name": "Ndsp User Login Gateway", "endpoint_path": "", "original_missing": "ENDPOINT", "resolved": "", "remaining": "ENDPOINT"}, {"capability_id": "CAP-3A5ED3DB0C0D", "capability_name": "Risk Label", "endpoint_path": "", "original_missing": "ENDPOINT", "resolved": "", "remaining": "ENDPOINT"}, {"capability_id": "CAP-3B89863B2015", "capability_name": "Ndsp User Login Gateway", "endpoint_path": "", "original_missing": "ENDPOINT", "resolved": "", "remaining": "ENDPOINT"}, {"capability_id": "CAP-3D9086A829ED", "capability_name": "Ndsp Admin Ui Proxy", "endpoint_path": "", "original_missing": "ENDPOINT", "resolved": "", "remaining": "ENDPOINT"}, {"capability_id": "CAP-4B75FD38F852", "capability_name": "Ndsp Admin Ui Proxy", "endpoint_path": "", "original_missing": "ENDPOINT", "resolved": "", "remaining": "ENDPOINT"}, {"capability_id": "CAP-4FCAA631BA18", "capability_name": "Ndsp Admin Actions Bypass Old Middleware", "endpoint_path": "", "original_missing": "ENDPOINT", "resolved": "", "remaining": "ENDPOINT"}, {"capability_id": "CAP-644C81537AC6", "capability_name": "Ndsp User Login Gateway", "endpoint_path": "", "original_missing": "ENDPOINT", "resolved": "", "remaining": "ENDPOINT"}, {"capability_id": "CAP-6565FE804AF5", "capability_name": "Ndsp User Login Gateway", "endpoint_path": "", "original_missing": "ENDPOINT", "resolved": "", "remaining": "ENDPOINT"}, {"capability_id": "CAP-8F78E58E5656", "capability_name": "Ndsp User Login Gateway", "endpoint_path": "", "original_missing": "ENDPOINT", "resolved": "", "remaining": "ENDPOINT"}, {"capability_id": "CAP-98156F574B28", "capability_name": "Risk Warnings", "endpoint_path": "", "original_missing": "ENDPOINT", "resolved": "", "remaining": "ENDPOINT"}, {"capability_id": "CAP-A61CF5BBAA01", "capability_name": "Ndsp Admin Ui Proxy", "endpoint_path": "", "original_missing": "ENDPOINT", "resolved": "", "remaining": "ENDPOINT"}, {"capability_id": "CAP-C55DEBBD7CB7", "capability_name": "Ndsp User Login Gateway", "endpoint_path": "", "original_missing": "ENDPOINT", "resolved": "", "remaining": "ENDPOINT"}, {"capability_id": "CAP-D054F1321201", "capability_name": "Ndsp User Login Gateway", "endpoint_path": "", "original_missing": "ENDPOINT", "resolved": "", "remaining": "ENDPOINT"}, {"capability_id": "CAP-E6FFD507C6FA", "capability_name": "Ndsp User Login Gateway", "endpoint_path": "", "original_missing": "ENDPOINT", "resolved": "", "remaining": "ENDPOINT"}, {"capability_id": "CAP-F139426B5341", "capability_name": "Ndsp User Login Gateway", "endpoint_path": "", "original_missing": "ENDPOINT", "resolved": "", "remaining": "ENDPOINT"}, {"capability_id": "CAP-F56AB637F669", "capability_name": "Ndsp User Login Gateway", "endpoint_path": "", "original_missing": "ENDPOINT", "resolved": "", "remaining": "ENDPOINT"}];

for (const record of records) {
  test(`PR-029 remaining quick win: ${record.capability_id}`, () => {
    assert.ok(record.capability_id, 'capability id is required');
    assert.ok(record.capability_name, 'capability name is required');

    const original = record.original_missing
      .split('|')
      .filter(Boolean);
    const resolved = record.resolved
      .split('|')
      .filter(Boolean);
    const remaining = record.remaining
      .split('|')
      .filter(Boolean);

    assert.equal(
      new Set([...resolved, ...remaining]).size,
      new Set(original).size,
      'resolved and remaining evidence must account for input gaps',
    );

    for (const item of resolved) {
      assert.ok(original.includes(item));
    }

    for (const item of remaining) {
      assert.ok(original.includes(item));
    }
  });
}
