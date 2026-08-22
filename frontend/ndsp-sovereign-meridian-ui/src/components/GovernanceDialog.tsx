import { Clock, Info, ShieldCheck, X } from "@phosphor-icons/react";
import { useEffect, useState } from "react";

type GovernanceDialogProps = {
  open: boolean;
  onClose: () => void;
};

export function GovernanceDialog({ open, onClose }: GovernanceDialogProps) {
  const [reason, setReason] = useState("");
  const [approver, setApprover] = useState("فريق الحوكمة");
  const [saved, setSaved] = useState<"draft" | "promoted" | null>(null);

  useEffect(() => {
    if (open) {
      setSaved(null);
      setReason("");
      setApprover("فريق الحوكمة");
    }
  }, [open]);

  if (!open) return null;

  const complete = (state: "draft" | "promoted") => {
    setSaved(state);
    window.setTimeout(onClose, 900);
  };

  return (
    <div className="dialog-backdrop" role="presentation" onMouseDown={(event) => event.currentTarget === event.target && onClose()}>
      <section className="governance-dialog" role="dialog" aria-modal="true" aria-labelledby="governance-title">
        <header className="governance-dialog__header">
          <div className="dialog-icon"><ShieldCheck size={24} /></div>
          <div>
            <span className="eyebrow">GOVERNANCE PROMOTION REQUEST</span>
            <h2 id="governance-title">ترقية منظور تجريبي إلى CORE</h2>
          </div>
          <button className="icon-button" type="button" onClick={onClose} aria-label="إغلاق الحوار">
            <X size={20} />
          </button>
        </header>

        <div className="dialog-impact-grid">
          <article>
            <span>ما الذي سيتغير؟</span>
            <strong>منظور أيام السيطرة</strong>
            <p>استبدال خوارزمية التجميع الداخلية فقط.</p>
          </article>
          <article>
            <span>ما الذي لن يتغير؟</span>
            <strong>عقد Public API</strong>
            <p>لا يتغير الشكل أو المسار أو صلاحيات الوصول.</p>
          </article>
          <article>
            <span>الأثر على المستخدم</span>
            <strong>بعد الاعتماد فقط</strong>
            <p>يظل EXPANDED معزولًا حتى اكتمال جميع الاختبارات.</p>
          </article>
        </div>

        <div className="version-compare" dir="ltr">
          <div><span>CURRENT</span><strong>CORE v4.3.2</strong></div>
          <span className="version-compare__arrow">→</span>
          <div><span>PROPOSED</span><strong>CORE v4.4.0</strong></div>
        </div>

        <div className="dialog-form-grid">
          <label>
            <span>سبب التعديل</span>
            <textarea value={reason} onChange={(event) => setReason(event.target.value)} placeholder="اكتب الدليل والسبب الحوكمي..." />
          </label>
          <label>
            <span>اسم المعتمد</span>
            <input value={approver} onChange={(event) => setApprover(event.target.value)} />
          </label>
          <div className="utc-field">
            <span>توقيت التنفيذ</span>
            <strong dir="ltr"><Clock size={17} /> 2026-08-12 · 02:00 التوقيت العالمي</strong>
          </div>
        </div>

        <div className="dialog-notice">
          <Info size={18} />
          لا يوجد مسار مباشر من EXPANDED إلى Public API. الترقية تنشئ نسخة جديدة قابلة للتراجع.
        </div>

        <footer className="governance-dialog__footer">
          {saved ? (
            <span className="dialog-success">{saved === "draft" ? "تم حفظ المسودة" : "تم إرسال طلب الترقية"}</span>
          ) : (
            <>
              <button className="button button--ghost" type="button" onClick={onClose}>Cancel Without Changes</button>
              <button className="button button--outline" type="button" onClick={() => complete("draft")}>Save as Draft</button>
              <button className="button button--primary" type="button" disabled={!reason.trim()} onClick={() => complete("promoted")}>Promote to CORE</button>
            </>
          )}
        </footer>
      </section>
    </div>
  );
}
