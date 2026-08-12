# NDSP Asset View Preflight
DATE=2026-07-07T10:09:21+02:00
FRONTEND=/var/www/ndsp-my

## 1) Target file
-rw-rw-r-- 1 nawaf511 nawaf511 2.8K يوليو   7 09:48 /var/www/ndsp-my/NDSP_Asset_View.html

## 2) HTML markers
7:<title>NDSP — الأسواق والأصول</title>
11:<link rel="stylesheet" href="/assets/markets-hq.css?v=14">
12:    <link rel="stylesheet" href="/assets/ndsp-global-menu.css?v=24-page-match">
13:  <link rel="stylesheet" href="/assets/ndsp-page-name-sync-v25.css?v=25-page-name">
14:  <script src="/assets/ndsp-disclaimer-gate.js?v=1"></script>
15:  <!-- NDSP_CANONICAL_PAGE_ALIAS_V1 source=asset-selector.html -->
22:      <div class="title">
24:        <h1 data-i18n="title">الأسواق والأصول</h1>
34:      <div class="sum"><small data-i18n="markets">الأسواق</small><b id="marketCount">7</b></div>
35:      <div class="sum"><small data-i18n="assets">الأصول</small><b id="assetTotal">54</b></div>
52:    <div id="assetCount" class="count">—</div>
55:  <section id="assetGrid" class="grid"></section>
61:<script src="/assets/markets-hq.js?v=14"></script>
62:    <script src="/assets/ndsp-global-menu.js?v=25-canonical-page-match"></script>
63:  <script src="/assets/ndsp-page-name-sync-v25.js?v=25-page-name"></script>

## 3) Asset data file
-rw-rw-r-- 1 nawaf511 nawaf511 3.4K يوليو   5 15:19 /var/www/ndsp-my/assets/ndsp-assets.json
[{"market": "CRYPTO", "symbol": "BTCUSDT", "name": "Bitcoin"}, {"market": "CRYPTO", "symbol": "ETHUSDT", "name": "Ethereum"}, {"market": "CRYPTO", "symbol": "BNBUSDT", "name": "BNB"}, {"market": "CRYPTO", "symbol": "SOLUSDT", "name": "Solana"}, {"market": "CRYPTO", "symbol": "XRPUSDT", "name": "XRP"}, {"market": "CRYPTO", "symbol": "ADAUSDT", "name": "Cardano"}, {"market": "CRYPTO", "symbol": "DOGEUSDT", "name": "Dogecoin"}, {"market": "CRYPTO", "symbol": "AVAXUSDT", "name": "Avalanche"}, {"market": "CRYPTO", "symbol": "LINKUSDT", "name": "Chainlink"}, {"market": "CRYPTO", "symbol": "DOTUSDT", "name": "Polkadot"}, {"market": "CRYPTO", "symbol": "TRXUSDT", "name": "TRON"}, {"market": "CRYPTO", "symbol": "MATICUSDT", "name": "Polygon"}, {"market": "CRYPTO", "symbol": "LTCUSDT", "name": "Litecoin"}, {"market": "CRYPTO", "symbol": "BCHUSDT", "name": "Bitcoin Cash"}, {"market": "CRYPTO", "symbol": "ATOMUSDT", "name": "Cosmos"}, {"market": "CRYPTO", "symbol": "UNIUSDT", "name": "Uniswap"}, {"market": "CRYPTO", "symbol": "AAVEUSDT", "name": "Aave"}, {"market": "CRYPTO", "symbol": "NEARUSDT", "name": "Near"}, {"market": "CRYPTO", "symbol": "ARBUSDT", "name": "Arbitrum"}, {"market": "FX", "

## 4) Script references
10:<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800;900&family=Inter:wght@400;600;700;800;900&display=swap" rel="stylesheet">
11:<link rel="stylesheet" href="/assets/markets-hq.css?v=14">
12:    <link rel="stylesheet" href="/assets/ndsp-global-menu.css?v=24-page-match">
13:  <link rel="stylesheet" href="/assets/ndsp-page-name-sync-v25.css?v=25-page-name">
14:  <script src="/assets/ndsp-disclaimer-gate.js?v=1"></script>
61:<script src="/assets/markets-hq.js?v=14"></script>
62:    <script src="/assets/ndsp-global-menu.js?v=25-canonical-page-match"></script>
63:  <script src="/assets/ndsp-page-name-sync-v25.js?v=25-page-name"></script>

## 5) HTTP checks
[200] size=2789 https://my.ndsp.app/NDSP_Asset_View.html
[200] size=2610 https://my.ndsp.app/decision-support.html
[200] size=3310 https://my.ndsp.app/NDSP_Command_Center.html

## 6) API sample
ok= True
symbol= ETHUSDT
live_price= 1771.24
quality= 86
scenario= UNDER_MONITORING
nmp= AVAILABLE 1583.4

FINAL_STATUS=ASSET_VIEW_PREFLIGHT_DONE
REPORT=docs/05-runbooks/NDSP_ASSET_VIEW_PREFLIGHT_20260707_100921.md
