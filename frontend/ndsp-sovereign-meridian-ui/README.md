# NDSP — Sovereign Meridian UI · Auth Integration

حزمة واجهات React وVite وTypeScript تطبّق ثيم **Sovereign Meridian**، مع مصادقة فعلية عبر عقود NDSP ذات المصدر نفسه، ودعم العربية RTL، وحاجز جلسة وصلاحية أمام لوحة الإدارة.

## التشغيل

يتطلب Node.js 20 أو أحدث:

```bash
npm install
npm run dev
```

فحوص التسليم:

```bash
npm run typecheck
npm run build
npm run test:sites
```

## الصفحات الجاهزة

| المسار | الغرض |
|---|---|
| `/` | الصفحة التسويقية والـHero ومسار الأدلة إلى CORE |
| `/methodology` | مراحل المنهجية وبوابات الجودة وسياسة UTC |
| `/analysis` | التحليل الرسمي الحالي، ويعرض CORE فقط |
| `/documentation` | مركز توثيق هرمي مع البحث وكتل JSON باتجاه LTR |
| `/login` | تسجيل الدخول الفعلي، مع دعم تحدي التحقق بخطوتين |
| `/sign-in` | تحويل متوافق إلى `/login` مع الحفاظ على معاملات الرابط |
| `/forgot-password` | طلب استعادة كلمة المرور |
| `/reset-password?token=...` | تعيين كلمة مرور جديدة عبر الرمز المؤقت |
| `/admin/cot/overview` | الملخص التنفيذي، النتائج، المرشحات، وسلامة الخدمات |
| `/admin/cot/reports` | سجل تقارير CORE ونتائج SHADOW الداخلية |
| `/admin/cot/daily-control` | التحكم بالأسبوع الفعّال وسياسة اليوم |
| `/admin/cot/experiments` | تجارب EXPANDED في SHADOW MODE |
| `/admin/cot/comparisons` | مقارنة النسخ |
| `/admin/cot/governance` | طلبات الترقية والاعتماد |
| `/admin/cot/audit-logs` | سجل التدقيق |
| `/admin/cot/contracts` | حدود العقود البرمجية |
| `/admin/cot/settings` | الخدمات والسياسات والصلاحيات |

## أهم الملفات

```text
src/
├── App.tsx                         # المسارات
├── api/auth.ts                     # عميل المصادقة الفعلي، من دون أسرار
├── auth/
│   ├── AuthContext.tsx             # حالة الجلسة وإنهاؤها
│   └── RequireAdmin.tsx            # حاجز الإدارة المغلق افتراضيًا
├── data.ts                        # بيانات العرض التجريبية
├── styles.css                     # Tokens + جميع الأنماط والاستجابة
├── components/
│   ├── AdminLayout.tsx
│   ├── AuthorityBar.tsx
│   ├── Brand.tsx
│   ├── GovernanceDialog.tsx
│   ├── PublicLayout.tsx
│   └── StatusChip.tsx
└── pages/
    ├── HomePage.tsx
    ├── MethodologyPage.tsx
    ├── AnalysisPage.tsx
    ├── DocumentationPage.tsx
    ├── SignInPage.tsx
    ├── AccountRecoveryPage.tsx
    └── admin/AdminPages.tsx
```

الأصول البصرية الأصلية موجودة في `public/assets/`، ويجب إبقاؤها كصور فعلية وعدم إعادة رسمها باستخدام CSS.

## عقود المصادقة المربوطة

تستخدم الواجهة نفس الأصل، وترسل Cookie الجلسة باستخدام `credentials: include`:

```text
GET  /api/auth/session
POST /api/auth/login
POST /api/auth/2fa/login/verify
POST /api/auth/logout
POST /api/auth/forgot-password
POST /api/auth/reset-password
```

لا تحتوي الحزمة على JWT أو مفاتيح إدارية أو بيانات قاعدة بيانات. ولا تعتمد صلاحية الإدارة على نجاح الدخول وحده؛ يجب أن ترجع الجلسة دورًا إداريًا صريحًا.

## ربط بيانات الصفحات

بيانات التحليل والإدارة الموجودة في `src/data.ts` ما زالت بيانات عرض. عند ربط الخدمات الفعلية:

1. استبدل البيانات في `src/data.ts` بطبقة API typed.
2. اجعل الصفحات العامة تقرأ من عقد Public CORE فقط، مثل:

```text
GET /api/public/core/current?instrument=XAUUSD
```

3. ضع عقود المراجعة والتجارب خلف مسارات الإدارة فقط، مثل:

```text
GET  /api/admin/cot/reports
GET  /api/admin/cot/experiments
POST /api/admin/cot/governance/promotion-requests
```

4. لا تضف أي استيراد أو مسار مباشر من EXPANDED إلى Public API. الترقية تمر عبر Governance Promotion Request والاختبارات والاعتماد.
5. استخدم UTC بصيغة ISO 8601 داخل العقود، مع إبقاء JSON والأكواد باتجاه LTR.

## الثيم

قيم التصميم الأساسية معرفة كـCSS custom properties في بداية `src/styles.css`:

```css
--canvas: #080a0d;
--surface: #0c0f13;
--gold: #cdaa56;
--blue: #35afe3;
--green: #2daa77;
--amber: #d19038;
--red: #cf565d;
--purple: #7962b6;
```

الخط العربي IBM Plex Sans Arabic، واللاتيني Inter، وكلاهما مثبت محليًا من خلال Fontsource.

## حدود مهمة قبل الإنتاج

- المصادقة والاستعادة مربوطتان، لكن بيانات التحليل والإدارة ما زالت Mock Data.
- الحزمة لا تحتوي صفحات بوابة المستخدم التاريخية مثل مركز القرار والحساب والإعدادات.
- لا تحتوي الحزمة عقد تسجيل مستخدم جديد موثقًا بما يكفي، لذلك لم تتم صناعة نموذج تسجيل تخميني.
- لا تحذف `frontend/user-portal-vite` أو أي نشر حالي قبل نقل صفحات المستخدم وعقود بياناتها واختبارها.
- أظهر التدقيق أن المنافذ العامة `80/443` يملكها Docker وأن نطاقات `my/admin/api` أعادت `503`؛ يلزم تدقيق ربط حاويات Docker قبل أي Cutover.
- أزرار الحوكمة تعرض دورة العمل في الواجهة، ولا ترسل قرارات حقيقية.
- جميع العمليات الحساسة يجب أن تبقى قابلة للتدقيق وتعرض الإصدار والسبب والمعتمد وتوقيت UTC.

راجع `AUTH_INTEGRATION_REPORT.md` لمعرفة ما تم ربطه وما بقي قبل النشر.

راجع `NEXT_CHAT_PROMPT_AR.md` للحصول على نص جاهز لبدء المحادثة التالية بهذه الحزمة.
