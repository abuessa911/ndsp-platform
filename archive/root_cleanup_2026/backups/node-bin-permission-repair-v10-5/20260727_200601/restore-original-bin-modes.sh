#!/usr/bin/env bash
set -Eeuo pipefail
set +H

[[ "$(id -u)" -eq 0 ]] || {
    echo "Run with sudo: sudo bash $0"
    exit 1
}
chmod 644 -- /opt/ndsp-auth-core-clean/releases/20260724_050053-final-ux-v31/node_modules/@babel/parser/bin/babel-parser.js
chmod 644 -- /opt/ndsp-auth-core-clean/releases/20260724_050053-final-ux-v31/node_modules/baseline-browser-mapping/dist/cli.cjs
chmod 644 -- /opt/ndsp-auth-core-clean/releases/20260724_050053-final-ux-v31/node_modules/bcryptjs/bin/bcrypt
chmod 644 -- /opt/ndsp-auth-core-clean/releases/20260724_050053-final-ux-v31/node_modules/browserslist/cli.js
chmod 644 -- /opt/ndsp-auth-core-clean/releases/20260724_050053-final-ux-v31/node_modules/esbuild/bin/esbuild
chmod 644 -- /opt/ndsp-auth-core-clean/releases/20260724_050053-final-ux-v31/node_modules/jsesc/bin/jsesc
chmod 644 -- /opt/ndsp-auth-core-clean/releases/20260724_050053-final-ux-v31/node_modules/json5/lib/cli.js
chmod 644 -- /opt/ndsp-auth-core-clean/releases/20260724_050053-final-ux-v31/node_modules/loose-envify/cli.js
chmod 644 -- /opt/ndsp-auth-core-clean/releases/20260724_050053-final-ux-v31/node_modules/nanoid/bin/nanoid.cjs
chmod 644 -- /opt/ndsp-auth-core-clean/releases/20260724_050053-final-ux-v31/node_modules/pino/bin.js
chmod 644 -- /opt/ndsp-auth-core-clean/releases/20260724_050053-final-ux-v31/node_modules/rollup/dist/bin/rollup
chmod 644 -- /opt/ndsp-auth-core-clean/releases/20260724_050053-final-ux-v31/node_modules/safe-regex2/bin/safe-regex2.js
chmod 644 -- /opt/ndsp-auth-core-clean/releases/20260724_050053-final-ux-v31/node_modules/semver/bin/semver.js
chmod 644 -- /opt/ndsp-auth-core-clean/releases/20260724_050053-final-ux-v31/node_modules/typescript/bin/tsc
chmod 644 -- /opt/ndsp-auth-core-clean/releases/20260724_050053-final-ux-v31/node_modules/typescript/bin/tsserver
chmod 644 -- /opt/ndsp-auth-core-clean/releases/20260724_050053-final-ux-v31/node_modules/update-browserslist-db/cli.js
chmod 644 -- /opt/ndsp-auth-core-clean/releases/20260724_050053-final-ux-v31/node_modules/vite/bin/vite.js
echo "ORIGINAL_NODE_BIN_MODES_RESTORED=YES"
