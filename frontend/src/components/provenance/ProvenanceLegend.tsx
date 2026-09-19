import React from 'react';
import {
  PROVENANCE_VALUES,
  PROVENANCE_ICONS,
  PROVENANCE_LABELS,
  Provenance,
} from '../../types/contracts';

interface ProvenanceLegendProps {
  className?: string;
}

export const ProvenanceLegend: React.FC<ProvenanceLegendProps> = ({ className = '' }) => {
  const descriptions: Record<Provenance, string> = {
    source_backed: 'Verified against external reports, research, or audit data.',
    founder_assumption: 'Hypothesis entered directly by the founder; requires proof.',
    ai_analysis: 'Synthesized by PitchPilot AI from telemetry and market context.',
    calculated: 'Derived via mathematical formulas (CAC, LTV, ratios, etc.).',
  };

  return (
    <div className={`p-4 bg-slate-50/80 rounded-xl border border-slate-200/80 text-sm ${className}`}>
      <div className="flex items-center gap-2 mb-3">
        <span className="font-semibold text-slate-800">Provenance Legend</span>
        <span className="text-xs text-slate-500">
          (Every fact is explicitly labeled to prevent unverified investor claims)
        </span>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
        {PROVENANCE_VALUES.map((prov) => (
          <div
            key={prov}
            className="flex items-start gap-2.5 p-2 rounded-lg bg-white border border-slate-100 shadow-sm"
          >
            <span className="text-base shrink-0 mt-0.5" aria-hidden="true">
              {PROVENANCE_ICONS[prov]}
            </span>
            <div>
              <div className="font-semibold text-slate-800 text-xs">
                {PROVENANCE_LABELS[prov]}
              </div>
              <div className="text-slate-500 text-xs mt-0.5 leading-snug">
                {descriptions[prov]}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
