import React from 'react';
import { SlideContent } from '../../types/capabilities';
import { SLIDE_TITLES } from '../../types/contracts';
import { Badge } from '../../components/ui/Badge';
import { CheckCircle2, AlertCircle } from 'lucide-react';

interface SlideRailProps {
  slides: SlideContent[];
  activeIndex: number;
  onSelectSlide: (index: number) => void;
}

export const SlideRail: React.FC<SlideRailProps> = ({
  slides,
  activeIndex,
  onSelectSlide,
}) => {
  return (
    <div className="space-y-2 overflow-y-auto max-h-[700px] pr-2">
      <div className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2 px-1">
        12-Slide Rail
      </div>

      {slides.map((slide, idx) => {
        const isActive = activeIndex === idx;
        const isComplete = slide.status === 'complete';

        return (
          <button
            key={slide.key}
            onClick={() => onSelectSlide(idx)}
            className={`w-full text-left p-3 rounded-xl border transition-all flex items-start justify-between gap-2 group ${
              isActive
                ? 'bg-brand-50 border-brand-500 ring-2 ring-brand-200 shadow-sm'
                : 'bg-white border-slate-200 hover:border-slate-300 hover:bg-slate-50'
            }`}
          >
            <div className="flex items-start gap-2.5 min-w-0">
              <span
                className={`w-5 h-5 rounded-md flex items-center justify-center text-xs font-bold shrink-0 mt-0.5 ${
                  isActive
                    ? 'bg-brand-600 text-white'
                    : 'bg-slate-100 text-slate-600 group-hover:bg-slate-200'
                }`}
              >
                {idx + 1}
              </span>
              <div className="min-w-0">
                <div
                  className={`text-sm font-semibold truncate ${
                    isActive ? 'text-brand-950' : 'text-slate-800'
                  }`}
                >
                  {SLIDE_TITLES[slide.key] || slide.title}
                </div>
                <div className="text-[11px] text-slate-400 mt-0.5">
                  {slide.bullets?.length || 0} claims / bullets
                </div>
              </div>
            </div>

            {isComplete ? (
              <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
            ) : (
              <AlertCircle className="w-4 h-4 text-amber-500 shrink-0 mt-0.5" />
            )}
          </button>
        );
      })}
    </div>
  );
};
