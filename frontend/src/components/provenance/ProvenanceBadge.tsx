import React from 'react';
import {
  Provenance,
  PROVENANCE_ICONS,
  PROVENANCE_LABELS,
} from '../../types/contracts';

interface ProvenanceBadgeProps {
  provenance?: Provenance | 'founder' | string | null;
  className?: string;
  showLabel?: boolean;
}

export const ProvenanceBadge: React.FC<ProvenanceBadgeProps> = ({
  provenance,
  className = '',
  showLabel = false,
}) => {
  // Normalize 'founder' to 'founder_assumption' as logged in CONTRACT_ISSUES.md
  const normalized: Provenance =
    provenance === 'founder'
      ? 'founder_assumption'
      : (provenance as Provenance) || 'founder_assumption';

  const icon = PROVENANCE_ICONS[normalized] || '🟡';
  const label = PROVENANCE_LABELS[normalized] || 'Founder Assumption';

  const styleMap: Record<Provenance, string> = {
    source_backed: 'bg-emerald-50 text-emerald-800 border-emerald-200/80 hover:bg-emerald-100',
    founder_assumption: 'bg-amber-50 text-amber-800 border-amber-200/80 hover:bg-amber-100',
    ai_analysis: 'bg-sky-50 text-sky-800 border-sky-200/80 hover:bg-sky-100',
    calculated: 'bg-purple-50 text-purple-800 border-purple-200/80 hover:bg-purple-100',
  };

  return (
    <span
      className={`inline-flex items-center gap-1 px-2 py-0.5 text-xs font-semibold rounded-full border transition-colors cursor-help select-none ${styleMap[normalized]} ${className}`}
      title={`Provenance: ${label} (${icon})`}
    >
      <span className="text-xs" aria-hidden="true">{icon}</span>
      {showLabel && <span>{label}</span>}
    </span>
  );
};
