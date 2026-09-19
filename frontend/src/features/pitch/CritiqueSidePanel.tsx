import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '../../api/client';
import { ENDPOINTS } from '../../api/endpoints';
import { PitchCritique } from '../../types/capabilities';
import { Badge } from '../../components/ui/Badge';
import { AiLoadingState } from '../../components/ui/Skeleton';
import { SLIDE_TITLES } from '../../types/contracts';
import { AlertCircle, ShieldAlert, Sparkles, X, CheckSquare } from 'lucide-react';

interface CritiqueSidePanelProps {
  startupId: string;
  isOpen: boolean;
  onClose: () => void;
  onSelectSlideKey?: (slideKey: string) => void;
}

export const CritiqueSidePanel: React.FC<CritiqueSidePanelProps> = ({
  startupId,
  isOpen,
  onClose,
  onSelectSlideKey,
}) => {
  const { data: envelope, isLoading } = useQuery({
    queryKey: ['pitch_critique', startupId],
    queryFn: () =>
      apiClient<PitchCritique>(ENDPOINTS.AI_CRITIQUE_PITCH, {
        method: 'POST',
        body: { startup_id: startupId },
      }),
    enabled: isOpen,
  });

  if (!isOpen) return null;

  const critique = envelope?.data;

  const severityVariant = (sev: string): 'danger' | 'warning' | 'default' => {
    if (sev === 'high') return 'danger';
    if (sev === 'med') return 'warning';
    return 'default';
  };

  return (
    <div className="fixed inset-y-0 right-0 w-full sm:w-[480px] bg-white shadow-2xl border-l border-slate-200 z-50 flex flex-col overflow-hidden animate-in slide-in-from-right duration-200">
      {/* Header */}
      <div className="p-5 border-b border-slate-200 flex items-center justify-between bg-slate-50/80">
        <div className="flex items-center gap-2.5">
          <div className="p-2 rounded-lg bg-rose-100 text-rose-700">
            <ShieldAlert className="w-5 h-5" />
          </div>
          <div>
            <h3 className="font-bold text-slate-900 text-base">
              AI Pitch Deck Critique
            </h3>
            <span className="text-xs text-slate-500">
              capability: critique_pitch
            </span>
          </div>
        </div>

        <button
          onClick={onClose}
          className="p-1.5 text-slate-400 hover:text-slate-700 hover:bg-slate-200 rounded-lg transition-colors"
          aria-label="Close critique panel"
        >
          <X className="w-5 h-5" />
        </button>
      </div>

      {/* Body */}
      <div className="flex-1 overflow-y-auto p-5 space-y-6">
        {isLoading ? (
          <AiLoadingState
            message="Critiquing 12-Slide Deck..."
            subtext="Simulating institutional venture diligence reviews..."
          />
        ) : critique ? (
          <>
            {/* Score Banner */}
            <div className="p-4 rounded-xl bg-gradient-to-r from-brand-50 to-indigo-50 border border-brand-200 flex items-center justify-between">
              <div>
                <span className="text-xs font-bold uppercase tracking-wider text-brand-700 block">
                  Deck Diligence Score
                </span>
                <span className="text-3xl font-black text-brand-950">
                  {critique.overall_score} / 10
                </span>
              </div>
              <Badge variant="brand" size="md">
                Seed Grade
              </Badge>
            </div>

            {/* Top Priorities */}
            <div className="space-y-2">
              <h4 className="text-sm font-bold text-slate-900 uppercase tracking-wider flex items-center gap-2">
                <CheckSquare className="w-4 h-4 text-brand-600" />
                Top Priorities Before Pitching
              </h4>
              <ul className="space-y-2">
                {critique.top_priorities.map((pri, i) => (
                  <li
                    key={i}
                    className="p-3 rounded-lg bg-slate-50 border border-slate-200 text-xs font-medium text-slate-800 flex items-start gap-2 leading-relaxed"
                  >
                    <span className="w-4 h-4 rounded-full bg-brand-600 text-white flex items-center justify-center text-[10px] font-bold shrink-0 mt-0.5">
                      {i + 1}
                    </span>
                    <span>{pri}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Anticipated Investor Objections */}
            <div className="space-y-2">
              <h4 className="text-sm font-bold text-slate-900 uppercase tracking-wider flex items-center gap-2">
                <AlertCircle className="w-4 h-4 text-amber-500" />
                Anticipated Investor Objections
              </h4>
              <div className="space-y-2">
                {critique.investor_objections.map((obj, i) => (
                  <div
                    key={i}
                    className="p-3 rounded-lg bg-amber-50/60 border border-amber-200 text-xs font-medium text-amber-900 leading-relaxed italic"
                  >
                    &ldquo;{obj}&rdquo;
                  </div>
                ))}
              </div>
            </div>

            {/* Identified Issues */}
            <div className="space-y-3">
              <h4 className="text-sm font-bold text-slate-900 uppercase tracking-wider">
                Specific Slide Weaknesses ({critique.issues.length})
              </h4>
              <div className="space-y-3">
                {critique.issues.map((issue, i) => (
                  <div
                    key={i}
                    className="p-4 rounded-xl border border-slate-200 bg-white shadow-xs space-y-2"
                  >
                    <div className="flex items-center justify-between">
                      <button
                        onClick={() => onSelectSlideKey?.(issue.slide_key)}
                        className="text-xs font-bold text-brand-700 hover:underline"
                      >
                        {SLIDE_TITLES[issue.slide_key] || issue.slide_key}
                      </button>
                      <Badge variant={severityVariant(issue.severity)} size="sm">
                        {issue.severity.toUpperCase()} SEVERITY
                      </Badge>
                    </div>

                    <div className="font-semibold text-sm text-slate-900">
                      {issue.title}
                    </div>
                    <p className="text-xs text-slate-600 leading-relaxed">
                      {issue.explanation}
                    </p>

                    <div className="p-2.5 rounded-lg bg-brand-50/60 border border-brand-100 text-xs text-brand-900 leading-relaxed">
                      <span className="font-bold block text-brand-800">
                        Suggested Revision:
                      </span>
                      {issue.suggestion}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </>
        ) : null}
      </div>
    </div>
  );
};
