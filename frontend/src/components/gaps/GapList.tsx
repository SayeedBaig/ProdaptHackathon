import React, { useState } from 'react';
import { Gap } from '../../types/profile';
import { GapCard } from './GapCard';
import { EmptyState } from '../ui/Skeleton';
import { CheckCircle, AlertTriangle } from 'lucide-react';

interface GapListProps {
  gaps: Gap[];
  onToggleStatus: (gapId: string) => void;
  onAnswerGap?: (gap: Gap) => void;
}

export const GapList: React.FC<GapListProps> = ({
  gaps,
  onToggleStatus,
  onAnswerGap,
}) => {
  const [filter, setFilter] = useState<'all' | 'open' | 'resolved'>('open');

  const filteredGaps = gaps.filter((g) => {
    if (filter === 'open') return g.status === 'open';
    if (filter === 'resolved') return g.status === 'resolved';
    return true;
  });

  const openCount = gaps.filter((g) => g.status === 'open').length;
  const resolvedCount = gaps.filter((g) => g.status === 'resolved').length;

  return (
    <div className="space-y-4">
      {/* Header & Filter Tabs */}
      <div className="flex flex-wrap items-center justify-between gap-3 pb-2 border-b border-slate-200">
        <div>
          <h3 className="text-lg font-bold text-slate-900 flex items-center gap-2">
            <AlertTriangle className="w-5 h-5 text-amber-500" />
            Identified Gaps & Diligence Red Flags ({openCount} open)
          </h3>
          <p className="text-xs text-slate-500">
            Issues identified across idea decomposition, deck critique, and investor questions.
          </p>
        </div>

        <div className="flex items-center gap-1 bg-slate-100 p-1 rounded-lg text-xs font-semibold">
          <button
            onClick={() => setFilter('open')}
            className={`px-3 py-1 rounded-md transition-colors ${
              filter === 'open'
                ? 'bg-white text-slate-900 shadow-xs'
                : 'text-slate-500 hover:text-slate-900'
            }`}
          >
            Open ({openCount})
          </button>
          <button
            onClick={() => setFilter('resolved')}
            className={`px-3 py-1 rounded-md transition-colors ${
              filter === 'resolved'
                ? 'bg-white text-slate-900 shadow-xs'
                : 'text-slate-500 hover:text-slate-900'
            }`}
          >
            Resolved ({resolvedCount})
          </button>
          <button
            onClick={() => setFilter('all')}
            className={`px-3 py-1 rounded-md transition-colors ${
              filter === 'all'
                ? 'bg-white text-slate-900 shadow-xs'
                : 'text-slate-500 hover:text-slate-900'
            }`}
          >
            All ({gaps.length})
          </button>
        </div>
      </div>

      {/* List */}
      {filteredGaps.length === 0 ? (
        <EmptyState
          title={
            filter === 'open'
              ? 'No open gaps remaining!'
              : 'No resolved gaps yet.'
          }
          description={
            filter === 'open'
              ? 'Your profile has answered all identified diligence concerns.'
              : 'Resolve gaps by answering clarification questions.'
          }
          icon={<CheckCircle className="w-8 h-8 text-emerald-500" />}
        />
      ) : (
        <div className="space-y-3">
          {filteredGaps.map((gap) => (
            <GapCard
              key={gap.id}
              gap={gap}
              onToggleStatus={onToggleStatus}
              onAnswerGap={onAnswerGap}
            />
          ))}
        </div>
      )}
    </div>
  );
};
