import React from 'react';
import { Loader2 } from 'lucide-react';

interface SkeletonProps {
  className?: string;
}

export const Skeleton: React.FC<SkeletonProps> = ({ className = '' }) => {
  return (
    <div
      className={`animate-pulse rounded-md bg-slate-200/80 ${className}`}
      aria-hidden="true"
    />
  );
};

interface AiLoadingStateProps {
  message?: string;
  subtext?: string;
  className?: string;
}

export const AiLoadingState: React.FC<AiLoadingStateProps> = ({
  message = 'AI is thinking...',
  subtext = 'Analyzing parameters and generating structured insights (10-30s)...',
  className = '',
}) => {
  return (
    <div
      className={`flex flex-col items-center justify-center p-12 text-center bg-white/70 backdrop-blur-sm rounded-xl border border-brand-100 ${className}`}
    >
      <div className="relative mb-4">
        <div className="w-12 h-12 rounded-full border-4 border-brand-100 border-t-brand-600 animate-spin" />
        <Loader2 className="w-6 h-6 text-brand-600 absolute inset-0 m-auto animate-pulse" />
      </div>
      <h4 className="text-lg font-semibold text-slate-800 tracking-tight mb-1">
        {message}
      </h4>
      <p className="text-sm text-slate-500 max-w-md">{subtext}</p>

      {/* Subtle simulated progress skeleton */}
      <div className="w-64 mt-6 space-y-2">
        <Skeleton className="h-2 w-full bg-brand-100/60" />
        <Skeleton className="h-2 w-4/5 mx-auto bg-brand-100/40" />
      </div>
    </div>
  );
};

interface EmptyStateProps {
  title: string;
  description: string;
  action?: React.ReactNode;
  icon?: React.ReactNode;
  className?: string;
}

export const EmptyState: React.FC<EmptyStateProps> = ({
  title,
  description,
  action,
  icon,
  className = '',
}) => {
  return (
    <div
      className={`flex flex-col items-center justify-center p-12 text-center rounded-xl border-2 border-dashed border-slate-200 bg-slate-50/50 ${className}`}
    >
      {icon && <div className="mb-3 text-slate-400">{icon}</div>}
      <h4 className="text-base font-semibold text-slate-800 mb-1">{title}</h4>
      <p className="text-sm text-slate-500 max-w-sm mb-4">{description}</p>
      {action && <div>{action}</div>}
    </div>
  );
};
