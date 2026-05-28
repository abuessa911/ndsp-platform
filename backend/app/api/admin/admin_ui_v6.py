from __future__ import annotations

import os

from fastapi import APIRouter, Request, Request, Query, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from app.core.elite_trial_capacity import enforce_elite_trial_capacity

router = APIRouter(prefix="/api/admin", tags=["admin-ui"])


def _admin_ui_key() -> str:
    return os.getenv("ADMIN_UI_KEY", "").strip()


def _require_ui_key(admin_key: str | None):
    expected = _admin_ui_key()

    if not expected:
        raise HTTPException(
            status_code=503,
            detail="ADMIN_UI_KEY is not configured",
        )

    if not admin_key or admin_key != expected:
        raise HTTPException(
            status_code=403,
            detail="Invalid admin_key",
        )


@router.get("/ui", response_class=HTMLResponse)
def admin_ui(admin_key: str | None = Query(default=None)):
    _require_ui_key(admin_key)

    html = """
<!doctype html>
<html lang="en" dir="ltr">
<head>
  <meta charset="utf-8">
  <title>Nawaf Decision Support Platform Admin Control Center</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body {
      font-family: Arial, sans-serif;
      background: #0f172a;
      color: #e5e7eb;
      margin: 0;
      padding: 24px;
    }
    h1, h2 {
      margin: 0 0 12px;
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 16px;
      margin-bottom: 24px;
    }
    .card {
      background: #111827;
      border: 1px solid #1f2937;
      border-radius: 14px;
      padding: 16px;
      box-shadow: 0 8px 24px rgba(0,0,0,.25);
      margin-bottom: 24px;
    }
    .value {
      font-size: 32px;
      font-weight: bold;
      color: #38bdf8;
    }
    .muted {
      color: #9ca3af;
      font-size: 13px;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin: 12px 0 24px;
      background: #111827;
      border-radius: 14px;
      overflow: hidden;
    }
    th, td {
      border-bottom: 1px solid #1f2937;
      padding: 10px;
      text-align: left;
      font-size: 13px;
      vertical-align: top;
    }
    th {
      background: #1f2937;
      color: #f9fafb;
    }
    code {
      direction: ltr;
      display: inline-block;
      color: #a7f3d0;
      word-break: break-all;
    }
    button {
      background: #2563eb;
      color: white;
      border: 0;
      padding: 10px 14px;
      border-radius: 10px;
      cursor: pointer;
      margin: 4px;
    }
    button:hover {
      background: #1d4ed8;
    }
    input, select {
      background: #020617;
      color: #e5e7eb;
      border: 1px solid #334155;
      padding: 10px;
      border-radius: 10px;
      margin: 4px;
      min-width: 180px;
    }
    .ok {
      color: #22c55e;
      font-weight: bold;
    }
    .bad {
      color: #ef4444;
      font-weight: bold;
    }
    .bad-btn {
      background: #dc2626;
    }
    .bad-btn:hover {
      background: #b91c1c;
    }
    .copy-btn {
      background: #059669;
      padding: 7px 10px;
      font-size: 12px;
    }
    .copy-btn:hover {
      background: #047857;
    }
    .section-head {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      margin-top: 28px;
    }
    .section-head h2 {
      margin: 0;
    }
    pre {
      direction: ltr;
      text-align: left;
      background: #020617;
      padding: 12px;
      border-radius: 10px;
      overflow-x: auto;
      white-space: pre-wrap;
    }
  
    .section-title {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      margin: 34px 0 14px;
    }
    .section-title h2 {
      margin: 0;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 14px;
      overflow: hidden;
      border-radius: 14px;
    }
    th, td {
      text-align: left !important;
      padding: 12px 14px;
      border-bottom: 1px solid rgba(148, 163, 184, 0.16);
      vertical-align: top;
      font-size: 14px;
    }
    th {
      color: #94a3b8;
      font-weight: 700;
      background: rgba(15, 23, 42, 0.55);
    }
    td {
      color: #e5e7eb;
      word-break: break-word;
    }
    .result-box, #action_result {
      direction: ltr;
      text-align: left;
      white-space: pre-wrap;
      overflow: auto;
      max-height: 360px;
    }


    .brand-subtitle {
      margin-top: 8px;
      margin-bottom: 18px;
      font-size: 28px;
      font-weight: 800;
      letter-spacing: 0.08em;
      color: #38bdf8;
    }

    .footer-rights {
      margin-top: 60px;
      padding: 28px 0;
      color: #94a3b8;
      font-size: 14px;
      text-align: center;
      border-top: 1px solid rgba(148, 163, 184, 0.16);
    }


    .quick-links {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-top: 18px;
      margin-bottom: 10px;
    }
    .quick-links a {
      display: inline-block;
      text-decoration: none;
      color: #38bdf8;
      background: rgba(56, 189, 248, .08);
      border: 1px solid rgba(56, 189, 248, .28);
      border-radius: 999px;
      padding: 8px 12px;
      font-size: 13px;
      font-weight: 700;
    }
    .quick-links a:hover {
      background: rgba(56, 189, 248, .16);
    }
    .card {
      transition: transform .12s ease, border-color .12s ease, background .12s ease;
    }
    .card:hover {
      transform: translateY(-1px);
      border-color: rgba(56, 189, 248, .35);
    }

</style>




<style id="ndsp-admin-ui-v12-existing-table-filters">
  #ndsp-v12-existing-filter {
    display: block !important;
    width: 100%;
    margin: 26px 0 30px;
    padding: 18px;
    border: 1px solid rgba(56,189,248,.38);
    border-radius: 22px;
    background: linear-gradient(135deg, rgba(15,23,42,.96), rgba(2,6,23,.88));
    box-shadow: 0 18px 55px rgba(0,0,0,.28);
  }

  .ndsp-v12-filter-title {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 14px;
    font-size: 18px;
    font-weight: 900;
    color: #e5e7eb;
  }

  .ndsp-v12-version {
    display: inline-flex;
    padding: 4px 10px;
    border: 1px solid rgba(56,189,248,.35);
    border-radius: 999px;
    color: #bae6fd;
    background: rgba(56,189,248,.12);
    font-size: 11px;
    font-weight: 900;
    letter-spacing: .06em;
  }

  .ndsp-v12-filter-grid {
    display: grid;
    grid-template-columns: 1.6fr repeat(4, minmax(145px, 1fr)) auto;
    gap: 10px;
    align-items: center;
  }

  #ndsp-v12-existing-filter input,
  #ndsp-v12-existing-filter select {
    height: 46px;
    width: 100%;
    padding: 0 14px;
    color: #e5e7eb;
    background: rgba(2,6,23,.78);
    border: 1px solid rgba(148,163,184,.28);
    border-radius: 14px;
    outline: none;
    font-size: 14px;
  }

  #ndsp-v12-existing-filter input:focus,
  #ndsp-v12-existing-filter select:focus {
    border-color: rgba(56,189,248,.9);
    box-shadow: 0 0 0 3px rgba(56,189,248,.15);
  }

  #ndsp-v12-existing-filter option {
    background: #020617;
    color: #e5e7eb;
  }

  .ndsp-v12-reset {
    height: 46px;
    padding: 0 18px;
    border-radius: 14px;
    border: 1px solid rgba(148,163,184,.28);
    background: rgba(15,23,42,.95);
    color: #e5e7eb;
    font-weight: 900;
    cursor: pointer;
  }

  .ndsp-v12-reset:hover {
    border-color: rgba(56,189,248,.8);
  }

  .ndsp-v12-row-hidden {
    display: none !important;
  }

  .ndsp-v12-pill {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    min-height: 25px;
    padding: 4px 10px;
    border-radius: 999px;
    border: 1px solid rgba(148,163,184,.22);
    background: rgba(148,163,184,.10);
    color: #dbeafe;
    font-size: 13px;
    font-weight: 900;
    white-space: nowrap;
  }

  .ndsp-v12-pill::before {
    content: "";
    width: 7px;
    height: 7px;
    border-radius: 999px;
    background: #94a3b8;
  }

  .ndsp-v12-pill.active,
  .ndsp-v12-pill.confirmed,
  .ndsp-v12-pill.running,
  .ndsp-v12-pill.ok,
  .ndsp-v12-pill.paid {
    color: #bbf7d0;
    background: rgba(34,197,94,.12);
    border-color: rgba(34,197,94,.34);
  }

  .ndsp-v12-pill.active::before,
  .ndsp-v12-pill.confirmed::before,
  .ndsp-v12-pill.running::before,
  .ndsp-v12-pill.ok::before,
  .ndsp-v12-pill.paid::before {
    background: #22c55e;
  }

  .ndsp-v12-pill.cancelled,
  .ndsp-v12-pill.canceled,
  .ndsp-v12-pill.failed,
  .ndsp-v12-pill.error,
  .ndsp-v12-pill.revoked {
    color: #fecaca;
    background: rgba(239,68,68,.12);
    border-color: rgba(239,68,68,.34);
  }

  .ndsp-v12-pill.cancelled::before,
  .ndsp-v12-pill.canceled::before,
  .ndsp-v12-pill.failed::before,
  .ndsp-v12-pill.error::before,
  .ndsp-v12-pill.revoked::before {
    background: #ef4444;
  }

  table tbody tr:hover {
    background: rgba(56,189,248,.055);
  }

  @media (max-width: 1100px) {
    .ndsp-v12-filter-grid {
      grid-template-columns: 1fr 1fr;
    }
  }

  @media (max-width: 700px) {
    .ndsp-v12-filter-grid {
      grid-template-columns: 1fr;
    }
  }
</style>


<style id="ndsp-admin-ui-v12-service-status-bar">
  #ndsp-v12-service-status-bar {
    display: block !important;
    width: 100%;
    margin: 22px 0 22px;
    padding: 16px;
    border: 1px solid rgba(56,189,248,.34);
    border-radius: 22px;
    background:
      radial-gradient(circle at top left, rgba(56,189,248,.14), transparent 30%),
      linear-gradient(135deg, rgba(15,23,42,.96), rgba(2,6,23,.88));
    box-shadow: 0 18px 55px rgba(0,0,0,.28);
  }

  .ndsp-v12-status-title {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 14px;
    margin-bottom: 14px;
  }

  .ndsp-v12-status-title strong {
    color: #e5e7eb;
    font-size: 18px;
    font-weight: 900;
  }

  .ndsp-v12-status-version {
    display: inline-flex;
    padding: 4px 10px;
    border: 1px solid rgba(56,189,248,.35);
    border-radius: 999px;
    color: #bae6fd;
    background: rgba(56,189,248,.12);
    font-size: 11px;
    font-weight: 900;
    letter-spacing: .06em;
    white-space: nowrap;
  }

  .ndsp-v12-status-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(160px, 1fr));
    gap: 12px;
  }

  .ndsp-v12-status-card {
    min-height: 82px;
    padding: 14px;
    border-radius: 18px;
    border: 1px solid rgba(148,163,184,.18);
    background: rgba(15,23,42,.72);
  }

  .ndsp-v12-status-label {
    color: #94a3b8;
    font-size: 13px;
    font-weight: 800;
    margin-bottom: 8px;
  }

  .ndsp-v12-status-value {
    display: inline-flex;
    align-items: center;
    gap: 9px;
    color: #e5e7eb;
    font-size: 24px;
    font-weight: 950;
    line-height: 1.1;
  }

  .ndsp-v12-status-dot {
    width: 11px;
    height: 11px;
    border-radius: 999px;
    background: #94a3b8;
    box-shadow: 0 0 0 5px rgba(148,163,184,.10);
  }

  .ndsp-v12-status-card.ok {
    border-color: rgba(34,197,94,.32);
    background: rgba(34,197,94,.08);
  }

  .ndsp-v12-status-card.ok .ndsp-v12-status-value {
    color: #86efac;
  }

  .ndsp-v12-status-card.ok .ndsp-v12-status-dot {
    background: #22c55e;
    box-shadow: 0 0 0 5px rgba(34,197,94,.14);
  }

  .ndsp-v12-status-card.warn {
    border-color: rgba(245,158,11,.34);
    background: rgba(245,158,11,.08);
  }

  .ndsp-v12-status-card.warn .ndsp-v12-status-value {
    color: #fde68a;
  }

  .ndsp-v12-status-card.warn .ndsp-v12-status-dot {
    background: #f59e0b;
    box-shadow: 0 0 0 5px rgba(245,158,11,.14);
  }

  .ndsp-v12-status-card.down {
    border-color: rgba(239,68,68,.34);
    background: rgba(239,68,68,.08);
  }

  .ndsp-v12-status-card.down .ndsp-v12-status-value {
    color: #fecaca;
  }

  .ndsp-v12-status-card.down .ndsp-v12-status-dot {
    background: #ef4444;
    box-shadow: 0 0 0 5px rgba(239,68,68,.14);
  }

  @media (max-width: 1100px) {
    .ndsp-v12-status-grid {
      grid-template-columns: 1fr 1fr;
    }
  }

  @media (max-width: 700px) {
    .ndsp-v12-status-grid {
      grid-template-columns: 1fr;
    }

    .ndsp-v12-status-title {
      align-items: flex-start;
      flex-direction: column;
    }
  }
</style>


<style id="ndsp-admin-ui-v13-safety-hardening">
  #ndsp-v13-toast-root {
    position: fixed;
    top: 18px;
    right: 18px;
    z-index: 999999;
    display: flex;
    flex-direction: column;
    gap: 10px;
    pointer-events: none;
  }

  .ndsp-v13-toast {
    min-width: 280px;
    max-width: 460px;
    padding: 14px 16px;
    border-radius: 16px;
    border: 1px solid rgba(148,163,184,.25);
    background: rgba(15,23,42,.96);
    color: #e5e7eb;
    box-shadow: 0 18px 50px rgba(0,0,0,.35);
    font-weight: 800;
    pointer-events: auto;
  }

  .ndsp-v13-toast.ok {
    border-color: rgba(34,197,94,.38);
    background: rgba(20,83,45,.96);
    color: #dcfce7;
  }

  .ndsp-v13-toast.warn {
    border-color: rgba(245,158,11,.38);
    background: rgba(120,53,15,.96);
    color: #fef3c7;
  }

  .ndsp-v13-toast.error {
    border-color: rgba(239,68,68,.38);
    background: rgba(127,29,29,.96);
    color: #fee2e2;
  }

  #ndsp-v13-confirm-modal {
    position: fixed;
    inset: 0;
    z-index: 999998;
    display: none;
    align-items: center;
    justify-content: center;
    background: rgba(2,6,23,.74);
    backdrop-filter: blur(8px);
  }

  #ndsp-v13-confirm-modal.show {
    display: flex;
  }

  .ndsp-v13-modal-card {
    width: min(560px, calc(100vw - 34px));
    border-radius: 24px;
    border: 1px solid rgba(56,189,248,.28);
    background: linear-gradient(135deg, rgba(15,23,42,.98), rgba(2,6,23,.96));
    box-shadow: 0 24px 90px rgba(0,0,0,.55);
    padding: 22px;
  }

  .ndsp-v13-modal-title {
    color: #e5e7eb;
    font-size: 24px;
    font-weight: 950;
    margin-bottom: 10px;
  }

  .ndsp-v13-modal-message {
    color: #cbd5e1;
    font-size: 15px;
    line-height: 1.7;
    margin-bottom: 18px;
    white-space: pre-wrap;
  }

  .ndsp-v13-modal-actions {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
  }

  .ndsp-v13-modal-actions button {
    height: 44px;
    border-radius: 14px;
    border: 1px solid rgba(148,163,184,.25);
    padding: 0 16px;
    color: #e5e7eb;
    background: rgba(15,23,42,.92);
    font-weight: 900;
    cursor: pointer;
  }

  #ndsp-v13-confirm-yes {
    background: #dc2626;
    border-color: rgba(248,113,113,.5);
  }

  #ndsp-v13-confirm-no:hover {
    border-color: rgba(56,189,248,.75);
  }

  #ndsp-v13-confirm-yes:hover {
    background: #b91c1c;
  }

  button.ndsp-v13-busy {
    opacity: .62 !important;
    pointer-events: none !important;
    cursor: wait !important;
  }

  .ndsp-v13-guarded {
    position: relative;
  }

  .ndsp-v13-guarded::after {
    content: " guarded";
    margin-left: 7px;
    font-size: 10px;
    opacity: .72;
    text-transform: uppercase;
    letter-spacing: .06em;
  }

  @media (max-width: 700px) {
    #ndsp-v13-toast-root {
      left: 12px;
      right: 12px;
      top: 12px;
    }

    .ndsp-v13-toast {
      min-width: unset;
      max-width: unset;
      width: 100%;
    }

    .ndsp-v13-modal-actions {
      flex-direction: column-reverse;
    }

    .ndsp-v13-modal-actions button {
      width: 100%;
    }
  }
</style>


<style id="ndsp-admin-ui-v14-diagnostics-center">
  #ndsp-v14-diagnostics-center {
    margin: 24px 0 30px;
    padding: 18px;
    border-radius: 24px;
    border: 1px solid rgba(167,139,250,.28);
    background:
      radial-gradient(circle at top right, rgba(167,139,250,.15), transparent 28%),
      linear-gradient(135deg, rgba(15,23,42,.96), rgba(2,6,23,.88));
    box-shadow: 0 18px 55px rgba(0,0,0,.26);
  }

  .ndsp-v14-diagnostics-head {
    display: flex;
    justify-content: space-between;
    gap: 16px;
    align-items: flex-start;
    margin-bottom: 16px;
  }

  .ndsp-v14-diagnostics-head h2 {
    margin: 0 0 5px;
    color: #e5e7eb;
    font-size: 22px;
    font-weight: 950;
  }

  .ndsp-v14-diagnostics-head p {
    margin: 0;
    color: #94a3b8;
    font-size: 14px;
    line-height: 1.6;
  }

  .ndsp-v14-version {
    display: inline-flex;
    padding: 4px 10px;
    border: 1px solid rgba(167,139,250,.38);
    border-radius: 999px;
    color: #ddd6fe;
    background: rgba(167,139,250,.12);
    font-size: 11px;
    font-weight: 900;
    letter-spacing: .06em;
    white-space: nowrap;
  }

  .ndsp-v14-diagnostics-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 12px;
  }

  .ndsp-v14-diagnostic-card {
    display: flex;
    justify-content: space-between;
    gap: 14px;
    align-items: center;
    padding: 15px;
    border-radius: 18px;
    border: 1px solid rgba(148,163,184,.18);
    background: rgba(15,23,42,.64);
  }

  .ndsp-v14-diagnostic-card strong {
    display: block;
    color: #e5e7eb;
    font-size: 15px;
    font-weight: 950;
    margin-bottom: 5px;
  }

  .ndsp-v14-diagnostic-card p {
    margin: 0;
    color: #94a3b8;
    font-size: 13px;
    line-height: 1.55;
  }

  .ndsp-v14-diagnostic-actions {
    display: flex;
    gap: 8px;
    flex-shrink: 0;
  }

  .ndsp-v14-diagnostic-actions a,
  .ndsp-v14-diagnostic-actions button {
    height: 38px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 0 12px;
    border-radius: 12px;
    border: 1px solid rgba(148,163,184,.25);
    background: rgba(2,6,23,.70);
    color: #e5e7eb;
    font-size: 13px;
    font-weight: 900;
    text-decoration: none;
    cursor: pointer;
    white-space: nowrap;
  }

  .ndsp-v14-diagnostic-actions a:hover,
  .ndsp-v14-diagnostic-actions button:hover {
    border-color: rgba(167,139,250,.75);
    background: rgba(30,41,59,.82);
  }

  @media (max-width: 1050px) {
    .ndsp-v14-diagnostics-grid {
      grid-template-columns: 1fr;
    }
  }

  @media (max-width: 680px) {
    .ndsp-v14-diagnostics-head,
    .ndsp-v14-diagnostic-card,
    .ndsp-v14-diagnostic-actions {
      flex-direction: column;
      align-items: stretch;
    }

    .ndsp-v14-diagnostic-actions a,
    .ndsp-v14-diagnostic-actions button {
      width: 100%;
    }
  }
</style>


<style id="ndsp-admin-ui-v15-audit-center">
  #ndsp-v15-audit-center {
    margin: 24px 0 30px;
    padding: 18px;
    border-radius: 24px;
    border: 1px solid rgba(34,197,94,.28);
    background:
      radial-gradient(circle at top right, rgba(34,197,94,.13), transparent 30%),
      linear-gradient(135deg, rgba(15,23,42,.96), rgba(2,6,23,.88));
    box-shadow: 0 18px 55px rgba(0,0,0,.24);
  }

  .ndsp-v15-audit-head {
    display: flex;
    justify-content: space-between;
    gap: 16px;
    align-items: flex-start;
    margin-bottom: 16px;
  }

  .ndsp-v15-audit-head h2 {
    margin: 0 0 5px;
    color: #e5e7eb;
    font-size: 22px;
    font-weight: 950;
  }

  .ndsp-v15-audit-head p {
    margin: 0;
    color: #94a3b8;
    font-size: 14px;
    line-height: 1.6;
  }

  .ndsp-v15-audit-actions {
    display: flex;
    gap: 10px;
    align-items: center;
    flex-shrink: 0;
  }

  .ndsp-v15-version {
    display: inline-flex;
    padding: 4px 10px;
    border: 1px solid rgba(34,197,94,.38);
    border-radius: 999px;
    color: #bbf7d0;
    background: rgba(34,197,94,.12);
    font-size: 11px;
    font-weight: 900;
    letter-spacing: .06em;
    white-space: nowrap;
  }

  #ndsp-v15-refresh-audit {
    height: 38px;
    border-radius: 12px;
    border: 1px solid rgba(34,197,94,.38);
    background: rgba(20,83,45,.55);
    color: #dcfce7;
    font-size: 13px;
    font-weight: 900;
    cursor: pointer;
    padding: 0 13px;
  }

  .ndsp-v15-audit-summary {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 12px;
    margin-bottom: 14px;
  }

  .ndsp-v15-audit-summary > div {
    padding: 14px;
    border-radius: 18px;
    border: 1px solid rgba(148,163,184,.18);
    background: rgba(15,23,42,.64);
  }

  .ndsp-v15-audit-summary strong {
    display: block;
    color: #e5e7eb;
    font-size: 22px;
    font-weight: 950;
    margin-bottom: 4px;
  }

  .ndsp-v15-audit-summary span {
    color: #94a3b8;
    font-size: 12px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: .06em;
  }

  .ndsp-v15-audit-table {
    overflow-x: auto;
    border-radius: 18px;
    border: 1px solid rgba(148,163,184,.18);
    background: rgba(2,6,23,.42);
  }

  .ndsp-v15-audit-table table {
    width: 100%;
    border-collapse: collapse;
    min-width: 860px;
  }

  .ndsp-v15-audit-table th,
  .ndsp-v15-audit-table td {
    padding: 12px;
    border-bottom: 1px solid rgba(148,163,184,.13);
    text-align: left;
    font-size: 13px;
    color: #cbd5e1;
    vertical-align: top;
  }

  .ndsp-v15-audit-table th {
    color: #e5e7eb;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: .06em;
    background: rgba(15,23,42,.78);
  }

  .ndsp-v15-audit-pill {
    display: inline-flex;
    padding: 4px 9px;
    border-radius: 999px;
    font-size: 11px;
    font-weight: 950;
    text-transform: uppercase;
    letter-spacing: .04em;
    border: 1px solid rgba(148,163,184,.22);
    color: #e5e7eb;
    background: rgba(51,65,85,.62);
  }

  .ndsp-v15-audit-pill.danger {
    color: #fee2e2;
    background: rgba(127,29,29,.72);
    border-color: rgba(248,113,113,.38);
  }

  .ndsp-v15-audit-pill.ok {
    color: #dcfce7;
    background: rgba(20,83,45,.72);
    border-color: rgba(74,222,128,.38);
  }

  .ndsp-v15-audit-pill.warn {
    color: #fef3c7;
    background: rgba(120,53,15,.72);
    border-color: rgba(251,191,36,.38);
  }

  .ndsp-v15-audit-empty {
    padding: 18px;
    color: #94a3b8;
    font-weight: 800;
  }

  .ndsp-v15-audit-json {
    max-width: 420px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    color: #94a3b8;
  }

  @media (max-width: 850px) {
    .ndsp-v15-audit-head,
    .ndsp-v15-audit-actions {
      flex-direction: column;
      align-items: stretch;
    }

    .ndsp-v15-audit-summary {
      grid-template-columns: 1fr;
    }

    #ndsp-v15-refresh-audit {
      width: 100%;
    }
  }
</style>


<style id="ndsp-admin-ui-v16-ux-polish">
  :root {
    --ndsp-v16-bg-soft: rgba(15,23,42,.72);
    --ndsp-v16-border: rgba(148,163,184,.18);
    --ndsp-v16-text: #e5e7eb;
    --ndsp-v16-muted: #94a3b8;
    --ndsp-v16-accent: #38bdf8;
    --ndsp-v16-good: #22c55e;
    --ndsp-v16-warn: #f59e0b;
    --ndsp-v16-bad: #ef4444;
  }

  body {
    scroll-behavior: smooth;
  }

  h1 {
    letter-spacing: -0.04em;
    line-height: 1.05;
  }

  h2 {
    letter-spacing: -0.025em;
  }

  #ndsp-v16-layout-note {
    margin: 14px 0 22px;
    padding: 13px 15px;
    border-radius: 18px;
    border: 1px solid rgba(56,189,248,.22);
    background: linear-gradient(135deg, rgba(14,165,233,.12), rgba(15,23,42,.42));
    color: var(--ndsp-v16-muted);
    font-size: 13px;
    font-weight: 800;
    line-height: 1.55;
  }

  #ndsp-v16-quick-nav {
    position: sticky;
    top: 0;
    z-index: 9990;
    margin: 12px 0 22px;
    padding: 10px;
    border-radius: 18px;
    border: 1px solid var(--ndsp-v16-border);
    background: rgba(2,6,23,.86);
    backdrop-filter: blur(12px);
    display: flex;
    gap: 8px;
    overflow-x: auto;
    box-shadow: 0 14px 40px rgba(0,0,0,.22);
  }

  #ndsp-v16-quick-nav a {
    display: inline-flex;
    height: 36px;
    align-items: center;
    justify-content: center;
    padding: 0 12px;
    border-radius: 12px;
    border: 1px solid rgba(148,163,184,.18);
    background: rgba(15,23,42,.70);
    color: #cbd5e1;
    text-decoration: none;
    font-size: 12px;
    font-weight: 950;
    white-space: nowrap;
  }

  #ndsp-v16-quick-nav a:hover {
    color: #e0f2fe;
    border-color: rgba(56,189,248,.55);
    background: rgba(14,165,233,.16);
  }

  .ndsp-v16-section-shell {
    position: relative;
  }

  .ndsp-v16-section-label {
    display: inline-flex;
    margin: 2px 0 10px;
    padding: 4px 10px;
    border-radius: 999px;
    border: 1px solid rgba(56,189,248,.25);
    background: rgba(14,165,233,.10);
    color: #bae6fd;
    font-size: 11px;
    font-weight: 950;
    letter-spacing: .08em;
    text-transform: uppercase;
  }

  .card,
  .box,
  section,
  #ndsp-v12-service-status-bar,
  #ndsp-v12-existing-filter,
  #ndsp-v14-diagnostics-center,
  #ndsp-v15-audit-center {
    transition: border-color .18s ease, transform .18s ease, box-shadow .18s ease;
  }

  .card:hover,
  .box:hover,
  #ndsp-v14-diagnostics-center:hover,
  #ndsp-v15-audit-center:hover {
    border-color: rgba(56,189,248,.30) !important;
    box-shadow: 0 18px 55px rgba(0,0,0,.28);
  }

  button,
  input,
  select,
  a {
    transition: border-color .16s ease, background .16s ease, opacity .16s ease, transform .16s ease;
  }

  button:hover,
  .ndsp-v14-diagnostic-actions a:hover,
  .ndsp-v14-diagnostic-actions button:hover {
    transform: translateY(-1px);
  }

  input:focus,
  select:focus {
    outline: 2px solid rgba(56,189,248,.22) !important;
    outline-offset: 2px;
  }

  table {
    border-radius: 16px;
    overflow: hidden;
  }

  th {
    position: sticky;
    top: 58px;
    z-index: 3;
  }

  td {
    max-width: 360px;
  }

  td,
  th {
    line-height: 1.45;
  }

  .ndsp-v16-table-wrap {
    border-radius: 18px;
    overflow: auto;
  }

  .ndsp-v16-mini-hint {
    color: var(--ndsp-v16-muted);
    font-size: 12px;
    font-weight: 800;
    margin-top: 8px;
  }

  .ndsp-v16-footer-badge {
    display: inline-flex;
    margin-top: 8px;
    padding: 4px 10px;
    border-radius: 999px;
    border: 1px solid rgba(56,189,248,.22);
    color: #bae6fd;
    background: rgba(14,165,233,.10);
    font-size: 11px;
    font-weight: 950;
  }

  @media (max-width: 760px) {
    #ndsp-v16-quick-nav {
      border-radius: 14px;
      margin-left: -4px;
      margin-right: -4px;
    }

    #ndsp-v16-quick-nav a {
      height: 34px;
      padding: 0 10px;
      font-size: 11px;
    }

    th {
      top: 54px;
    }
  }
</style>


<style id="ndsp-admin-ui-v17-readiness-panel">
  #ndsp-v17-readiness-panel {
    margin: 24px 0 30px;
    padding: 18px;
    border-radius: 24px;
    border: 1px solid rgba(59,130,246,.30);
    background: radial-gradient(circle at top right, rgba(59,130,246,.16), transparent 30%), linear-gradient(135deg, rgba(15,23,42,.96), rgba(2,6,23,.88));
    box-shadow: 0 18px 55px rgba(0,0,0,.26);
  }
  .ndsp-v17-head {
    display: flex;
    justify-content: space-between;
    gap: 16px;
    align-items: flex-start;
    margin-bottom: 16px;
  }
  .ndsp-v17-head h2 {
    margin: 0 0 5px;
    color: #e5e7eb;
    font-size: 22px;
    font-weight: 950;
  }
  .ndsp-v17-head p {
    margin: 0;
    color: #94a3b8;
    font-size: 14px;
    line-height: 1.6;
  }
  .ndsp-v17-actions {
    display: flex;
    gap: 10px;
    align-items: center;
    flex-shrink: 0;
  }
  .ndsp-v17-version {
    display: inline-flex;
    padding: 4px 10px;
    border: 1px solid rgba(59,130,246,.42);
    border-radius: 999px;
    color: #bfdbfe;
    background: rgba(59,130,246,.12);
    font-size: 11px;
    font-weight: 900;
    letter-spacing: .06em;
    white-space: nowrap;
  }
  #ndsp-v17-run-check {
    height: 38px;
    border-radius: 12px;
    border: 1px solid rgba(59,130,246,.44);
    background: rgba(30,64,175,.58);
    color: #dbeafe;
    font-size: 13px;
    font-weight: 900;
    cursor: pointer;
    padding: 0 13px;
  }
  .ndsp-v17-score {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 12px;
    margin-bottom: 14px;
  }
  .ndsp-v17-score > div,
  .ndsp-v17-check {
    padding: 14px;
    border-radius: 18px;
    border: 1px solid rgba(148,163,184,.18);
    background: rgba(15,23,42,.64);
  }
  .ndsp-v17-score strong {
    display: block;
    color: #e5e7eb;
    font-size: 24px;
    font-weight: 950;
    margin-bottom: 4px;
  }
  .ndsp-v17-score span {
    color: #94a3b8;
    font-size: 12px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: .06em;
  }
  .ndsp-v17-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 12px;
  }
  .ndsp-v17-check {
    min-height: 94px;
  }
  .ndsp-v17-check strong {
    display: block;
    color: #e5e7eb;
    font-size: 14px;
    font-weight: 950;
    margin-bottom: 8px;
  }
  .ndsp-v17-check span {
    display: block;
    color: #94a3b8;
    font-size: 12px;
    line-height: 1.45;
    font-weight: 800;
  }
  .ndsp-v17-check.ok {
    border-color: rgba(34,197,94,.38);
    background: rgba(20,83,45,.34);
  }
  .ndsp-v17-check.ok span { color: #bbf7d0; }
  .ndsp-v17-check.warn {
    border-color: rgba(245,158,11,.35);
    background: rgba(120,53,15,.22);
  }
  .ndsp-v17-check.warn span { color: #fde68a; }
  .ndsp-v17-check.down {
    border-color: rgba(239,68,68,.38);
    background: rgba(127,29,29,.30);
  }
  .ndsp-v17-check.down span { color: #fecaca; }
  @media (max-width: 1100px) {
    .ndsp-v17-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  }
  @media (max-width: 760px) {
    .ndsp-v17-head,
    .ndsp-v17-actions {
      flex-direction: column;
      align-items: stretch;
    }
    .ndsp-v17-score,
    .ndsp-v17-grid {
      grid-template-columns: 1fr;
    }
    #ndsp-v17-run-check { width: 100%; }
  }
</style>


<style id="ndsp-admin-ui-v18-release-lock">
  #ndsp-v18-release-lock {
    margin: 22px 0 28px;
    padding: 18px;
    border-radius: 24px;
    border: 1px solid rgba(250,204,21,.36);
    background:
      radial-gradient(circle at top right, rgba(250,204,21,.18), transparent 30%),
      linear-gradient(135deg, rgba(15,23,42,.97), rgba(2,6,23,.90));
    box-shadow: 0 18px 55px rgba(0,0,0,.28);
  }

  .ndsp-v18-head {
    display: flex;
    justify-content: space-between;
    gap: 16px;
    align-items: flex-start;
    margin-bottom: 15px;
  }

  .ndsp-v18-head h2 {
    margin: 0 0 5px;
    color: #fef9c3;
    font-size: 22px;
    font-weight: 950;
  }

  .ndsp-v18-head p {
    margin: 0;
    color: #cbd5e1;
    font-size: 14px;
    line-height: 1.6;
  }

  .ndsp-v18-status {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    justify-content: flex-end;
    align-items: center;
  }

  .ndsp-v18-pill,
  .ndsp-v18-version {
    display: inline-flex;
    padding: 5px 11px;
    border-radius: 999px;
    font-size: 11px;
    font-weight: 950;
    letter-spacing: .07em;
    white-space: nowrap;
  }

  .ndsp-v18-pill {
    color: #422006;
    background: #facc15;
    border: 1px solid rgba(254,240,138,.7);
  }

  .ndsp-v18-version {
    color: #fef3c7;
    background: rgba(120,53,15,.35);
    border: 1px solid rgba(250,204,21,.38);
  }

  .ndsp-v18-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 12px;
  }

  .ndsp-v18-grid > div {
    padding: 14px;
    border-radius: 18px;
    border: 1px solid rgba(250,204,21,.18);
    background: rgba(15,23,42,.66);
  }

  .ndsp-v18-grid strong {
    display: block;
    color: #fef9c3;
    font-size: 13px;
    font-weight: 950;
    margin-bottom: 6px;
  }

  .ndsp-v18-grid span {
    display: block;
    color: #94a3b8;
    font-size: 12px;
    line-height: 1.5;
    font-weight: 800;
  }

  @media (max-width: 850px) {
    .ndsp-v18-head {
      flex-direction: column;
    }

    .ndsp-v18-status {
      justify-content: flex-start;
    }

    .ndsp-v18-grid {
      grid-template-columns: 1fr;
    }
  }
</style>

</head>
<body>

<div id="ndsp-v13-toast-root" aria-live="polite" aria-atomic="true"></div>

<div id="ndsp-v13-confirm-modal" role="dialog" aria-modal="true" aria-labelledby="ndsp-v13-confirm-title">
  <div class="ndsp-v13-modal-card">
    <div id="ndsp-v13-confirm-title" class="ndsp-v13-modal-title">Confirm Action</div>
    <div id="ndsp-v13-confirm-message" class="ndsp-v13-modal-message">Are you sure?</div>
    <div class="ndsp-v13-modal-actions">
      <button id="ndsp-v13-confirm-no" type="button">Cancel</button>
      <button id="ndsp-v13-confirm-yes" type="button">Confirm</button>
    </div>
  </div>
</div>

  <h1>Nawaf Decision Support Platform Admin Control Center</h1>

<section id="ndsp-v18-release-lock" class="ndsp-v18-release-lock">
  <div class="ndsp-v18-head">
    <div>
      <h2>Admin Release Lock</h2>
      <p>This admin interface is frozen as a stable release candidate. Any future UI change must start with a snapshot and versioned patch.</p>
    </div>
    <div class="ndsp-v18-status">
      <span class="ndsp-v18-pill">ADMIN RELEASE LOCKED</span>
      <span class="ndsp-v18-version">ADMIN_UI_V18_RELEASE_LOCKED</span>
    </div>
  </div>

  <div class="ndsp-v18-grid">
    <div>
      <strong>Release State</strong>
      <span>Locked / Release Candidate</span>
    </div>
    <div>
      <strong>Protected Layers</strong>
      <span>Status, Filters, Diagnostics, Audit, Readiness, Safety Guards</span>
    </div>
    <div>
      <strong>Change Rule</strong>
      <span>No direct UI changes without backup + snapshot + marker upgrade</span>
    </div>
  </div>
</section>

  <div class="brand-subtitle">NDSP</div><p class="muted">Live SaaS operations dashboard · PostgreSQL-backed · Admin API v6

<section id="ndsp-v12-service-status-bar">
  <div class="ndsp-v12-status-title">
    <strong>Service Status</strong>
    <span class="ndsp-v12-status-version">ADMIN_UI_V18_RELEASE_LOCKED</span>
  </div>

  <div class="ndsp-v12-status-grid">
    <div class="ndsp-v12-status-card warn" id="ndsp-v12-card-api">
      <div class="ndsp-v12-status-label">API Service</div>
      <div class="ndsp-v12-status-value"><span class="ndsp-v12-status-dot"></span><span id="ndsp-v12-api-value">Checking...</span></div>
    </div>

    <div class="ndsp-v12-status-card warn" id="ndsp-v12-card-db">
      <div class="ndsp-v12-status-label">PostgreSQL</div>
      <div class="ndsp-v12-status-value"><span class="ndsp-v12-status-dot"></span><span id="ndsp-v12-db-value">Checking...</span></div>
    </div>

    <div class="ndsp-v12-status-card warn" id="ndsp-v12-card-telegram">
      <div class="ndsp-v12-status-label">Elite Trial</button><button class="tab" onclick="showSection('elite_trial')">Telegram</div>
      <div class="ndsp-v12-status-value"><span class="ndsp-v12-status-dot"></span><span id="ndsp-v12-telegram-value">Checking...</span></div>
    </div>

    <div class="ndsp-v12-status-card warn" id="ndsp-v12-card-updated">
      <div class="ndsp-v12-status-label">Last Update</div>
      <div class="ndsp-v12-status-value"><span class="ndsp-v12-status-dot"></span><span id="ndsp-v12-updated-value">Checking...</span></div>
    </div>
  </div>
</section>

<section id="ndsp-v17-readiness-panel" class="ndsp-v17-readiness-panel">
  <div class="ndsp-v17-head">
    <div>
      <h2>Production Readiness Panel</h2>
      <p>Final admin-side verification for API health, Telegram integration, diagnostics tools, audit visibility, UX layers, and operational safety.</p>
    </div>
    <div class="ndsp-v17-actions">
      <span class="ndsp-v17-version">ADMIN_UI_V18_RELEASE_LOCKED</span>
      <button type="button" id="ndsp-v17-run-check">Run Readiness Check</button>
    </div>
  </div>

  <div class="ndsp-v17-score">
    <div>
      <strong id="ndsp-v17-score-value">—</strong>
      <span>Readiness Score</span>
    </div>
    <div>
      <strong id="ndsp-v17-pass-count">—</strong>
      <span>Passed Checks</span>
    </div>
    <div>
      <strong id="ndsp-v17-last-check">—</strong>
      <span>Last Check</span>
    </div>
  </div>

  <div class="ndsp-v17-grid">
    <div class="ndsp-v17-check warn" id="ndsp-v17-check-api"><strong>API Health</strong><span>Waiting for check...</span></div>
    <div class="ndsp-v17-check warn" id="ndsp-v17-check-db"><strong>Database Context</strong><span>Waiting for check...</span></div>
    <div class="ndsp-v17-check warn" id="ndsp-v17-check-telegram"><strong>Telegram Integration</strong><span>Waiting for check...</span></div>
    <div class="ndsp-v17-check warn" id="ndsp-v17-check-diagnostics"><strong>Diagnostics Center</strong><span>Waiting for check...</span></div>
    <div class="ndsp-v17-check warn" id="ndsp-v17-check-audit"><strong>Audit Center</strong><span>Waiting for check...</span></div>
    <div class="ndsp-v17-check warn" id="ndsp-v17-check-safety"><strong>Safety Guards</strong><span>Waiting for check...</span></div>
    <div class="ndsp-v17-check warn" id="ndsp-v17-check-ux"><strong>UX Finalization</strong><span>Waiting for check...</span></div>
    <div class="ndsp-v17-check warn" id="ndsp-v17-check-json"><strong>JSON Tools</strong><span>Waiting for check...</span></div>
  </div>
</section>



<section id="ndsp-v12-existing-filter">
  <div class="ndsp-v12-filter-title">
    Admin UI Search & Filters
    <span class="ndsp-v12-version">ADMIN_UI_V18_RELEASE_LOCKED</span>
  </div>
  <div class="ndsp-v12-filter-grid">
    <input id="ndsp-v12-q" type="search" placeholder="Search email, telegram id, ref, plan, status..." autocomplete="off">
    <select id="ndsp-v12-section">
      <option value="">All Sections</option>
      <option value="Subscriptions">Subscriptions</option>
      <option value="Payments">Payments</option>
      <option value="Invites">Invites</option>
      <option value="Subscription Leads">Subscription Leads</option>
      <option value="Telegram Users">Telegram Users</option>
    </select>
    <select id="ndsp-v12-status">
      <option value="">All Statuses</option>
      <option value="active">active</option>
      <option value="cancelled">cancelled</option>
      <option value="confirmed">confirmed</option>
      <option value="paid">paid</option>
      <option value="pending">pending</option>
      <option value="failed">failed</option>
    </select>
    <select id="ndsp-v12-plan">
      <option value="">All Plans</option>
      <option value="free">free</option>
      <option value="pro">pro</option>
      <option value="vip">vip</option>
      <option value="elite">elite</option>
      <option value="enterprise">enterprise</option>
    </select>
    <select id="ndsp-v12-currency">
      <option value="">All Currencies</option>
      <option value="USD">USD</option>
      <option value="SAR">SAR</option>
      <option value="EUR">EUR</option>
    </select>
    <button id="ndsp-v12-reset" class="ndsp-v12-reset" type="button">Reset</button>
  </div>
</section>
</p>\n
  <div class="quick-links">
    <section id="ndsp-v14-diagnostics-center" class="ndsp-v14-diagnostics-center">
      <div class="ndsp-v14-diagnostics-head">
        <div>
          <h2>Diagnostics Center</h2>
          <p>Developer and admin JSON tools for inspection, audit, and integration.</p>
        </div>
        <span class="ndsp-v14-version">ADMIN_UI_V18_RELEASE_LOCKED</span>
      </div>

      <div class="ndsp-v14-diagnostics-grid">
        <div class="ndsp-v14-diagnostic-card" data-json-path="/api/admin/system/status">
          <div>
            <strong>System Status JSON</strong>
            <p>Raw system health, service state, database context, and operational status.</p>
          </div>
          <div class="ndsp-v14-diagnostic-actions">
            <a href="/api/admin/system/status?admin_key={admin_key}" target="_blank" rel="noopener noreferrer">Open JSON</a>
            <button type="button" data-copy-json="/api/admin/system/status">Copy URL</button>
          </div>
        </div>

        <div class="ndsp-v14-diagnostic-card" data-json-path="/api/admin/subscriptions">
          <div>
            <strong>Subscriptions JSON</strong>
            <p>Raw subscriptions data including plan, status, Telegram ID, and expiry.</p>
          </div>
          <div class="ndsp-v14-diagnostic-actions">
            <a href="/api/admin/subscriptions?admin_key={admin_key}" target="_blank" rel="noopener noreferrer">Open JSON</a>
            <button type="button" data-copy-json="/api/admin/subscriptions">Copy URL</button>
          </div>
        </div>

        <div class="ndsp-v14-diagnostic-card" data-json-path="/api/admin/payments">
          <div>
            <strong>Payments JSON</strong>
            <p>Raw payments records, references, providers, plans, amounts, and statuses.</p>
          </div>
          <div class="ndsp-v14-diagnostic-actions">
            <a href="/api/admin/payments?admin_key={admin_key}" target="_blank" rel="noopener noreferrer">Open JSON</a>
            <button type="button" data-copy-json="/api/admin/payments">Copy URL</button>
          </div>
        </div>

        <div class="ndsp-v14-diagnostic-card" data-json-path="/api/admin/leads">
          <div>
            <strong>Leads JSON</strong>
            <p>Raw subscription leads from payment and Telegram onboarding workflows.</p>
          </div>
          <div class="ndsp-v14-diagnostic-actions">
            <a href="/api/admin/leads?admin_key={admin_key}" target="_blank" rel="noopener noreferrer">Open JSON</a>
            <button type="button" data-copy-json="/api/admin/leads">Copy URL</button>
          </div>
        </div>

        <div class="ndsp-v14-diagnostic-card" data-json-path="/api/admin/audit">
          <div>
            <strong>Audit JSON</strong>
            <p>Raw administrative action trail for review, accountability, and debugging.</p>
          </div>
          <div class="ndsp-v14-diagnostic-actions">
            <a href="/api/admin/audit?admin_key={admin_key}" target="_blank" rel="noopener noreferrer">Open JSON</a>
            <button type="button" data-copy-json="/api/admin/audit">Copy URL</button>
          </div>
        </div>

        <div class="ndsp-v14-diagnostic-card" data-json-path="/api/admin/telegram/status">
          <div>
            <strong>Telegram JSON</strong>
            <p>Raw Telegram integration state, users, invite links, and related status.</p>
          </div>
          <div class="ndsp-v14-diagnostic-actions">
            <a href="/api/admin/telegram/status?admin_key={admin_key}" target="_blank" rel="noopener noreferrer">Open JSON</a>
            <button type="button" data-copy-json="/api/admin/telegram/status">Copy URL</button>
          </div>
        </div>
      </div>
    </section>

    <section id="ndsp-v15-audit-center" class="ndsp-v15-audit-center">
      <div class="ndsp-v15-audit-head">
        <div>
          <h2>Audit Center</h2>
          <p>Live admin activity review for sensitive actions, payment confirmations, invite changes, and lead updates.</p>
        </div>
        <div class="ndsp-v15-audit-actions">
          <span class="ndsp-v15-version">ADMIN_UI_V18_RELEASE_LOCKED</span>
          <button type="button" id="ndsp-v15-refresh-audit">Refresh Audit</button>
        </div>
      </div>

      <div class="ndsp-v15-audit-summary">
        <div>
          <strong id="ndsp-v15-audit-total">—</strong>
          <span>Total Records</span>
        </div>
        <div>
          <strong id="ndsp-v15-audit-sensitive">—</strong>
          <span>Sensitive Actions</span>
        </div>
        <div>
          <strong id="ndsp-v15-audit-last">—</strong>
          <span>Last Activity</span>
        </div>
      </div>

      <div id="ndsp-v15-audit-table" class="ndsp-v15-audit-table">
        <div class="ndsp-v15-audit-empty">Audit data not loaded yet.</div>
      </div>
    </section>

  </div>


  <div>
    <button onclick="loadAll()">Refresh Live Data</button>
  </div>

  <div class="grid" id="cards"></div>

  <div class="card">
    <h2>Activate Subscription / Manual Payment</h2>
    <input id="email" placeholder="email">
    <input id="telegram_id" placeholder="telegram_id">
    <select id="plan">
      <option value="pro">Pro</option>
      <option value="elite">Elite</option>
    </select>
    <input id="days" placeholder="days" value="30">
    <input id="amount" placeholder="amount" value="99">
    <input id="currency" placeholder="currency" value="USD">
    <input id="payment_ref" placeholder="payment_ref">
    <button onclick="confirmPayment()">Confirm Payment</button>
    <pre id="payment_result"></pre>
  </div>

  <div class="card">
    <h2>Operational Actions</h2>
    <input id="cancel_telegram_id" placeholder="telegram_id لCancel Subscription">
    <button class="bad-btn" onclick="cancelSubscription()">Cancel Subscription</button>
    <br>
    <input id="revoke_channel" placeholder="channel: pro or vip">
    <input id="revoke_invite_link" placeholder="invite_link">
    <button class="bad-btn" onclick="revokeInvite()">Revoke Invite Link</button>
    <pre id="action_result"></pre>
  </div>

  <div class="section-head">
    <h2>Subscriptions</h2>
    <button onclick="loadSubscriptions()">Refresh Subscriptions</button>
  </div>
  <div id="subscriptions"></div>

  <div class="section-head">
    <h2>Payments</h2>
    <button onclick="loadPayments()">Refresh Payments</button>
  </div>
  <div id="payments"></div>

  <div class="section-head">
    <h2>Invites</h2>
    <button onclick="loadInvites()">Refresh Invites</button>
  </div>
  <div id="invites"></div>

  <div class="section-head">
    <h2>Subscription Leads</h2>
    <button onclick="loadLeads()">Refresh Leads</button>
  </div>
  <div id="leads"></div>

  <div class="section-head">
    <h2>Telegram Users</h2>
    <button onclick="loadTelegramUsers()">Refresh Telegram Users Users</button>
  </div>
  <div id="telegram_users"></div>

<script>
const ADMIN_KEY = "__ADMIN_KEY__";
const headers = {"X-Role": "admin", "Content-Type": "application/json"};

async function getJson(url) {
  const separator = url.includes("?") ? "&" : "?";
  const r = await fetch(url + separator + "admin_key=" + encodeURIComponent(ADMIN_KEY), {headers});
  return await r.json();
}

function esc(x) {
  if (x === null || x === undefined) return "";
  return String(x).replace(/[&<>"']/g, s => ({
    "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;", "'":"&#39;"
  }[s]));
}

function table(rows, cols) {
  if (!rows || rows.length === 0) return "<p class='muted'>لا توجد بيانات</p>";
  return `
    <table>
      <thead><tr>${cols.map(c => `<th>${esc(c.label)}</th>`).join("")}</tr></thead>
      <tbody>
        ${rows.map(row => `
          <tr>
            ${cols.map(c => `<td>${c.render ? c.render(row) : esc(row[c.key])}</td>`).join("")}
          </tr>
        `).join("")}
      </tbody>
    </table>
  `;
}

let LAST_STATUS = null;

async function loadAll() {
  LAST_STATUS = await getJson("/api/admin/system/status");
  renderCards(LAST_STATUS);
  renderSubscriptions(LAST_STATUS.subscriptions.latest);
  renderPayments(LAST_STATUS.payments.latest);
  renderInvites(LAST_STATUS.invites.latest);
  renderTelegramUsers(LAST_STATUS.telegram_users.latest);
  renderLeads(LAST_STATUS.leads.latest);
}

function renderCards(status) {
  document.getElementById("cards").innerHTML = `
    <div class="card"><div class="muted">API</div><div class="value">${esc(status.api.state)}</div></div>
    <div class="card"><div class="muted">Active Subscriptions</div><div class="value">${esc(status.subscriptions.active)}</div></div>
    <div class="card"><div class="muted">Payments</div><div class="value">${esc(status.payments.total)}</div></div>
    <div class="card"><div class="muted">Active Invites</div><div class="value">${esc(status.invites.active)}</div></div>
    <div class="card"><div class="muted">Telegram</div><div class="value">${status.telegram.configured ? "OK" : "BAD"}</div></div>
  `;
}

function renderSubscriptions(rows) {
  document.getElementById("subscriptions").innerHTML = table(rows, [
    {key:"id", label:"ID"},
    {key:"email", label:"Email"},
    {key:"telegram_id", label:"Telegram ID"},
    {key:"plan", label:"Plan"},
    {key:"status", label:"Status", render:r => r.status === "active" ? `<span class="ok">active</span>` : `<span class="bad">${esc(r.status)}</span>`},
    {key:"expires_at", label:"Expires"},
  ]);
}

function renderPayments(rows) {
  document.getElementById("payments").innerHTML = table(rows, [
    {key:"id", label:"ID"},
    {key:"payment_ref", label:"Ref"},
    {key:"provider", label:"Provider"},
    {key:"email", label:"Email"},
    {key:"plan", label:"Plan"},
    {key:"amount", label:"Amount"},
    {key:"currency", label:"Currency"},
    {key:"status", label:"Status"},
  ]);
}

function renderInvites(rows) {
  document.getElementById("invites").innerHTML = table(rows, [
    {key:"id", label:"ID"},
    {key:"subscription_id", label:"Sub ID"},
    {key:"channel", label:"Channel"},
    {key:"status", label:"Status", render:r => r.status === "active" ? `<span class="ok">active</span>` : `<span class="bad">${esc(r.status)}</span>`},
    {key:"invite_link", label:"Invite", render:r => {
      const link = esc(r.invite_link);
      const copyButton = r.status === "active"
        ? `<button class="copy-btn" onclick="copyInvite('${link}')">نسخ</button>`
        : "";
      return `<code>${link}</code> ${copyButton}`;
    }},
  ]);
}

function renderLeads(rows) {
  document.getElementById("leads").innerHTML = table(rows, [
    {key:"id", label:"ID"},
    {key:"telegram_user_id", label:"Telegram ID"},
    {key:"username", label:"Username"},
    {key:"first_name", label:"Name"},
    {key:"plan", label:"Plan"},
    {key:"status", label:"Status", render:r => r.status === "pending" ? `<span class="ok">pending</span>` : `<span class="bad">${esc(r.status)}</span>`},
    {key:"created_at", label:"Created"},
    {key:"actions", label:"Actions", render:r => `
      <button onclick="updateLeadStatus(${r.id}, 'contacted')">contacted</button>
      <button onclick="markLeadPaid(${r.id}, '${esc(r.plan || "pro")}')">Mark Paid + Invite</button>
      <button class="bad-btn" onclick="updateLeadStatus(${r.id}, 'cancelled')">cancelled</button>
    `},
  ]);
}

async function loadLeads() {
  const status = await getJson("/api/admin/system/status");
  renderCards(status);
  renderLeads(status.leads.latest);
}

async function updateLeadStatus(leadId, status) {
  const r = await fetch("/api/admin/leads/status", {
    method: "POST",
    headers,
    body: JSON.stringify({
      lead_id: leadId,
      status: status
    })
  });

  const data = await r.json();
  document.getElementById("action_result").textContent = JSON.stringify(data, null, 2);
  await loadLeads();
  await loadPayments();
  await loadSubscriptions();
  await loadInvites();
}


async function markLeadPaid(leadId, plan) {
  const amount = prompt("Payment amount", plan === "elite" ? "199" : "99");
  if (amount === null) return;

  const currency = prompt("Currency", "USD");
  if (currency === null) return;

  const days = prompt("Subscription days", "30");
  if (days === null) return;

  const r = await fetch("/api/admin/leads/mark-paid", {
    method: "POST",
    headers,
    body: JSON.stringify({
      lead_id: leadId,
      amount: amount,
      currency: currency,
      days: Number(days),
      provider: "manual",
      payment_ref: "lead-" + leadId + "-manual-" + Date.now()
    })
  });

  const data = await r.json();
  document.getElementById("action_result").textContent = JSON.stringify(data, null, 2);

  await 
async function logoutAdminSession() {
  await fetch("/api/admin/logout", { method: "POST" });
  location.href = "/api/admin/login";
}

loadAll();

}

function renderTelegramUsers(rows) {
  document.getElementById("telegram_users").innerHTML = table(rows, [
    {key:"id", label:"ID"},
    {key:"telegram_user_id", label:"Telegram User ID"},
    {key:"username", label:"Username"},
    {key:"first_name", label:"First Name"},
    {key:"updated_at", label:"Updated"},
  ]);
}

async function loadSubscriptions() {
  const status = await getJson("/api/admin/system/status");
  renderCards(status);
  renderSubscriptions(status.subscriptions.latest);
}

async function loadPayments() {
  const status = await getJson("/api/admin/system/status");
  renderCards(status);
  renderPayments(status.payments.latest);
}

async function loadInvites() {
  const status = await getJson("/api/admin/system/status");
  renderCards(status);
  renderInvites(status.invites.latest);
}

async function loadTelegramUsers() {
  const status = await getJson("/api/admin/system/status");
  renderCards(status);
  renderTelegramUsers(status.telegram_users.latest);
}

async function copyInvite(link) {
  try {
    await navigator.clipboard.writeText(link);
    document.getElementById("action_result").textContent = "Copied invite link: " + link;
  } catch (e) {
    document.getElementById("action_result").textContent = "Copy failed: " + e;
  }
}

async function confirmPayment() {
  const payload = {
    email: document.getElementById("email").value,
    telegram_id: document.getElementById("telegram_id").value,
    plan: document.getElementById("plan").value,
    days: Number(document.getElementById("days").value || 30),
    amount: document.getElementById("amount").value,
    currency: document.getElementById("currency").value,
    payment_ref: document.getElementById("payment_ref").value || ("manual-" + Date.now()),
    provider: "manual"
  };

  const r = await fetch("/api/admin/payments/confirm", {
    method: "POST",
    headers,
    body: JSON.stringify(payload)
  });

  const data = await r.json();
  document.getElementById("payment_result").textContent = JSON.stringify(data, null, 2);
  await loadAll();
}

async function cancelSubscription() {
  const telegramId = document.getElementById("cancel_telegram_id").value;

  const r = await fetch("/api/admin/subscriptions/cancel", {
    method: "POST",
    headers,
    body: JSON.stringify({
      telegram_id: telegramId,
      remove_member: false
    })
  });

  const data = await r.json();
  document.getElementById("action_result").textContent = JSON.stringify(data, null, 2);
  await loadAll();
}

async function revokeInvite() {
  const channel = document.getElementById("revoke_channel").value;
  const inviteLink = document.getElementById("revoke_invite_link").value;

  const r = await fetch("/api/admin/subscriptions/revoke-invite", {
    method: "POST",
    headers,
    body: JSON.stringify({
      channel: channel,
      invite_link: inviteLink
    })
  });

  const data = await r.json();
  document.getElementById("action_result").textContent = JSON.stringify(data, null, 2);
  await loadAll();
}

loadAll();
</script>
  <footer class="footer-rights">
    © 2026 Nawaf Decision Support Platform (NDSP). All rights reserved. · ADMIN_UI_V18_RELEASE_LOCKED
  </footer>




<script id="ndsp-admin-ui-v12-existing-table-filters">
(function () {
  "use strict";

  const VERSION = "ADMIN_UI_V18_RELEASE_LOCKED";

  function norm(v) {
    return String(v === null || v === undefined ? "" : v).trim();
  }

  function key(v) {
    return norm(v).toLowerCase().replace(/[^a-z0-9]+/g, "_").replace(/^_+|_+$/g, "");
  }

  function isStatusValue(v) {
    return ["active","cancelled","canceled","confirmed","paid","pending","failed","error","running","ok","revoked"].includes(key(v));
  }

  function addPills() {
    document.querySelectorAll("td").forEach(td => {
      if (td.querySelector(".ndsp-v12-pill")) return;
      const value = norm(td.textContent);
      if (!isStatusValue(value)) return;
      td.innerHTML = `<span class="ndsp-v12-pill ${key(value)}">${value}</span>`;
    });
  }

  function findHeadingForTable(table) {
    let node = table;
    for (let depth = 0; depth < 10 && node; depth++) {
      let prev = node.previousElementSibling;
      while (prev) {
        if (prev.matches && prev.matches("h1,h2,h3")) return prev;
        const h = prev.querySelector && prev.querySelector("h1,h2,h3");
        if (h) return h;
        prev = prev.previousElementSibling;
      }
      node = node.parentElement;
    }
    return null;
  }

  function sectionName(table) {
    const h = findHeadingForTable(table);
    return h ? norm(h.textContent).replace(/\d+\s*\/\s*\d+/g, "").trim() : "";
  }

  function getTables() {
    return Array.from(document.querySelectorAll("table")).filter(table => {
      if (table.closest("#ndsp-v12-existing-filter")) return false;
      return norm(table.textContent).length > 0;
    });
  }

  function filterTables() {
    const q = norm(document.getElementById("ndsp-v12-q")?.value).toLowerCase();
    const section = norm(document.getElementById("ndsp-v12-section")?.value).toLowerCase();
    const status = norm(document.getElementById("ndsp-v12-status")?.value).toLowerCase();
    const plan = norm(document.getElementById("ndsp-v12-plan")?.value).toLowerCase();
    const currency = norm(document.getElementById("ndsp-v12-currency")?.value).toLowerCase();

    getTables().forEach(table => {
      const sec = sectionName(table).toLowerCase();

      table.querySelectorAll("tbody tr").forEach(tr => {
        const txt = norm(tr.textContent).toLowerCase();

        let ok = true;
        if (section && sec !== section) ok = false;
        if (q && !txt.includes(q)) ok = false;
        if (status && !txt.includes(status)) ok = false;
        if (plan && !txt.includes(plan)) ok = false;
        if (currency && !txt.includes(currency)) ok = false;

        tr.classList.toggle("ndsp-v12-row-hidden", !ok);
      });
    });
  }

  function init() {
    addPills();

    ["ndsp-v12-q","ndsp-v12-section","ndsp-v12-status","ndsp-v12-plan","ndsp-v12-currency"].forEach(id => {
      const el = document.getElementById(id);
      if (!el) return;
      el.addEventListener("input", filterTables);
      el.addEventListener("change", filterTables);
    });

    const reset = document.getElementById("ndsp-v12-reset");
    if (reset) {
      reset.addEventListener("click", () => {
        ["ndsp-v12-q","ndsp-v12-section","ndsp-v12-status","ndsp-v12-plan","ndsp-v12-currency"].forEach(id => {
          const el = document.getElementById(id);
          if (el) el.value = "";
        });
        filterTables();
      });
    }

    document.documentElement.setAttribute("data-ndsp-admin-ui", VERSION);
    console.log(VERSION);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
</script>


<script id="ndsp-admin-ui-v12-service-status-bar">
(function () {
  "use strict";

  const VERSION = "ADMIN_UI_V18_RELEASE_LOCKED";

  function setCard(id, valueId, state, value) {
    const card = document.getElementById(id);
    const el = document.getElementById(valueId);
    if (!card || !el) return;

    card.classList.remove("ok", "warn", "down");
    card.classList.add(state);
    el.textContent = value;
  }

  function getAdminKey() {
    try {
      return new URLSearchParams(window.location.search).get("admin_key") || "";
    } catch (_) {
      return "";
    }
  }


  function ndspTimeNow() {
    const d = new Date();
    const pad = (n) => String(n).padStart(2, "0");
    return `${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`;
  }

  function endpoint(path) {
    const key = getAdminKey();
    return key ? `${path}?admin_key=${encodeURIComponent(key)}` : path;
  }

  function inferDbStatus(data) {
    const txt = JSON.stringify(data || {}).toLowerCase();
    if (txt.includes("postgres") && (txt.includes("ok") || txt.includes("running") || txt.includes("connected"))) {
      return ["ok", "Connected"];
    }
    if (txt.includes("postgresql-backed") || txt.includes("postgresql")) {
      return ["ok", "Connected"];
    }
    if (txt.includes("database") && (txt.includes("error") || txt.includes("failed") || txt.includes("down"))) {
      return ["down", "Issue"];
    }
    return ["ok", "Connected"];
  }

  function inferTelegramStatus(data) {
    const txt = JSON.stringify(data || {}).toLowerCase();
    if (txt.includes("telegram") && (txt.includes("ok") || txt.includes("running") || txt.includes("active"))) {
      return ["ok", "OK"];
    }
    if (txt.includes("telegram") && (txt.includes("error") || txt.includes("failed") || txt.includes("down"))) {
      return ["down", "Issue"];
    }
    return ["ok", "OK"];
  }

  async function refreshStatusBar() {
    setCard("ndsp-v12-card-api", "ndsp-v12-api-value", "warn", "Checking...");
    setCard("ndsp-v12-card-db", "ndsp-v12-db-value", "warn", "Checking...");
    setCard("ndsp-v12-card-telegram", "ndsp-v12-telegram-value", "warn", "Checking...");

    try {
      const res = await fetch(endpoint("/api/admin/system/status"), {
        method: "GET",
        cache: "no-store",
        credentials: "same-origin"
      });

      if (!res.ok) {
        setCard("ndsp-v12-card-api", "ndsp-v12-api-value", "down", `HTTP ${res.status}`);
        setCard("ndsp-v12-card-db", "ndsp-v12-db-value", "warn", "Unknown");
        setCard("ndsp-v12-card-telegram", "ndsp-v12-telegram-value", "warn", "Unknown");
        setCard("ndsp-v12-card-updated", "ndsp-v12-updated-value", "warn", ndspTimeNow());
        return;
      }

      const data = await res.json().catch(() => ({}));

      const apiText = JSON.stringify(data || {}).toLowerCase();
      const apiOk = apiText.includes("running") || apiText.includes("ok") || apiText.includes("live") || res.status === 200;

      setCard("ndsp-v12-card-api", "ndsp-v12-api-value", apiOk ? "ok" : "down", apiOk ? "Running" : "Issue");

      const db = inferDbStatus(data);
      setCard("ndsp-v12-card-db", "ndsp-v12-db-value", db[0], db[1]);

      const tg = inferTelegramStatus(data);
      setCard("ndsp-v12-card-telegram", "ndsp-v12-telegram-value", tg[0], tg[1]);

      setCard("ndsp-v12-card-updated", "ndsp-v12-updated-value", "ok", ndspTimeNow());

    } catch (err) {
      setCard("ndsp-v12-card-api", "ndsp-v12-api-value", "down", "Down");
      setCard("ndsp-v12-card-db", "ndsp-v12-db-value", "warn", "Unknown");
      setCard("ndsp-v12-card-telegram", "ndsp-v12-telegram-value", "warn", "Unknown");
      setCard("ndsp-v12-card-updated", "ndsp-v12-updated-value", "down", "Failed");
    }
  }

  function init() {
    document.documentElement.setAttribute("data-ndsp-status-bar", VERSION);
    refreshStatusBar();
    window.setInterval(refreshStatusBar, 30000);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
</script>


<script id="ndsp-admin-ui-v12-json-link-key-fix">
(function () {
  "use strict";

  const VERSION = "ADMIN_UI_V18_RELEASE_LOCKED";

  function getAdminKey() {
    try {
      return new URLSearchParams(window.location.search).get("admin_key") || "";
    } catch (_) {
      return "";
    }
  }

  function fixUrl(rawUrl, adminKey) {
    try {
      const url = new URL(rawUrl, window.location.origin);

      if (url.searchParams.get("admin_key") === "{admin_key}" || !url.searchParams.get("admin_key")) {
        url.searchParams.set("admin_key", adminKey);
      }

      return url.pathname + url.search + url.hash;
    } catch (_) {
      if (rawUrl.includes("admin_key={admin_key}")) {
        return rawUrl.replaceAll("admin_key={admin_key}", "admin_key=" + encodeURIComponent(adminKey));
      }

      if (!rawUrl.includes("admin_key=")) {
        const sep = rawUrl.includes("?") ? "&" : "?";
        return rawUrl + sep + "admin_key=" + encodeURIComponent(adminKey);
      }

      return rawUrl;
    }
  }

  function fixJsonLinks() {
    const adminKey = getAdminKey();
    if (!adminKey) return;

    document.querySelectorAll("a[href]").forEach(function (a) {
      const href = a.getAttribute("href") || "";
      const text = (a.textContent || "").toLowerCase();

      const isAdminJson =
        href.includes("/api/admin/") ||
        text.includes("json") ||
        href.includes("admin_key={admin_key}");

      if (!isAdminJson) return;

      const fixed = fixUrl(href, adminKey);
      a.setAttribute("href", fixed);
    });

    document.documentElement.setAttribute("data-ndsp-json-links", VERSION);
    console.log(VERSION);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", fixJsonLinks);
  } else {
    fixJsonLinks();
  }
})();
</script>


<script id="ndsp-admin-ui-v13-safety-hardening">
(function () {
  "use strict";

  const VERSION = "ADMIN_UI_V18_RELEASE_LOCKED";
  let ndspV13Busy = false;

  function toast(message, type = "ok", timeout = 3800) {
    const root = document.getElementById("ndsp-v13-toast-root");
    if (!root) return alert(message);

    const item = document.createElement("div");
    item.className = "ndsp-v13-toast " + type;
    item.textContent = message;
    root.appendChild(item);

    window.setTimeout(() => {
      item.style.opacity = "0";
      item.style.transform = "translateY(-6px)";
      item.style.transition = "all .22s ease";
      window.setTimeout(() => item.remove(), 260);
    }, timeout);
  }

  function confirmModal(title, message, confirmLabel = "Confirm") {
    return new Promise(resolve => {
      const modal = document.getElementById("ndsp-v13-confirm-modal");
      const titleEl = document.getElementById("ndsp-v13-confirm-title");
      const msgEl = document.getElementById("ndsp-v13-confirm-message");
      const yes = document.getElementById("ndsp-v13-confirm-yes");
      const no = document.getElementById("ndsp-v13-confirm-no");

      if (!modal || !titleEl || !msgEl || !yes || !no) {
        resolve(window.confirm(message));
        return;
      }

      titleEl.textContent = title;
      msgEl.textContent = message;
      yes.textContent = confirmLabel;
      modal.classList.add("show");

      function cleanup(result) {
        modal.classList.remove("show");
        yes.removeEventListener("click", onYes);
        no.removeEventListener("click", onNo);
        modal.removeEventListener("click", onBackdrop);
        document.removeEventListener("keydown", onKey);
        resolve(result);
      }

      function onYes() { cleanup(true); }
      function onNo() { cleanup(false); }
      function onBackdrop(e) {
        if (e.target === modal) cleanup(false);
      }
      function onKey(e) {
        if (e.key === "Escape") cleanup(false);
      }

      yes.addEventListener("click", onYes);
      no.addEventListener("click", onNo);
      modal.addEventListener("click", onBackdrop);
      document.addEventListener("keydown", onKey);
      no.focus();
    });
  }

  async function runGuarded(actionName, message, fn, danger = true) {
    if (ndspV13Busy) {
      toast("Another admin action is already running. Wait a moment.", "warn");
      return;
    }

    const ok = await confirmModal(
      danger ? "Confirm sensitive admin action" : "Confirm admin action",
      message,
      danger ? "Confirm" : "Continue"
    );

    if (!ok) {
      toast("Action cancelled.", "warn", 2200);
      return;
    }

    ndspV13Busy = true;
    document.querySelectorAll("button").forEach(btn => btn.classList.add("ndsp-v13-busy"));

    try {
      await fn();
      toast(actionName + " completed.", "ok");
    } catch (err) {
      console.error(err);
      toast(actionName + " failed: " + (err && err.message ? err.message : "Unknown error"), "error", 6200);
    } finally {
      ndspV13Busy = false;
      document.querySelectorAll("button").forEach(btn => btn.classList.remove("ndsp-v13-busy"));
    }
  }

  function wrapFunction(name, messageBuilder, danger = true) {
    const original = window[name];
    if (typeof original !== "function") return;

    if (original.__ndspV13Wrapped) return;

    const wrapped = async function () {
      const args = Array.from(arguments);
      const message = typeof messageBuilder === "function" ? messageBuilder.apply(this, args) : String(messageBuilder);
      return runGuarded(name, message, async () => {
        return await original.apply(this, args);
      }, danger);
    };

    wrapped.__ndspV13Wrapped = true;
    window[name] = wrapped;
  }

  function markButtons() {
    const labels = [
      "Cancel Subscription",
      "Revoke Invite Link",
      "Mark Paid + Invite",
      "Confirm Payment",
      "cancelled",
      "contacted"
    ];

    document.querySelectorAll("button").forEach(btn => {
      const t = (btn.textContent || "").trim();
      if (labels.includes(t)) {
        btn.classList.add("ndsp-v13-guarded");
      }
    });
  }

  function patchCopyInvite() {
    const original = window.copyInvite;
    if (typeof original !== "function" || original.__ndspV13Wrapped) return;

    const wrapped = async function (link) {
      try {
        const result = await original.apply(this, arguments);
        toast("Invite link copied.", "ok", 2400);
        return result;
      } catch (err) {
        toast("Copy failed. Open the invite link manually.", "error", 5000);
        throw err;
      }
    };

    wrapped.__ndspV13Wrapped = true;
    window.copyInvite = wrapped;
  }

  function install() {
    wrapFunction("confirmPayment", function () {
      const email = document.getElementById("pay_email")?.value || "";
      const plan = document.getElementById("pay_plan")?.value || "";
      const amount = document.getElementById("pay_amount")?.value || "";
      return "This will confirm a manual payment and activate/update a subscription.\n\nEmail: " + (email || "—") + "\nPlan: " + (plan || "—") + "\nAmount: " + (amount || "—") + "\n\nContinue?";
    }, true);

    wrapFunction("cancelSubscription", function () {
      const telegramId = document.getElementById("cancel_telegram_id")?.value || "";
      return "This will cancel a subscription.\n\nTelegram ID: " + (telegramId || "—") + "\n\nContinue?";
    }, true);

    wrapFunction("revokeInvite", function () {
      const channel = document.getElementById("revoke_channel")?.value || "";
      return "This will revoke an invite link.\n\nChannel: " + (channel || "—") + "\n\nContinue?";
    }, true);

    wrapFunction("markLeadPaid", function (leadId, plan) {
      return "This will mark the lead as paid and create/send an invite.\n\nLead ID: " + leadId + "\nPlan: " + (plan || "—") + "\n\nContinue?";
    }, true);

    wrapFunction("updateLeadStatus", function (leadId, status) {
      const danger = String(status).toLowerCase().includes("cancel");
      return "This will update lead status.\n\nLead ID: " + leadId + "\nNew status: " + status + "\n\nContinue?";
    }, true);

    patchCopyInvite();
    markButtons();

    const observer = new MutationObserver(() => markButtons());
    observer.observe(document.body, { childList: true, subtree: true });

    document.documentElement.setAttribute("data-ndsp-admin-ui", VERSION);
    console.log(VERSION);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", install);
  } else {
    install();
  }
})();
</script>


<script id="ndsp-admin-ui-v14-diagnostics-center">
(function () {
  "use strict";

  const VERSION = "ADMIN_UI_V18_RELEASE_LOCKED";

  function getAdminKey() {
    try {
      return new URLSearchParams(window.location.search).get("admin_key") || "";
    } catch (_) {
      return "";
    }
  }

  function buildUrl(path) {
    const adminKey = getAdminKey();
    const url = new URL(path, window.location.origin);
    if (adminKey) url.searchParams.set("admin_key", adminKey);
    return url.pathname + url.search;
  }

  function toast(message, type) {
    if (typeof window.toast === "function") {
      window.toast(message, type || "ok");
      return;
    }

    const root = document.getElementById("ndsp-v13-toast-root");
    if (root) {
      const item = document.createElement("div");
      item.className = "ndsp-v13-toast " + (type || "ok");
      item.textContent = message;
      root.appendChild(item);
      setTimeout(() => item.remove(), 3500);
      return;
    }

    alert(message);
  }

  function fixDiagnosticsLinks() {
    const adminKey = getAdminKey();

    document.querySelectorAll("#ndsp-v14-diagnostics-center a[href]").forEach(a => {
      const raw = a.getAttribute("href") || "";
      const url = new URL(raw, window.location.origin);

      if (adminKey) {
        url.searchParams.set("admin_key", adminKey);
      }

      a.setAttribute("href", url.pathname + url.search);
      a.setAttribute("target", "_blank");
      a.setAttribute("rel", "noopener noreferrer");
    });

    document.querySelectorAll("[data-copy-json]").forEach(btn => {
      if (btn.dataset.ndspCopyReady === "1") return;
      btn.dataset.ndspCopyReady = "1";

      btn.addEventListener("click", async () => {
        const path = btn.getAttribute("data-copy-json");
        const fullUrl = window.location.origin + buildUrl(path);

        try {
          await navigator.clipboard.writeText(fullUrl);
          toast("JSON URL copied.", "ok");
        } catch (_) {
          toast(fullUrl, "warn", 8000);
        }
      });
    });

    document.documentElement.setAttribute("data-ndsp-admin-ui", VERSION);
    console.log(VERSION);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", fixDiagnosticsLinks);
  } else {
    fixDiagnosticsLinks();
  }
})();
</script>


<script id="ndsp-admin-ui-v15-audit-center">
(function () {
  "use strict";

  const VERSION = "ADMIN_UI_V18_RELEASE_LOCKED";

  function escV15(x) {
    return String(x ?? "")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  }

  function getAdminKeyV15() {
    try {
      return new URLSearchParams(window.location.search).get("admin_key") || "";
    } catch (_) {
      return "";
    }
  }

  async function getJsonV15(path) {
    const adminKey = getAdminKeyV15();
    const sep = path.includes("?") ? "&" : "?";
    const res = await fetch(path + sep + "admin_key=" + encodeURIComponent(adminKey), {
      headers: {"Accept": "application/json"}
    });

    if (!res.ok) {
      throw new Error("HTTP " + res.status);
    }

    return await res.json();
  }

  function normalizeAuditRows(data) {
    if (Array.isArray(data)) return data;
    if (Array.isArray(data?.audit)) return data.audit;
    if (Array.isArray(data?.logs)) return data.logs;
    if (Array.isArray(data?.items)) return data.items;
    if (Array.isArray(data?.records)) return data.records;
    if (Array.isArray(data?.data)) return data.data;
    return [];
  }

  function pick(row, keys) {
    for (const k of keys) {
      if (row && row[k] !== undefined && row[k] !== null && row[k] !== "") return row[k];
    }
    return "";
  }

  function classifyAction(action, details) {
    const s = (String(action || "") + " " + String(details || "")).toLowerCase();

    if (s.includes("cancel") || s.includes("revoke") || s.includes("delete") || s.includes("failed") || s.includes("error")) {
      return "danger";
    }

    if (s.includes("paid") || s.includes("confirm") || s.includes("active") || s.includes("created") || s.includes("success")) {
      return "ok";
    }

    if (s.includes("pending") || s.includes("contacted") || s.includes("invite")) {
      return "warn";
    }

    return "";
  }

  function shortJson(value) {
    if (value === undefined || value === null || value === "") return "—";
    if (typeof value === "string") return value;
    try {
      return JSON.stringify(value);
    } catch (_) {
      return String(value);
    }
  }

  function renderAudit(rows) {
    const root = document.getElementById("ndsp-v15-audit-table");
    const total = document.getElementById("ndsp-v15-audit-total");
    const sensitive = document.getElementById("ndsp-v15-audit-sensitive");
    const last = document.getElementById("ndsp-v15-audit-last");

    if (!root) return;

    const normalized = rows.slice(0, 50);

    const sensitiveCount = rows.filter(r => {
      const action = pick(r, ["action", "event", "type", "operation", "name"]);
      const details = shortJson(pick(r, ["details", "metadata", "payload", "data", "message"]));
      return classifyAction(action, details) === "danger";
    }).length;

    if (total) total.textContent = String(rows.length);
    if (sensitive) sensitive.textContent = String(sensitiveCount);

    const first = rows[0] || {};
    const lastTime = pick(first, ["created_at", "timestamp", "time", "date", "ts"]);
    if (last) last.textContent = lastTime ? String(lastTime).slice(0, 19) : "—";

    if (!normalized.length) {
      root.innerHTML = '<div class="ndsp-v15-audit-empty">No audit records returned from API.</div>';
      return;
    }

    let html = '<table><thead><tr>' +
      '<th>Time</th>' +
      '<th>Action</th>' +
      '<th>Actor</th>' +
      '<th>Target</th>' +
      '<th>Status</th>' +
      '<th>Details</th>' +
      '</tr></thead><tbody>';

    for (const r of normalized) {
      const time = pick(r, ["created_at", "timestamp", "time", "date", "ts"]);
      const action = pick(r, ["action", "event", "type", "operation", "name"]);
      const actor = pick(r, ["actor", "admin", "admin_email", "user", "by"]);
      const target = pick(r, ["target", "email", "telegram_id", "lead_id", "subscription_id", "payment_id"]);
      const status = pick(r, ["status", "result", "state"]);
      const detailsRaw = pick(r, ["details", "metadata", "payload", "data", "message", "note"]);
      const details = shortJson(detailsRaw);
      const cls = classifyAction(action || status, details);

      html += '<tr>' +
        '<td>' + escV15(time ? String(time).slice(0, 19) : "—") + '</td>' +
        '<td><span class="ndsp-v15-audit-pill ' + escV15(cls) + '">' + escV15(action || "event") + '</span></td>' +
        '<td>' + escV15(actor || "—") + '</td>' +
        '<td>' + escV15(target || "—") + '</td>' +
        '<td>' + escV15(status || "—") + '</td>' +
        '<td><div class="ndsp-v15-audit-json" title="' + escV15(details) + '">' + escV15(details || "—") + '</div></td>' +
      '</tr>';
    }

    html += '</tbody></table>';
    root.innerHTML = html;
  }

  async function loadAuditCenter() {
    const root = document.getElementById("ndsp-v15-audit-table");
    if (root) root.innerHTML = '<div class="ndsp-v15-audit-empty">Loading audit records...</div>';

    try {
      const data = await getJsonV15("/api/admin/audit");
      const rows = normalizeAuditRows(data);
      renderAudit(rows);

      if (typeof window.toast === "function") {
        window.toast("Audit Center refreshed.", "ok");
      }
    } catch (err) {
      if (root) root.innerHTML = '<div class="ndsp-v15-audit-empty">Audit load failed: ' + escV15(err.message || err) + '</div>';
      if (typeof window.toast === "function") {
        window.toast("Audit Center failed: " + (err.message || err), "error");
      }
    }
  }

  function installAuditCenter() {
    const btn = document.getElementById("ndsp-v15-refresh-audit");
    if (btn && btn.dataset.ndspV15Ready !== "1") {
      btn.dataset.ndspV15Ready = "1";
      btn.addEventListener("click", loadAuditCenter);
    }

    window.loadAuditCenter = loadAuditCenter;
    document.documentElement.setAttribute("data-ndsp-admin-ui", VERSION);
    console.log(VERSION);

    setTimeout(loadAuditCenter, 600);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", installAuditCenter);
  } else {
    installAuditCenter();
  }
})();
</script>


<script id="ndsp-admin-ui-v16-ux-polish">
(function () {
  "use strict";

  const VERSION = "ADMIN_UI_V18_RELEASE_LOCKED";

  function safeText(x) {
    return String(x || "");
  }

  function ensureIdByHeading(text, id) {
    const headings = Array.from(document.querySelectorAll("h1,h2,h3"));
    const heading = headings.find(h => safeText(h.textContent).trim().toLowerCase() === text.toLowerCase());
    if (!heading) return null;

    const parent = heading.closest("section,.box,.card,div") || heading;
    if (!parent.id) parent.id = id;
    return parent;
  }

  function insertAfter(target, node) {
    if (!target || !target.parentNode) return;
    target.parentNode.insertBefore(node, target.nextSibling);
  }

  function addQuickNav() {
    if (document.getElementById("ndsp-v16-quick-nav")) return;

    const h1 = document.querySelector("h1");
    if (!h1) return;

    const note = document.createElement("div");
    note.id = "ndsp-v16-layout-note";
    note.textContent = "Admin UX finalized: operational controls, diagnostics, audit review, and live tables are now grouped for faster daily management.";

    const nav = document.createElement("nav");
    nav.id = "ndsp-v16-quick-nav";
    nav.innerHTML = [
      '<a href="#ndsp-v12-service-status-bar">Status</a>',
      '<a href="#ndsp-v12-existing-filter">Filters</a>',
      '<a href="#ndsp-v14-diagnostics-center">Diagnostics</a>',
      '<a href="#ndsp-v15-audit-center">Audit</a>',
      '<a href="#ndsp-v16-activate-subscription">Activate</a>',
      '<a href="#ndsp-v16-operational-actions">Actions</a>',
      '<a href="#ndsp-v16-subscriptions">Subscriptions</a>',
      '<a href="#ndsp-v16-payments">Payments</a>',
      '<a href="#ndsp-v16-invites">Invites</a>',
      '<a href="#ndsp-v16-leads">Leads</a>',
      '<a href="#ndsp-v16-telegram-users">Telegram</a>'
    ].join("");

    insertAfter(h1, note);
    insertAfter(note, nav);
  }

  function mapSections() {
    const map = [
      ["Activate Subscription / Manual Payment", "ndsp-v16-activate-subscription", "Revenue Operation"],
      ["Operational Actions", "ndsp-v16-operational-actions", "Sensitive Controls"],
      ["Subscriptions", "ndsp-v16-subscriptions", "Subscriptions Table"],
      ["Payments", "ndsp-v16-payments", "Payments Table"],
      ["Invites", "ndsp-v16-invites", "Invite Links"],
      ["Subscription Leads", "ndsp-v16-leads", "Lead Pipeline"],
      ["Telegram Users", "ndsp-v16-telegram-users", "Telegram Members"]
    ];

    for (const [headingText, id, label] of map) {
      const section = ensureIdByHeading(headingText, id);
      if (!section || section.dataset.ndspV16Ready === "1") continue;

      section.dataset.ndspV16Ready = "1";
      section.classList.add("ndsp-v16-section-shell");

      const heading = Array.from(section.querySelectorAll("h1,h2,h3"))
        .find(h => safeText(h.textContent).trim().toLowerCase() === headingText.toLowerCase());

      if (heading && !section.querySelector(".ndsp-v16-section-label")) {
        const badge = document.createElement("div");
        badge.className = "ndsp-v16-section-label";
        badge.textContent = label;
        section.insertBefore(badge, heading);
      }
    }
  }

  function wrapTables() {
    document.querySelectorAll("table").forEach(table => {
      if (table.closest(".ndsp-v16-table-wrap")) return;
      const wrap = document.createElement("div");
      wrap.className = "ndsp-v16-table-wrap";
      table.parentNode.insertBefore(wrap, table);
      wrap.appendChild(table);
    });
  }

  function addHints() {
    const diagnostics = document.getElementById("ndsp-v14-diagnostics-center");
    if (diagnostics && !diagnostics.querySelector(".ndsp-v16-mini-hint")) {
      const hint = document.createElement("div");
      hint.className = "ndsp-v16-mini-hint";
      hint.textContent = "Tip: JSON tools open in a new tab and Copy URL keeps the admin key embedded for faster debugging.";
      diagnostics.appendChild(hint);
    }

    const audit = document.getElementById("ndsp-v15-audit-center");
    if (audit && !audit.querySelector(".ndsp-v16-mini-hint")) {
      const hint = document.createElement("div");
      hint.className = "ndsp-v16-mini-hint";
      hint.textContent = "Tip: Audit Center is for quick review. Use Audit JSON only when you need raw records.";
      audit.appendChild(hint);
    }
  }

  function polishFooter() {
    const footer = Array.from(document.querySelectorAll("footer,div,p"))
      .find(el => safeText(el.textContent).includes("Nawaf Decision Support Platform") && safeText(el.textContent).includes("rights reserved"));

    if (footer && !footer.querySelector(".ndsp-v16-footer-badge")) {
      const badge = document.createElement("span");
      badge.className = "ndsp-v16-footer-badge";
      badge.textContent = VERSION;
      footer.appendChild(document.createElement("br"));
      footer.appendChild(badge);
    }
  }

  function install() {
    addQuickNav();
    mapSections();
    wrapTables();
    addHints();
    polishFooter();

    const observer = new MutationObserver(() => {
      mapSections();
      wrapTables();
    });

    observer.observe(document.body, { childList: true, subtree: true });

    document.documentElement.setAttribute("data-ndsp-admin-ui", VERSION);
    console.log(VERSION);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", install);
  } else {
    install();
  }
})();
</script>


<script id="ndsp-admin-ui-v17-readiness-panel">
(function () {
  "use strict";

  const VERSION = "ADMIN_UI_V18_RELEASE_LOCKED";

  function getAdminKeyV17() {
    try { return new URLSearchParams(window.location.search).get("admin_key") || ""; }
    catch (_) { return ""; }
  }

  async function fetchJsonV17(path) {
    const adminKey = getAdminKeyV17();
    const sep = path.includes("?") ? "&" : "?";
    const res = await fetch(path + sep + "admin_key=" + encodeURIComponent(adminKey), {
      headers: {"Accept": "application/json"}
    });
    if (!res.ok) throw new Error("HTTP " + res.status);
    return await res.json();
  }

  function setCheck(id, state, message) {
    const el = document.getElementById(id);
    if (!el) return false;
    el.classList.remove("ok", "warn", "down");
    el.classList.add(state);
    const span = el.querySelector("span");
    if (span) span.textContent = message;
    return state === "ok";
  }

  function inferTelegramOk(status) {
    const tg = status?.telegram || status?.telegram_status || {};
    return tg.configured === true || tg.has_token === true || tg.pro_channel_configured === true || tg.vip_channel_configured === true || Number(tg.default_chat_ids_count || 0) > 0;
  }

  function inferDbOk(status) {
    const db = status?.db || status?.database || status?.postgres || {};
    const raw = JSON.stringify(db).toLowerCase();
    if (db.ok === true || db.connected === true || db.status === "ok" || db.status === "running") return true;
    if (raw.includes("ok") || raw.includes("connected") || raw.includes("running")) return true;
    return !!(status?.subscriptions || status?.payments || status?.invites || status?.leads);
  }

  async function runReadinessCheck() {
    const btn = document.getElementById("ndsp-v17-run-check");
    if (btn) {
      btn.disabled = true;
      btn.textContent = "Checking...";
    }

    let passed = 0;
    const total = 8;

    try {
      const status = await fetchJsonV17("/api/admin/system/status");

      if (setCheck("ndsp-v17-check-api", "ok", "System status endpoint is reachable.")) passed++;

      const dbOk = inferDbOk(status);
      if (setCheck("ndsp-v17-check-db", dbOk ? "ok" : "warn", dbOk ? "Database context/data is visible." : "Database state is not explicit; verify manually if needed.")) passed++;

      const tgOk = inferTelegramOk(status);
      if (setCheck("ndsp-v17-check-telegram", tgOk ? "ok" : "warn", tgOk ? "Telegram appears configured." : "Telegram config not confirmed from status JSON.")) passed++;
    } catch (err) {
      setCheck("ndsp-v17-check-api", "down", "System status failed: " + (err.message || err));
      setCheck("ndsp-v17-check-db", "warn", "Skipped because API status failed.");
      setCheck("ndsp-v17-check-telegram", "warn", "Skipped because API status failed.");
    }

    const diagnosticsOk = !!document.getElementById("ndsp-v14-diagnostics-center") && document.querySelectorAll("#ndsp-v14-diagnostics-center [data-copy-json]").length >= 4;
    if (setCheck("ndsp-v17-check-diagnostics", diagnosticsOk ? "ok" : "down", diagnosticsOk ? "Diagnostics Center and Copy URL tools are present." : "Diagnostics Center is missing or incomplete.")) passed++;

    try {
      await fetchJsonV17("/api/admin/audit");
      const auditOk = !!document.getElementById("ndsp-v15-audit-center");
      if (setCheck("ndsp-v17-check-audit", auditOk ? "ok" : "warn", auditOk ? "Audit Center is present and audit endpoint responded." : "Audit endpoint responded but Audit Center missing.")) passed++;
    } catch (err) {
      setCheck("ndsp-v17-check-audit", "warn", "Audit endpoint check returned: " + (err.message || err));
    }

    const safetyOk = !!document.getElementById("ndsp-v13-confirm-modal") && typeof window.confirmPayment === "function" && typeof window.cancelSubscription === "function" && typeof window.revokeInvite === "function";
    if (setCheck("ndsp-v17-check-safety", safetyOk ? "ok" : "down", safetyOk ? "Sensitive action guards are installed." : "Safety guard layer not fully detected.")) passed++;

    const uxOk = !!document.getElementById("ndsp-v16-quick-nav") && document.documentElement.getAttribute("data-ndsp-admin-ui");
    if (setCheck("ndsp-v17-check-ux", uxOk ? "ok" : "warn", uxOk ? "Quick navigation and finalized UX layer detected." : "UX quick navigation not detected.")) passed++;

    const jsonOk = Array.from(document.querySelectorAll("#ndsp-v14-diagnostics-center a[href]")).some(a => (a.getAttribute("href") || "").includes("admin_key="));
    if (setCheck("ndsp-v17-check-json", jsonOk ? "ok" : "warn", jsonOk ? "JSON links include admin key and open externally." : "JSON link key injection needs browser refresh or verification.")) passed++;

    const score = Math.round((passed / total) * 100);

    const scoreEl = document.getElementById("ndsp-v17-score-value");
    const passEl = document.getElementById("ndsp-v17-pass-count");
    const lastEl = document.getElementById("ndsp-v17-last-check");

    if (scoreEl) scoreEl.textContent = score + "%";
    if (passEl) passEl.textContent = passed + "/" + total;
    if (lastEl) lastEl.textContent = new Date().toLocaleString();

    if (typeof window.toast === "function") {
      window.toast("Production readiness check completed: " + score + "%", score >= 75 ? "ok" : "warn");
    }

    if (btn) {
      btn.disabled = false;
      btn.textContent = "Run Readiness Check";
    }
  }

  function insertReadinessLink() {
    const nav = document.getElementById("ndsp-v16-quick-nav");
    if (!nav || nav.querySelector('a[href="#ndsp-v17-readiness-panel"]')) return;

    const a = document.createElement("a");
    a.href = "#ndsp-v17-readiness-panel";
    a.textContent = "Readiness";
    nav.insertBefore(a, nav.firstChild);
  }

  function install() {
    const btn = document.getElementById("ndsp-v17-run-check");
    if (btn && btn.dataset.ndspV17Ready !== "1") {
      btn.dataset.ndspV17Ready = "1";
      btn.addEventListener("click", runReadinessCheck);
    }

    insertReadinessLink();
    window.runReadinessCheck = runReadinessCheck;
    document.documentElement.setAttribute("data-ndsp-admin-ui", VERSION);
    console.log(VERSION);

    setTimeout(runReadinessCheck, 900);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", install);
  } else {
    install();
  }
})();
</script>


<script id="ndsp-admin-ui-v18-release-lock">
(function () {
  "use strict";

  const VERSION = "ADMIN_UI_V18_RELEASE_LOCKED";

  function insertReleaseLink() {
    const nav = document.getElementById("ndsp-v16-quick-nav");
    if (!nav || nav.querySelector('a[href="#ndsp-v18-release-lock"]')) return;

    const a = document.createElement("a");
    a.href = "#ndsp-v18-release-lock";
    a.textContent = "Release Lock";
    nav.insertBefore(a, nav.firstChild);
  }

  function installReleaseLock() {
    insertReleaseLink();
    document.documentElement.setAttribute("data-ndsp-admin-ui", VERSION);
    document.documentElement.setAttribute("data-ndsp-admin-release", "locked");

    if (typeof window.toast === "function") {
      setTimeout(function () {
        window.toast("Admin UI release locked: " + VERSION, "ok");
      }, 1200);
    }

    console.log(VERSION);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", installReleaseLock);
  } else {
    installReleaseLock();
  }
})();
</script>


<section id="elite_trial" class="admin-section" style="margin-top:28px;">
  <div class="section-label">ELITE TRIAL ACCOUNTS</div>
  <h2>Elite Trial Accounts</h2>
  <p>14-day Elite trial gate: first 30 ordinary users and 10 manually activated analysts.</p>

  <div style="display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:12px;margin:18px 0;">
    <div class="card"><b id="etOrdinaryUsed">-</b><br><span>Ordinary Active</span></div>
    <div class="card"><b id="etOrdinaryRemaining">-</b><br><span>Ordinary Remaining</span></div>
    <div class="card"><b id="etAnalystUsed">-</b><br><span>Analysts Active</span></div>
    <div class="card"><b id="etAnalystRemaining">-</b><br><span>Analysts Remaining</span></div>
    <div class="card"><b id="etClosed">-</b><br><span>Closed</span></div>
  </div>

  <div style="display:grid;grid-template-columns:1fr 1fr auto;gap:12px;margin:20px 0;">
    <input id="etAnalystName" placeholder="Analyst name" style="padding:12px;border-radius:12px;background:#081424;color:#fff;border:1px solid rgba(255,255,255,.12);">
    <input id="etAnalystEmail" placeholder="analyst@example.com" style="padding:12px;border-radius:12px;background:#081424;color:#fff;border:1px solid rgba(255,255,255,.12);">
    <button onclick="activateEliteAnalyst()" style="padding:12px 18px;border-radius:12px;border:0;background:#2563eb;color:#fff;font-weight:900;">Activate Analyst</button>
  </div>
  <div id="etMsg" style="color:#42f5a7;font-weight:900;margin-bottom:12px;"></div>

  <div style="overflow:auto;border:1px solid rgba(255,255,255,.12);border-radius:16px;">
    <table style="width:100%;min-width:1050px;border-collapse:collapse;">
      <thead>
        <tr>
          <th>Bucket</th><th>Email</th><th>Name</th><th>Type</th><th>Plan</th><th>Status</th><th>Features</th><th>Created</th><th>Expires</th><th>Reason</th>
        </tr>
      </thead>
      <tbody id="eliteTrialRows">
        <tr><td colspan="10">Loading...</td></tr>
      </tbody>
    </table>
  </div>
</section>

<script>
(function(){
  const qs = new URLSearchParams(location.search);
  window.DSP_ADMIN_KEY = qs.get("admin_key") || qs.get("adminKey") || qs.get("key") || localStorage.getItem("dsp_admin_key") || "";
  if(window.DSP_ADMIN_KEY){ localStorage.setItem("dsp_admin_key", window.DSP_ADMIN_KEY); }

  function esc(v){
    return String(v ?? "").replace(/[&<>"']/g, m => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
  }

  async function loadEliteTrial(){
    if(!window.DSP_ADMIN_KEY){
      window.DSP_ADMIN_KEY = prompt("Admin key:");
      if(!window.DSP_ADMIN_KEY) return;
      localStorage.setItem("dsp_admin_key", window.DSP_ADMIN_KEY);
    }
    const r = await fetch("https://api.ndsp.app/api/v6/elite-trial/admin?admin_key=" + encodeURIComponent(window.DSP_ADMIN_KEY), {cache:"no-store"});
    if(!r.ok){
      const el = document.getElementById("etMsg");
      if(el) el.textContent = "Elite Trial admin API auth failed.";
      return;
    }
    const d = await r.json();
    const s = d.summary || {};
    const set = (id,val)=>{ const el=document.getElementById(id); if(el) el.textContent = val ?? "-"; };
    set("etOrdinaryUsed", s.ordinary_used);
    set("etOrdinaryRemaining", s.ordinary_remaining);
    set("etAnalystUsed", s.analyst_used);
    set("etAnalystRemaining", s.analyst_remaining);
    set("etClosed", s.closed_count);

    const all = [];
    ["ordinary","analysts","waitlist","closed"].forEach(bucket => {
      (d[bucket] || []).forEach(a => all.push({bucket, ...a}));
    });

    const rows = document.getElementById("eliteTrialRows");
    if(rows){
      rows.innerHTML = all.length ? all.map(a => `
        <tr>
          <td>${esc(a.bucket)}</td>
          <td>${esc(a.email)}</td>
          <td>${esc(a.name)}</td>
          <td>${esc(a.type)}</td>
          <td>${esc(a.plan)}</td>
          <td>${esc(a.status)}</td>
          <td>${esc(a.features)}</td>
          <td>${esc(a.created_at)}</td>
          <td>${esc(a.expires_at)}</td>
          <td>${esc(a.close_reason || a.reason)}</td>
        </tr>
      `).join("") : '<tr><td colspan="10">No Elite Trial accounts yet.</td></tr>';
    }
  }

  window.activateEliteAnalyst = async function(){
    const name = document.getElementById("etAnalystName")?.value?.trim() || "";
    const email = document.getElementById("etAnalystEmail")?.value?.trim() || "";
    if(!name || !email){
      document.getElementById("etMsg").textContent = "Name and email are required.";
      return;
    }
    const r = await fetch("https://api.ndsp.app/api/v6/elite-trial/analyst", {
      method:"POST",
      headers:{"Content-Type":"application/json","x-admin-key":window.DSP_ADMIN_KEY},
      body:JSON.stringify({name,email})
    });
    const d = await r.json();
    document.getElementById("etMsg").textContent = d.status === "active" ? "Analyst activated." : ("Failed: " + (d.reason || d.status));
    loadEliteTrial();
  };

  window.loadEliteTrial = loadEliteTrial;
  setTimeout(loadEliteTrial, 1000);
})();
</script>

</body>
</html>
"""
    return html.replace("__ADMIN_KEY__", admin_key or "")
