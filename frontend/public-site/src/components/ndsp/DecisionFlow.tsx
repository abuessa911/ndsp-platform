import React from 'react';

interface DecisionFlowProps {
  className?: string;
}

export const DecisionFlow: React.FC<DecisionFlowProps> = ({ className = '' }) => {
  const sources = [
    { id: '01', title: 'الأنظمة واللوائح', sub: 'Regulatory Rules' },
    { id: '02', title: 'سجلات القرارات', sub: 'Decision History' },
    { id: '03', title: 'مؤشرات السوق', sub: 'Market Signals' },
    { id: '04', title: 'التقارير الميدانية', sub: 'Field Intelligence' },
    { id: '05', title: 'المعايير الوطنية', sub: 'National Standards' },
  ];

  return (
    <div className={`w-full relative isolate py-6 ${className}`}>
      {/* 1. Desktop Layout */}
      <div className="hidden lg:grid grid-cols-[1fr_auto_1fr] items-center gap-6 w-full max-w-6xl mx-auto">
        <div className="flex flex-col gap-3">
          {sources.map((src) => (
            <div 
              key={src.id}
              className="flex items-center justify-between p-3 rounded-lg bg-card border border-border/60 hover:border-primary/50 transition-colors shadow-sm"
            >
              <span className="text-xs font-mono text-primary">{src.id}</span>
              <div className="text-right">
                <div className="text-sm font-semibold text-foreground">{src.title}</div>
                <div className="text-[10px] text-muted-foreground">{src.sub}</div>
              </div>
            </div>
          ))}
        </div>

        <div className="flex flex-col items-center justify-center p-8 rounded-2xl bg-card border-2 border-primary/40 shadow-[0_0_30px_rgba(235,189,87,0.15)] relative">
          <div className="w-16 h-16 rounded-full bg-primary/10 border border-primary flex items-center justify-center mb-3">
            <span className="font-heading font-black text-xl text-primary">CORE</span>
          </div>
          <span className="text-xs font-mono tracking-widest text-muted-foreground uppercase">
            Decision Engine
          </span>
        </div>

        <div className="p-5 rounded-xl bg-accent/30 border border-primary/30 text-right">
          <span className="inline-block px-2 py-0.5 rounded text-[10px] font-mono bg-primary/20 text-primary mb-2">
            OUTPUT RESULT
          </span>
          <h4 className="text-lg font-bold text-foreground mb-1">القرار الموصى به</h4>
          <p className="text-xs text-muted-foreground leading-relaxed">
            تحليل مدعوم بالأدلة وقابل للتفسير وفق سياسات الحوكمة.
          </p>
        </div>
      </div>

      {/* 2. Mobile Layout */}
      <div className="flex lg:hidden flex-col gap-4 w-full max-w-md mx-auto">
        <div className="space-y-2">
          <span className="text-xs font-mono text-muted-foreground uppercase px-1">Input Sources</span>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
            {sources.map((src) => (
              <div key={src.id} className="p-2.5 rounded-lg bg-card border border-border text-right">
                <div className="text-xs font-bold text-foreground">{src.title}</div>
                <div className="text-[10px] text-muted-foreground">{src.sub}</div>
              </div>
            ))}
          </div>
        </div>

        <div className="flex justify-center my-1">
          <div className="w-0.5 h-6 bg-gradient-to-b from-border to-primary" />
        </div>

        <div className="p-4 rounded-xl bg-card border border-primary/40 text-center shadow-lg">
          <div className="font-heading font-bold text-primary text-base mb-0.5">محرك CORE</div>
          <div className="text-[11px] text-muted-foreground">معالجة الحوكمة والمطابقة</div>
        </div>

        <div className="flex justify-center my-1">
          <div className="w-0.5 h-6 bg-gradient-to-b from-primary to-border" />
        </div>

        <div className="p-3.5 rounded-lg bg-secondary/60 border border-border text-right">
          <div className="text-xs font-bold text-foreground">التوصية النهائية</div>
          <div className="text-[11px] text-muted-foreground">قرار مؤطر بالكامل مع تحليلات التفسير</div>
        </div>
      </div>
    </div>
  );
};
