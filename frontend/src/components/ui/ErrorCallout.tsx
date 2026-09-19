import React, { useState } from 'react';
import { ApiError } from '../../api/errors';
import { Button } from './Button';
import { AlertTriangle, Copy, Check, ChevronDown, ChevronRight, RefreshCw } from 'lucide-react';
import { toast } from 'sonner';

interface ErrorCalloutProps {
  error: Error | ApiError | null;
  onRetry?: () => void;
  className?: string;
}

export const ErrorCallout: React.FC<ErrorCalloutProps> = ({
  error,
  onRetry,
  className = '',
}) => {
  const [isDetailsOpen, setIsDetailsOpen] = useState(false);
  const [hasCopied, setHasCopied] = useState(false);

  if (!error) return null;

  const isApiError = error instanceof ApiError;
  const requestId = isApiError ? (error as ApiError).request_id : 'n/a';
  const code = isApiError ? (error as ApiError).code : 'ERROR';
  const details = isApiError ? (error as ApiError).details : {};

  const handleCopyRequestId = () => {
    navigator.clipboard.writeText(requestId);
    setHasCopied(true);
    toast.success('Request ID copied to clipboard');
    setTimeout(() => setHasCopied(false), 2000);
  };

  const isLlmInvalid = code === 'LLM_INVALID_OUTPUT';
  const isLlmUnavailable = code === 'LLM_UNAVAILABLE';

  return (
    <div
      className={`p-4 rounded-xl border border-rose-200 bg-rose-50/70 text-rose-950 space-y-3 ${className}`}
      role="alert"
    >
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-start gap-2.5">
          <AlertTriangle className="w-5 h-5 text-rose-600 shrink-0 mt-0.5" />
          <div>
            <h4 className="font-bold text-sm text-rose-900">
              {isLlmInvalid
                ? 'The AI returned an unusable answer'
                : isLlmUnavailable
                ? 'AI Service Temporarily Unavailable'
                : error.message || 'An error occurred'}
            </h4>
            <p className="text-xs text-rose-700 mt-0.5 leading-relaxed">
              {isLlmInvalid
                ? 'The language model produced output that did not adhere to the required JSON schema.'
                : isLlmUnavailable
                ? 'The AI provider is experiencing high latency or downtime. Please retry.'
                : error.message}
            </p>
          </div>
        </div>

        {onRetry && (
          <Button
            size="sm"
            variant="outline"
            onClick={onRetry}
            leftIcon={<RefreshCw className="w-3.5 h-3.5 text-rose-700" />}
            className="border-rose-300 text-rose-800 bg-white hover:bg-rose-50 text-xs shrink-0"
          >
            Retry
          </Button>
        )}
      </div>

      {/* Copyable Request ID Disclosure */}
      <div className="pt-2 border-t border-rose-200/60 text-xs">
        <button
          onClick={() => setIsDetailsOpen(!isDetailsOpen)}
          className="flex items-center gap-1 font-semibold text-rose-800 hover:text-rose-950"
        >
          {isDetailsOpen ? (
            <ChevronDown className="w-3.5 h-3.5" />
          ) : (
            <ChevronRight className="w-3.5 h-3.5" />
          )}
          <span>Diagnostic Details</span>
        </button>

        {isDetailsOpen && (
          <div className="mt-2 p-2.5 rounded-lg bg-white/80 border border-rose-200 font-mono text-[11px] text-slate-700 space-y-1.5">
            <div className="flex items-center justify-between">
              <span>Request ID: <strong className="text-slate-900">{requestId}</strong></span>
              <button
                onClick={handleCopyRequestId}
                className="p-1 hover:bg-slate-100 rounded text-slate-500 hover:text-slate-800 inline-flex items-center gap-1"
                title="Copy Request ID"
              >
                {hasCopied ? (
                  <Check className="w-3 h-3 text-emerald-600" />
                ) : (
                  <Copy className="w-3 h-3" />
                )}
                <span>Copy</span>
              </button>
            </div>
            <div>Error Code: <strong>{code}</strong></div>
            {Object.keys(details).length > 0 && (
              <div>Details: {JSON.stringify(details)}</div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
