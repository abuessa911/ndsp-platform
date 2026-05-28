#!/usr/bin/env bash
set -euo pipefail

SERVER="ndsp.app"
SSH_USER="nawaf511"
ZIP_LOCAL="./Archive.zip"
ZIP_REMOTE="/home/nawaf511/Archive.zip"
APP_NAME="ndsp-archive-app"
PORT="9020"

if [[ ! -f "$ZIP_LOCAL" ]]; then
  echo "❌ لم أجد الملف محلياً: $ZIP_LOCAL"
  echo "ضع Archive.zip بجانب هذا السكربت ثم أعد التشغيل."
  exit 1
fi

echo "== Uploading Archive.zip to server =="
scp "$ZIP_LOCAL" "$SSH_USER@$SERVER:$ZIP_REMOTE"

echo "== Creating and running remote installer =="
ssh "$SSH_USER@$SERVER" "cat > /tmp/run_archive_remote.sh" <<'REMOTE_SCRIPT'
#!/usr/bin/env bash
set -euo pipefail

ZIP_FILE="/home/nawaf511/Archive.zip"
APP_NAME="ndsp-archive-app"
INSTALL_DIR="/opt/$APP_NAME"
BACKUP_DIR="/root/${APP_NAME}_backup_$(date +%Y%m%d_%H%M%S)"
SERVICE_NAME="$APP_NAME"
PORT="9020"

if [[ "$EUID" -ne 0 ]]; then
  echo "❌ سيتم تشغيل هذا السكربت عبر sudo"
  exit 1
fi

if [[ ! -f "$ZIP_FILE" ]]; then
  echo "❌ الملف غير موجود على السيرفر: $ZIP_FILE"
  exit 1
fi

echo "== Installing required packages =="
apt-get update -y
apt-get install -y unzip rsync curl nginx

mkdir -p "$BACKUP_DIR"

if [[ -d "$INSTALL_DIR" ]]; then
  echo "== Backup old install =="
  cp -a "$INSTALL_DIR" "$BACKUP_DIR/app"
fi

rm -rf "$INSTALL_DIR"
mkdir -p "$INSTALL_DIR"

echo "== Extracting archive =="
unzip -q "$ZIP_FILE" -d "$INSTALL_DIR"

echo "== Normalizing archive root =="
shopt -s dotglob nullglob
items=("$INSTALL_DIR"/*)

if [[ ${#items[@]} -eq 1 && -d "${items[0]}" ]]; then
  INNER="${items[0]}"
  TMP="${INSTALL_DIR}_tmp"
  rm -rf "$TMP"
  mv "$INNER" "$TMP"
  rm -rf "$INSTALL_DIR"
  mv "$TMP" "$INSTALL_DIR"
fi

cd "$INSTALL_DIR"

echo "== Files detected =="
find "$INSTALL_DIR" -maxdepth 2 -type f | sed "s#$INSTALL_DIR/##" | head -n 100

echo "== Detecting project type =="

if [[ -f package.json ]]; then
  echo "✅ Node project detected"

  if ! command -v node >/dev/null 2>&1; then
    echo "❌ Node.js غير مثبت على السيرفر"
    exit 1
  fi

  npm install

  if grep -q '"build"' package.json; then
    echo "== Building Node project =="
    export QT_QPA_PLATFORM=offscreen
    export CI=true

    node <<'NODE'
const fs = require('fs');
const p = 'package.json';
const pkg = JSON.parse(fs.readFileSync(p, 'utf8'));

if (pkg.scripts && pkg.scripts.build === 'vite build' && fs.existsSync('./node_modules/vite/bin/vite.js')) {
  pkg.scripts.build = 'QT_QPA_PLATFORM=offscreen node ./node_modules/vite/bin/vite.js build';
  fs.writeFileSync(p, JSON.stringify(pkg, null, 2) + '\n');
}
NODE

    npm run build
  fi

  START_CMD=""

  if grep -q '"start"' package.json; then
    START_CMD="npm start"
  elif grep -q '"preview"' package.json; then
    START_CMD="npm run preview -- --host 127.0.0.1 --port $PORT"
  elif grep -q '"dev"' package.json; then
    START_CMD="npm run dev -- --host 127.0.0.1 --port $PORT"
  elif [[ -f server.js ]]; then
    START_CMD="node server.js"
  elif [[ -f index.js ]]; then
    START_CMD="node index.js"
  elif [[ -f app.js ]]; then
    START_CMD="node app.js"
  elif [[ -d dist ]]; then
    START_CMD="npx serve -s dist -l 127.0.0.1:$PORT"
    npm install serve --save-dev
  else
    echo "❌ لم أجد أمر تشغيل مناسب داخل package.json"
    exit 1
  fi

  cat > "/etc/systemd/system/${SERVICE_NAME}.service" <<EOF
[Unit]
Description=NDSP Archive App
After=network.target

[Service]
Type=simple
WorkingDirectory=$INSTALL_DIR
Environment=NODE_ENV=production
Environment=PORT=$PORT
Environment=HOST=127.0.0.1
ExecStart=/bin/bash -lc '$START_CMD'
Restart=always
RestartSec=3
User=root

[Install]
WantedBy=multi-user.target
EOF

  systemctl daemon-reload
  systemctl enable "$SERVICE_NAME"
  systemctl restart "$SERVICE_NAME"

  sleep 3

  systemctl is-active --quiet "$SERVICE_NAME" \
    && echo "✅ Service active: $SERVICE_NAME" \
    || { echo "❌ Service failed"; systemctl status "$SERVICE_NAME" --no-pager -l; exit 1; }

  echo "✅ Node app running on http://127.0.0.1:$PORT"

elif [[ -f index.html ]]; then
  echo "✅ Static HTML project detected"

  STATIC_DIR="/var/www/html/archive-app"
  mkdir -p "$STATIC_DIR"
  rsync -a --delete "$INSTALL_DIR/" "$STATIC_DIR/"

  systemctl reload nginx || true

  echo "✅ Static app deployed:"
  echo "https://ndsp.app/archive-app/"

elif [[ -f requirements.txt || -f app.py || -f main.py ]]; then
  echo "✅ Python project detected"

  apt-get install -y python3 python3-venv python3-pip

  python3 -m venv venv
  source venv/bin/activate

  if [[ -f requirements.txt ]]; then
    pip install -r requirements.txt
  fi

  PY_FILE=""
  [[ -f app.py ]] && PY_FILE="app.py"
  [[ -f main.py ]] && PY_FILE="main.py"

  if [[ -z "$PY_FILE" ]]; then
    echo "❌ لم أجد app.py أو main.py"
    exit 1
  fi

  cat > "/etc/systemd/system/${SERVICE_NAME}.service" <<EOF
[Unit]
Description=NDSP Archive Python App
After=network.target

[Service]
Type=simple
WorkingDirectory=$INSTALL_DIR
Environment=PORT=$PORT
ExecStart=$INSTALL_DIR/venv/bin/python $INSTALL_DIR/$PY_FILE
Restart=always
RestartSec=3
User=root

[Install]
WantedBy=multi-user.target
EOF

  systemctl daemon-reload
  systemctl enable "$SERVICE_NAME"
  systemctl restart "$SERVICE_NAME"

  sleep 3

  systemctl is-active --quiet "$SERVICE_NAME" \
    && echo "✅ Service active: $SERVICE_NAME" \
    || { echo "❌ Service failed"; systemctl status "$SERVICE_NAME" --no-pager -l; exit 1; }

  echo "✅ Python app running on port $PORT"

else
  echo "❌ لم أتعرف على نوع المشروع داخل الأرشيف"
  echo "أرسل ناتج:"
  echo "find $INSTALL_DIR -maxdepth 2 -type f | sed 's#$INSTALL_DIR/##' | head -n 100"
  exit 1
fi

echo ""
echo "== Done =="
echo "Backup saved at: $BACKUP_DIR"
REMOTE_SCRIPT

ssh "$SSH_USER@$SERVER" "chmod +x /tmp/run_archive_remote.sh && sudo /tmp/run_archive_remote.sh"

echo ""
echo "✅ انتهى الرفع والتشغيل"
echo ""
echo "لو كان المشروع Static افتح:"
echo "https://ndsp.app/archive-app/"
echo ""
echo "لو كان المشروع خدمة Node/Python تحقق من الحالة:"
echo "ssh $SSH_USER@$SERVER 'sudo systemctl status ndsp-archive-app --no-pager -l'"
echo ""
echo "ولعرض السجلات:"
echo "ssh $SSH_USER@$SERVER 'sudo journalctl -u ndsp-archive-app -n 100 --no-pager'"
