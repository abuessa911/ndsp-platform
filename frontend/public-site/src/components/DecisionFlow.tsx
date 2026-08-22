import React from 'react';

interface DecisionFlowProps {
  className?: string;
}

export const DecisionFlow: React.FC<DecisionFlowProps> = ({ className = '' }) => {
  const sources = [
    'بيانات مؤسسية',
    'تقارير وتحليلات',
    'سياق تشغيلي',
    'معلومات خارجية',
    'معايير وسياسات'
  ];

  const outputs = [
    'اتجاه رسمي',
    'معتمد حوكميًا',
    'أدلة قابلة للتحقق'
  ];

  return (
    <div className={`relative isolate w-full min-w-0 [container-type:inline-size] ${className}`}>
      {/* Decoupled Glow Effect Layer */}
      <div 
        className="absolute inset-0 -z-10 overflow-clip pointer-events-none select-none" 
        aria-hidden="true"
      >
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-[#CDAA56]/10 rounded-full blur-3xl animate-pulse" />
        <div className="absolute top-1/2 left-1/3 -translate-x-1/2 -translate-y-1/2 w-48 h-48 bg-[#35AFE3]/10 rounded-full blur-2xl" />
      </div>

      {/* 1. DESKTOP WIDE VIEW */}
      <div className="hidden @[60rem]:grid grid-cols-[1fr_auto_1fr] items-center gap-6 w-full dir-rtl">
        <div className="flex flex-col gap-3">
          {sources.map((source, index) => (
            <div 
              key={index} 
              className="p-3 text-sm font-medium text-[#D9DDE2] bg-[#151A20]/80 border border-[#D9DDE2]/10 rounded-lg backdrop-blur-sm text-right transition-colors hover:border-[#CDAA56]/40"
            >
              {source}
            </div>
          ))}
        </div>

        <div className="flex flex-col items-center justify-center px-4 relative">
          <svg className="w-16 h-48 text-[#35AFE3]/40" viewBox="0 0 64 192" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M0 16C32 16 32 96 64 96M0 56C32 56 32 96 64 96M0 96H64M0 136C32 136 32 96 64 96M0 176C32 176 32 96 64 96" stroke="currentColor" strokeWidth="2" strokeDasharray="4 4"/>
          </svg>
          <div className="my-2 px-6 py-3 bg-[#080A0D] border-2 border-[#CDAA56] text-[#CDAA56] font-bold rounded-xl shadow-[0_0_20px_rgba(205,170,86,0.2)]">
            CORE
          </div>
          <svg className="w-16 h-24 text-[#CDAA56]/60" viewBox="0 0 64 96" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M0 48H64" stroke="currentColor" strokeWidth="2"/>
          </svg>
        </div>

        <div className="flex flex-col gap-3">
          {outputs.map((output, index) => (
            <div 
              key={index} 
              className="p-3 text-sm font-semibold text-[#CDAA56] bg-[#CDAA56]/5 border border-[#CDAA56]/20 rounded-lg text-right flex items-center gap-2"
            >
              <span className="w-2 h-2 rounded-full bg-[#CDAA56]" />
              {output}
            </div>
          ))}
        </div>
      </div>

      {/* 2. TABLET COMPACT VIEW */}
      <div className="hidden @[38rem]:grid @[60rem]:hidden grid-cols-1 gap-6 w-full text-center dir-rtl">
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
          {sources.map((source, index) => (
            <div key={index} className="p-2.5 text-xs font-medium text-[#D9DDE2] bg-[#151A20] border border-[#D9DDE2]/10 rounded-md">
              {source}
            </div>
          ))}
        </div>
        <div className="flex items-center justify-center gap-2 my-1">
          <div className="h-px bg-[#35AFE3]/30 flex-1" />
          <span className="px-5 py-2 bg-[#080A0D] border border-[#CDAA56] text-[#CDAA56] font-bold text-sm rounded-lg">
            CORE
          </span>
          <div className="h-px bg-[#CDAA56]/30 flex-1" />
        </div>
        <div className="flex justify-center gap-2 flex-wrap">
          {outputs.map((output, index) => (
            <span key={index} className="px-3 py-1.5 text-xs text-[#CDAA56] bg-[#CDAA56]/10 border border-[#CDAA56]/30 rounded-full">
              ✓ {output}
            </span>
          ))}
        </div>
      </div>

      {/* 3. MOBILE VERTICAL VIEW */}
      <div className="grid @[38rem]:hidden grid-cols-1 gap-3 w-full text-right dir-rtl">
        <div className="p-3 bg-[#151A20]/50 border border-[#D9DDE2]/10 rounded-xl space-y-2">
          <span className="text-xs text-[#77818C] font-mono block mb-1">المصادر المدخلة</span>
          {sources.map((source, index) => (
            <div key={index} className="text-xs text-[#D9DDE2] pr-2 border-r-2 border-[#35AFE3]">
              {source}
            </div>
          ))}
        </div>

        <div className="flex flex-col items-center my-1">
          <div className="w-0.5 h-6 bg-gradient-to-b from-[#35AFE3] to-[#CDAA56]" />
          <div className="w-full text-center py-2.5 bg-[#080A0D] border border-[#CDAA56] text-[#CDAA56] font-bold text-sm rounded-lg shadow-sm">
            CORE
          </div>
          <div className="w-0.5 h-6 bg-[#CDAA56]" />
        </div>

        <div className="p-3 bg-[#CDAA56]/5 border border-[#CDAA56]/20 rounded-xl space-y-2">
          <span className="text-xs text-[#CDAA56] font-mono block mb-1">المخرجات المعتمدة</span>
          {outputs.map((output, index) => (
            <div key={index} className="text-xs text-[#F4F3EF] font-medium flex items-center gap-2">
              <span className="text-[#2DAA77]">✓</span> {output}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
