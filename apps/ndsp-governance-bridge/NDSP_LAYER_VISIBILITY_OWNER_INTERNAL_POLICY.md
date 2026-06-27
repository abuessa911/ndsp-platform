# NDSP Layer Visibility Policy — Owner Internal Unmasked / Public UI Masked

## Status

Authoritative replacement for the old global layer-name masking policy.

## Decision

Layer-name masking is no longer applied inside backend, layer folders, governance bridge, owner audit files, or admin/internal pages.

Masking applies only to public customer-facing UI and public sanitized APIs.

## Visibility Matrix

| Surface | Layer Names | Layer Logic | Code Paths | Raw Mapping |
|---|---:|---:|---:|---:|
| Backend source | Visible | Visible | Visible | Visible |
| Layer source folder | Visible | Visible | Visible | Visible |
| Owner governance files | Visible | Visible | Visible | Visible |
| Admin owner audit | Visible | Visible | Visible | Visible |
| Public frontend | Masked by default | Hidden | Hidden | Hidden |
| Public API | Sanitized by default | Hidden | Hidden | Hidden |

## Publicly Allowed Names

These may remain visible in customer-facing UI when needed:

1. TDL / منطق البعد الزمني
2. NMP / نقطة التقاء نواف
3. Devil's Advocate / محامي الشيطان
4. Nawaf Golden Alignment / إشارة نواف الذهبية

## Owner Internal Rule

All 16 internal layer names, logic descriptions, source file paths, and output mappings are allowed internally for verification and development.

## Public UI Rule

Public UI may show rich outputs without exposing all internal layer names.

## Final Rule

No backend censorship of layer names.  
No layer-folder censorship.  
No owner-admin censorship.  
Only customer-facing masking remains.
