<!-- BEGIN NDSP ROOT GOVERNANCE -->
# NDSP Root Instructions for Agents

MANDATORY: Before any work that can change this repository or its runtime, read:

- `governance/change-control/NDSP_ROOT_CHANGE_GOVERNANCE.md`
- `governance/change-control/NDSP_ROOT_POLICY.json`
- `governance/change-control/NDSP_CURRENT_PRELAUNCH_STATE.env`

Required mutation sequence:

READ → CLASSIFY → DISCOVER → SCOPE → BACKUP/ROLLBACK → CHANGE → VERIFY → RECORD → SEAL.

Never expose secrets.

Nested instructions may refine but MUST NOT weaken root governance.

PUBLIC_LAUNCH is currently NO.

Coolify/Traefik is transitional and must not be treated as the final NDSP deployment authority.
<!-- END NDSP ROOT GOVERNANCE -->

<!-- NDSP_FULL_CAPABILITY_UI_GOVERNANCE_START -->

# NDSP Full-Capability Product Contract

The visible frontend is not the complete definition of NDSP.

Before changing algorithms, services, APIs, data contracts, frontend code,
product flows, or interface design, every human or automated agent must inspect:

- `docs/99-governance/pr-018-full-capability-ui-governance/`
- `CAPABILITY_UI_TRACEABILITY.csv`
- relevant canonical runtime governance artifacts
- the actual source logic, service, endpoint, data, and frontend consumer

Every material capability must be traceable through:

`capability -> source_or_algorithm -> service -> endpoint_or_contract ->
real_data -> user_role -> screen -> visible_component -> evidence`

Mandatory rules:

- Never omit a verified capability merely because it is absent from the UI.
- Never replace real calculations with mock or decorative values.
- Never claim complete coverage without machine-verifiable evidence.
- Mark unknown mappings as `DISCOVERY_REQUIRED`.
- Update traceability when product logic, APIs, or UI behavior changes.
- Internal formulas may remain protected, but user-relevant capabilities must
  have an accurate product representation or a governed exclusion.

<!-- NDSP_FULL_CAPABILITY_UI_GOVERNANCE_END -->

<!-- NDSP_DISCOVER_REUSE_START -->

## NDSP — البحث وإعادة الاستخدام قبل الإنشاء

قبل إنشاء أو إضافة أي:

- محرك
- خدمة
- API أو Gateway
- طبقة تحليلية
- صفحة أو مكوّن واجهة
- عقد أو Schema
- سياسة حوكمة
- اختبار
- أداة نشر أو تكامل

يجب تنفيذ التسلسل الإلزامي التالي:

1. **Discover** — البحث في المشروع والسجلات والعقود والخدمات.
2. **Reuse** — إعادة استخدام المكوّن القائم إن كان مناسبًا.
3. **Extend** — توسعة المكوّن القائم بدل إنشاء بديل.
4. **Merge** — دمج المكونات المتداخلة أو المتكررة.
5. **Create** — الإنشاء فقط بعد إثبات أن الخيارات السابقة غير كافية.
6. **Register** — تسجيل المالك والمسار والعقد والاختبارات والأدلة.

يحظر نسخ مكوّن قائم وتغيير اسمه فقط، أو إنشاء مالكين canonical
للوظيفة نفسها، أو إنشاء مكونات مشروع جديدة داخل `/opt`.

السياسة المركزية:

`governance/canonical-v1/NDSP_DISCOVER_REUSE_GOVERNANCE_V1_AR.md`

أي سياسة محلية يمكن أن تكون أشد، لكنها لا يجوز أن تلغي أو تخفف
هذه القاعدة.

<!-- NDSP_DISCOVER_REUSE_END -->
