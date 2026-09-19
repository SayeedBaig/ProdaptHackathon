import React from 'react';
import { Gap } from '../../types/profile';
import { Badge } from '../ui/Badge';
import { Button } from '../ui/Button';
import { TOPIC_LABELS } from '../../types/contracts';
import { CheckCircle2, AlertCircle, MessageSquare } from 'lucide-react';

interface GapCardProps {
  gap: Gap;
  onToggleStatus: (gapId: string) => void;
  onAnswerGap?: (gap: Gap) => void;
}

export const GapCard: React.FC<GapCardProps> = ({
  gap,
  onToggleStatus,
  onAnswerGap,
}) => {
  const isResolved = gap.status === 'resolved';

  const severityVariant = (sev: number): 'success' | 'warning' | 'danger' => {
    if (sev >= 4) return 'danger';
    if (sev === 3) return 'warning';
    return 'success';
  };

  const raisedByLabels = {
    idea_analysis: 'Idea Analysis',
    critique: 'Pitch Critique',
    investor: 'Investor Simulation',
  };

  return (
    <div
      className={`p-4 rounded-xl border transition-all duration-150 ${
        isResolved
          ? 'bg-slate-50/60 border-slate-200 opacity-80'
          : 'bg-white border-amber-200/90 shadow-sm hover:border-amber-300'
      }`}
    >
      <div className="flex flex-wrap items-center justify-between gap-2 mb-2">
        <div className="flex items-center gap-2">
          <Badge
            variant={isResolved ? 'default' : severityVariant(gap.severity)}
            size="sm"
          >
            Severity {gap.severity}/5
          </Badge>
          <Badge variant="brand" size="sm">
            {TOPIC_LABELS[gap.topic] || gap.topic}
          </Badge>
          <span className="text-xs text-slate-400">
            Source: {raisedByLabels[gap.raised_by] || gap.raised_by}
          </span>
        </div>

        <button
          onClick={() => onToggleStatus(gap.id)}
          className={`inline-flex items-center gap-1 text-xs font-semibold px-2 py-1 rounded transition-colors ${
            isResolved
              ? 'text-emerald-700 bg-emerald-50 hover:bg-emerald-100'
              : 'text-slate-500 hover:text-slate-800 hover:bg-slate-100'
          }`}
          title={isResolved ? 'Mark as open' : 'Mark as resolved'}
        >
          {isResolved ? (
            <>
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
              Resolved
            </>
          ) : (
            <>
              <AlertCircle className="w-3.5 h-3.5 text-amber-500" />
              Open Gap
            </>
          )}
        </button>
      </div>

      <p className={`text-base font-medium ${isResolved ? 'line-through text-slate-500' : 'text-slate-800'}`}>
        {gap.text}
      </p>

      {!isResolved && onAnswerGap && (
        <div className="mt-3 pt-2 border-t border-slate-100 flex justify-end">
          <Button
            size="sm"
            variant="outline"
            onClick={() => onAnswerGap(gap)}
            leftIcon={<MessageSquare className="w-3.5 h-3.5 text-brand-600" />}
            className="text-xs text-brand-700 hover:bg-brand-50"
          >
            Answer This Gap
          </Button>
        </div>
      )}
    </div>
  );
};
