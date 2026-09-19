import React from 'react';

interface NullValueProps {
  className?: string;
}

export const NULL_DISPLAY_TEXT = 'Not provided — requires validation';

export const NullValue: React.FC<NullValueProps> = ({ className = '' }) => {
  return (
    <span
      className={`inline-flex items-center text-amber-700 bg-amber-50 border border-dashed border-amber-300 rounded px-2 py-0.5 text-sm font-medium italic ${className}`}
      title="This field has not been provided yet and requires validation."
    >
      <span className="mr-1.5 inline-block w-1.5 h-1.5 rounded-full bg-amber-500 animate-pulse" />
      {NULL_DISPLAY_TEXT}
    </span>
  );
};

/**
 * Shared helper to safely render a value or the NullValue component.
 * Ensures null/undefined is never coerced to "", "N/A" or invented strings.
 */
export function renderNullSafe<T>(
  val: T | null | undefined,
  renderFn?: (val: T) => React.ReactNode
): React.ReactNode {
  if (val === null || val === undefined) {
    return <NullValue />;
  }
  if (typeof val === 'string' && val.trim() === '') {
    return <NullValue />;
  }
  if (renderFn) {
    return renderFn(val);
  }
  return String(val);
}
