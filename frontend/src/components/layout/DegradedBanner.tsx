import React from 'react';
import { AlertTriangle, X } from 'lucide-react';
import { useUiStore } from '../../store/uiStore';

interface DegradedBannerProps {
  warnings?: string[];
}

export const DegradedBanner: React.FC<DegradedBannerProps> = ({ warnings = [] }) => {
  const isDismissed = useUiStore((state) => state.isDegradedBannerDismissed);
  const setDismissed = useUiStore((state) => state.setDegradedBannerDismissed);

  if (isDismissed || warnings.length === 0) return null;

  return (
    <div className="bg-amber-500 text-slate-950 px-4 py-2.5 shadow-sm border-b border-amber-600 flex items-center justify-between z-30 relative">
      <div className="flex items-center gap-3 max-w-5xl mx-auto flex-1">
        <AlertTriangle className="w-5 h-5 shrink-0 text-slate-950" />
        <div className="text-sm font-medium">
          <span className="font-bold mr-2">System Degraded:</span>
          {warnings.join(' • ') || 'Operating in fallback mode. Some AI responses may be cached or slower than usual.'}
        </div>
      </div>
      <button
        onClick={() => setDismissed(true)}
        className="p-1 hover:bg-amber-600/30 rounded text-slate-950 transition-colors"
        aria-label="Dismiss banner"
      >
        <X className="w-4 h-4" />
      </button>
    </div>
  );
};
