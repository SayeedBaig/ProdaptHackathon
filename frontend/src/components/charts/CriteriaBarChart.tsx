import React from 'react';
import { CriteriaKey, CRITERIA_LABELS } from '../../types/contracts';

interface CriteriaBarChartProps {
  scores: Record<CriteriaKey, number>;
}

export const CriteriaBarChart: React.FC<CriteriaBarChartProps> = ({ scores }) => {
  const safeScores = scores || {};
  const keys = Object.keys(safeScores) as CriteriaKey[];

  const getBarColor = (score: number): string => {
    if (score >= 8) return 'bg-emerald-500';
    if (score >= 6) return 'bg-brand-500';
    if (score >= 4) return 'bg-amber-500';
    return 'bg-rose-500';
  };

  return (
    <div className="space-y-3">
      {keys.map((key) => {
        const score = safeScores[key] || 0;
        const percentage = Math.min(100, Math.max(0, (score / 10) * 100));

        return (
          <div key={key} className="space-y-1">
            <div className="flex items-center justify-between text-xs font-semibold">
              <span className="text-slate-700">{CRITERIA_LABELS[key] || key}</span>
              <span className="text-slate-900 font-bold">{score} / 10</span>
            </div>
            <div className="w-full h-2 rounded-full bg-slate-100 overflow-hidden">
              <div
                style={{ width: `${percentage}%` }}
                className={`h-full rounded-full transition-all duration-500 ${getBarColor(
                  score
                )}`}
              />
            </div>
          </div>
        );
      })}
    </div>
  );
};
