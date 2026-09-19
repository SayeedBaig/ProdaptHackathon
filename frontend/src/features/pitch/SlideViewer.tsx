import React, { useState, useEffect } from 'react';
import { SlideContent, Claim } from '../../types/capabilities';
import { SLIDE_TITLES, Provenance, PROVENANCE_VALUES, PROVENANCE_LABELS } from '../../types/contracts';
import { ProvenanceBadge } from '../../components/provenance/ProvenanceBadge';
import { renderNullSafe, NullValue } from '../../components/ui/NullValue';
import { Button } from '../../components/ui/Button';
import { ChevronLeft, ChevronRight, Plus, Check } from 'lucide-react';
import { toast } from 'sonner';

interface SlideViewerProps {
  slide: SlideContent;
  index: number;
  total: number;
  startupName?: string;
  onPrev: () => void;
  onNext: () => void;
  onAddBullet?: (claim: Claim) => void;
}

export const SlideViewer: React.FC<SlideViewerProps> = ({
  slide,
  index,
  total,
  startupName = 'Current Startup',
  onPrev,
  onNext,
  onAddBullet,
}) => {
  const [isAddingClaim, setIsAddingClaim] = useState(false);
  const [newClaimText, setNewClaimText] = useState('');
  const [newClaimProv, setNewClaimProv] = useState<Provenance>('founder_assumption');

  // Keyboard navigation for arrow keys
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) {
        return;
      }
      if (e.key === 'ArrowLeft') {
        onPrev();
      } else if (e.key === 'ArrowRight') {
        onNext();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [onPrev, onNext]);

  const handleCreateBullet = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newClaimText.trim()) return;

    if (onAddBullet) {
      onAddBullet({
        text: newClaimText.trim(),
        provenance: newClaimProv,
      });
      toast.success('Added bullet claim to slide!');
      setNewClaimText('');
      setIsAddingClaim(false);
    }
  };

  return (
    <div className="flex flex-col h-full">
      {/* Presentation Canvas (16:9 Aspect Ratio) */}
      <div className="w-full aspect-[16/9] bg-white rounded-2xl border border-slate-200/90 shadow-elevation p-6 sm:p-10 flex flex-col justify-between select-none relative overflow-hidden group">
        {/* Subtle Slide Background Accent */}
        <div className="absolute top-0 right-0 w-96 h-96 bg-gradient-to-bl from-brand-100/40 via-indigo-50/30 to-transparent rounded-full blur-3xl pointer-events-none -mr-20 -mt-20" />

        {/* Slide Top Bar */}
        <div className="flex items-center justify-between border-b border-slate-100 pb-3 mb-3 z-10">
          <div className="flex items-center gap-3">
            <span className="text-xs font-bold uppercase tracking-wider text-brand-700 bg-brand-50 px-2.5 py-1 rounded-md border border-brand-200">
              Slide {index + 1} of {total}
            </span>
            <span className="text-xs text-slate-400 font-medium">
              {startupName}
            </span>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => setIsAddingClaim(true)}
              className="text-xs font-semibold text-brand-700 hover:text-brand-900 bg-brand-50 hover:bg-brand-100 px-2.5 py-1 rounded-md transition-colors inline-flex items-center gap-1"
            >
              <Plus className="w-3.5 h-3.5" /> Add Claim
            </button>
            <span className="text-xs font-mono text-slate-400">
              Key: {slide.key}
            </span>
          </div>
        </div>

        {/* Slide Title */}
        <div className="mb-4 z-10">
          <h2 className="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight leading-snug">
            {slide.title || SLIDE_TITLES[slide.key]}
          </h2>
        </div>

        {/* Bullets Content Area */}
        <div className="flex-1 space-y-3.5 my-auto z-10">
          {(!slide.bullets || slide.bullets.length === 0) ? (
            <div className="p-4 bg-amber-50/70 border border-dashed border-amber-200 rounded-xl">
              <NullValue />
            </div>
          ) : (
            slide.bullets.map((item, idx) => {
              const isClaim = typeof item === 'object' && item !== null && 'provenance' in item;
              const text = isClaim ? (item as Claim).text : (item as string);
              const prov = isClaim ? (item as Claim).provenance : 'ai_analysis';

              return (
                <div
                  key={idx}
                  className="flex items-start justify-between gap-4 p-3 sm:p-3.5 rounded-xl bg-slate-50/80 hover:bg-slate-50 border border-slate-100/90 transition-all shadow-2xs"
                >
                  <div className="flex items-start gap-3">
                    <span className="w-2 h-2 rounded-full bg-brand-600 shrink-0 mt-2.5" />
                    <p className="text-base sm:text-lg text-slate-800 font-medium leading-snug">
                      {renderNullSafe(text)}
                    </p>
                  </div>
                  <div className="shrink-0 mt-0.5">
                    <ProvenanceBadge provenance={prov} showLabel />
                  </div>
                </div>
              );
            })
          )}
        </div>

        {/* Slide Footer */}
        <div className="flex items-center justify-between pt-3 border-t border-slate-100 text-xs text-slate-400 mt-3 z-10">
          <span>Confidential — For Authorized Investor Review Only</span>
          <span>PitchPilot Diligence Coach</span>
        </div>
      </div>

      {/* Inline Add Claim Form */}
      {isAddingClaim && (
        <form
          onSubmit={handleCreateBullet}
          className="mt-3 p-4 rounded-xl bg-white border border-brand-200 shadow-md space-y-3 animate-in fade-in duration-150"
        >
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-800 uppercase tracking-wider">
              Add Bullet Claim to Slide {index + 1}
            </span>
            <button
              type="button"
              onClick={() => setIsAddingClaim(false)}
              className="text-xs text-slate-400 hover:text-slate-600"
            >
              Cancel
            </button>
          </div>

          <input
            type="text"
            value={newClaimText}
            onChange={(e) => setNewClaimText(e.target.value)}
            placeholder="e.g. Proven 3-5x ROI verified across 8 customer cluster deployments..."
            required
            className="w-full px-3 py-2 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-brand-500 outline-none"
          />

          <div className="flex flex-wrap items-center justify-between gap-2">
            <div className="flex items-center gap-2">
              <span className="text-xs font-semibold text-slate-600">Provenance:</span>
              <select
                value={newClaimProv}
                onChange={(e) => setNewClaimProv(e.target.value as Provenance)}
                className="text-xs bg-slate-50 border border-slate-200 rounded-lg px-2.5 py-1 font-medium"
              >
                {PROVENANCE_VALUES.map((p) => (
                  <option key={p} value={p}>
                    {PROVENANCE_LABELS[p]}
                  </option>
                ))}
              </select>
            </div>

            <Button
              type="submit"
              size="sm"
              variant="primary"
              leftIcon={<Check className="w-3.5 h-3.5" />}
            >
              Insert Bullet Claim
            </Button>
          </div>
        </form>
      )}

      {/* Navigation Controls */}
      <div className="flex items-center justify-between mt-4">
        <Button
          variant="outline"
          size="sm"
          onClick={onPrev}
          disabled={index === 0}
          leftIcon={<ChevronLeft className="w-4 h-4" />}
        >
          Previous Slide
        </Button>

        <span className="text-xs sm:text-sm font-semibold text-slate-500">
          Slide {index + 1} of {total} <span className="hidden sm:inline">(Use ← → arrow keys)</span>
        </span>

        <Button
          variant="outline"
          size="sm"
          onClick={onNext}
          disabled={index === total - 1}
          rightIcon={<ChevronRight className="w-4 h-4" />}
        >
          Next Slide
        </Button>
      </div>
    </div>
  );
};
