'use strict';

const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const assert = require('node:assert/strict');

const root = path.resolve(__dirname, '..', '..');
const records = [{"capability_id": "CAP-4FF90CCC6DFE", "capability_name": "Tdl V2 Policy Admin", "selected_route": "", "selected_route_source": "", "accepted_probe_url": "", "accepted_http_status": "", "original_missing_evidence": "REAL_DATA", "resolved_evidence": "", "remaining_missing_evidence": "REAL_DATA"}, {"capability_id": "CAP-8A9DD9B6E7D5", "capability_name": "Tdl V2 Policy Admin", "selected_route": "", "selected_route_source": "", "accepted_probe_url": "", "accepted_http_status": "", "original_missing_evidence": "REAL_DATA", "resolved_evidence": "", "remaining_missing_evidence": "REAL_DATA"}, {"capability_id": "CAP-15C56B60B4B0", "capability_name": "Ndsp User Login Gateway", "selected_route": "GET /api/auth/2fa/status", "selected_route_source": "backend/ndsp_user_login_gateway.cjs:407", "accepted_probe_url": "http://127.0.0.1:443/api/auth/2fa/status", "accepted_http_status": "400", "original_missing_evidence": "ENDPOINT", "resolved_evidence": "ENDPOINT", "remaining_missing_evidence": ""}, {"capability_id": "CAP-214521E6EBD1", "capability_name": "Ndsp User Login Gateway", "selected_route": "GET /api/auth/2fa/status", "selected_route_source": "backend/ndsp_user_login_gateway.cjs:407", "accepted_probe_url": "http://127.0.0.1:443/api/auth/2fa/status", "accepted_http_status": "400", "original_missing_evidence": "ENDPOINT", "resolved_evidence": "ENDPOINT", "remaining_missing_evidence": ""}, {"capability_id": "CAP-242D8324FAD9", "capability_name": "Ndsp User Login Gateway", "selected_route": "GET /api/auth/2fa/status", "selected_route_source": "backend/ndsp_user_login_gateway.cjs:407", "accepted_probe_url": "http://127.0.0.1:443/api/auth/2fa/status", "accepted_http_status": "400", "original_missing_evidence": "ENDPOINT", "resolved_evidence": "ENDPOINT", "remaining_missing_evidence": ""}, {"capability_id": "CAP-3A5ED3DB0C0D", "capability_name": "Risk Label", "selected_route": "GET /risk_state", "selected_route_source": "backend/app/support_layers/scenario/scenario_engine.py:105", "accepted_probe_url": "http://127.0.0.1:443/risk_state", "accepted_http_status": "400", "original_missing_evidence": "ENDPOINT", "resolved_evidence": "ENDPOINT", "remaining_missing_evidence": ""}, {"capability_id": "CAP-3B89863B2015", "capability_name": "Ndsp User Login Gateway", "selected_route": "GET /api/auth/2fa/status", "selected_route_source": "backend/ndsp_user_login_gateway.cjs:407", "accepted_probe_url": "http://127.0.0.1:443/api/auth/2fa/status", "accepted_http_status": "400", "original_missing_evidence": "ENDPOINT", "resolved_evidence": "ENDPOINT", "remaining_missing_evidence": ""}, {"capability_id": "CAP-3D9086A829ED", "capability_name": "Ndsp Admin Ui Proxy", "selected_route": "GET /api/admin-ui/alerts", "selected_route_source": "backend/ndsp_admin_ui_proxy.cjs:486", "accepted_probe_url": "http://127.0.0.1:443/api/admin-ui/alerts", "accepted_http_status": "400", "original_missing_evidence": "ENDPOINT", "resolved_evidence": "ENDPOINT", "remaining_missing_evidence": ""}, {"capability_id": "CAP-4B75FD38F852", "capability_name": "Ndsp Admin Ui Proxy", "selected_route": "GET /api/admin-ui/alerts", "selected_route_source": "backend/ndsp_admin_ui_proxy.cjs:486", "accepted_probe_url": "http://127.0.0.1:443/api/admin-ui/alerts", "accepted_http_status": "400", "original_missing_evidence": "ENDPOINT", "resolved_evidence": "ENDPOINT", "remaining_missing_evidence": ""}, {"capability_id": "CAP-4FCAA631BA18", "capability_name": "Ndsp Admin Actions Bypass Old Middleware", "selected_route": "GET /api/admin-actions/users/action/health", "selected_route_source": "backend/ndsp_admin_actions_bypass_old_middleware.cjs:225", "accepted_probe_url": "http://127.0.0.1:443/api/admin-actions/users/action/health", "accepted_http_status": "400", "original_missing_evidence": "ENDPOINT", "resolved_evidence": "ENDPOINT", "remaining_missing_evidence": ""}, {"capability_id": "CAP-644C81537AC6", "capability_name": "Ndsp User Login Gateway", "selected_route": "GET /api/auth/2fa/status", "selected_route_source": "backend/ndsp_user_login_gateway.cjs:407", "accepted_probe_url": "http://127.0.0.1:443/api/auth/2fa/status", "accepted_http_status": "400", "original_missing_evidence": "ENDPOINT", "resolved_evidence": "ENDPOINT", "remaining_missing_evidence": ""}, {"capability_id": "CAP-6565FE804AF5", "capability_name": "Ndsp User Login Gateway", "selected_route": "GET /api/auth/2fa/status", "selected_route_source": "backend/ndsp_user_login_gateway.cjs:407", "accepted_probe_url": "http://127.0.0.1:443/api/auth/2fa/status", "accepted_http_status": "400", "original_missing_evidence": "ENDPOINT", "resolved_evidence": "ENDPOINT", "remaining_missing_evidence": ""}, {"capability_id": "CAP-8F78E58E5656", "capability_name": "Ndsp User Login Gateway", "selected_route": "GET /api/auth/2fa/status", "selected_route_source": "backend/ndsp_user_login_gateway.cjs:407", "accepted_probe_url": "http://127.0.0.1:443/api/auth/2fa/status", "accepted_http_status": "400", "original_missing_evidence": "ENDPOINT", "resolved_evidence": "ENDPOINT", "remaining_missing_evidence": ""}, {"capability_id": "CAP-98156F574B28", "capability_name": "Risk Warnings", "selected_route": "GET /risk_state", "selected_route_source": "backend/app/support_layers/scenario/scenario_engine.py:105", "accepted_probe_url": "http://127.0.0.1:443/risk_state", "accepted_http_status": "400", "original_missing_evidence": "ENDPOINT", "resolved_evidence": "ENDPOINT", "remaining_missing_evidence": ""}, {"capability_id": "CAP-A61CF5BBAA01", "capability_name": "Ndsp Admin Ui Proxy", "selected_route": "GET /api/admin-ui/alerts", "selected_route_source": "backend/ndsp_admin_ui_proxy.cjs:486", "accepted_probe_url": "http://127.0.0.1:443/api/admin-ui/alerts", "accepted_http_status": "400", "original_missing_evidence": "ENDPOINT", "resolved_evidence": "ENDPOINT", "remaining_missing_evidence": ""}, {"capability_id": "CAP-C55DEBBD7CB7", "capability_name": "Ndsp User Login Gateway", "selected_route": "GET /api/auth/2fa/status", "selected_route_source": "backend/ndsp_user_login_gateway.cjs:407", "accepted_probe_url": "http://127.0.0.1:443/api/auth/2fa/status", "accepted_http_status": "400", "original_missing_evidence": "ENDPOINT", "resolved_evidence": "ENDPOINT", "remaining_missing_evidence": ""}, {"capability_id": "CAP-D054F1321201", "capability_name": "Ndsp User Login Gateway", "selected_route": "GET /api/auth/2fa/status", "selected_route_source": "backend/ndsp_user_login_gateway.cjs:407", "accepted_probe_url": "http://127.0.0.1:443/api/auth/2fa/status", "accepted_http_status": "400", "original_missing_evidence": "ENDPOINT", "resolved_evidence": "ENDPOINT", "remaining_missing_evidence": ""}, {"capability_id": "CAP-E6FFD507C6FA", "capability_name": "Ndsp User Login Gateway", "selected_route": "GET /api/auth/2fa/status", "selected_route_source": "backend/ndsp_user_login_gateway.cjs:407", "accepted_probe_url": "http://127.0.0.1:443/api/auth/2fa/status", "accepted_http_status": "400", "original_missing_evidence": "ENDPOINT", "resolved_evidence": "ENDPOINT", "remaining_missing_evidence": ""}, {"capability_id": "CAP-F139426B5341", "capability_name": "Ndsp User Login Gateway", "selected_route": "GET /api/auth/2fa/status", "selected_route_source": "backend/ndsp_user_login_gateway.cjs:407", "accepted_probe_url": "http://127.0.0.1:443/api/auth/2fa/status", "accepted_http_status": "400", "original_missing_evidence": "ENDPOINT", "resolved_evidence": "ENDPOINT", "remaining_missing_evidence": ""}, {"capability_id": "CAP-F56AB637F669", "capability_name": "Ndsp User Login Gateway", "selected_route": "GET /api/auth/2fa/status", "selected_route_source": "backend/ndsp_user_login_gateway.cjs:407", "accepted_probe_url": "http://127.0.0.1:443/api/auth/2fa/status", "accepted_http_status": "400", "original_missing_evidence": "ENDPOINT", "resolved_evidence": "ENDPOINT", "remaining_missing_evidence": ""}];

for (const record of records) {
  test(`PR-030 endpoint/data: ${record.capability_id}`, () => {
    assert.ok(record.capability_id);
    assert.ok(record.capability_name);

    const original = record.original_missing_evidence
      .split('|')
      .filter(Boolean);
    const resolved = record.resolved_evidence
      .split('|')
      .filter(Boolean);
    const remaining = record.remaining_missing_evidence
      .split('|')
      .filter(Boolean);

    assert.deepEqual(
      [...new Set([...resolved, ...remaining])].sort(),
      [...new Set(original)].sort(),
      'resolved and remaining evidence must account for input gaps',
    );

    if (record.selected_route_source) {
      const sourceFile = record.selected_route_source
        .replace(/:\d+$/, '');
      assert.ok(
        fs.existsSync(path.join(root, sourceFile)),
        `route source missing: ${sourceFile}`,
      );
    }

    if (record.accepted_probe_url) {
      assert.match(
        record.accepted_probe_url,
        /^http:\/\/(127\.0\.0\.1|localhost):\d+\//,
      );
      assert.notEqual(record.accepted_http_status, '404');
    }
  });
}
