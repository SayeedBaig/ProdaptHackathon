import React, { useState, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '../../api/client';
import { ENDPOINTS } from '../../api/endpoints';
import { Pitch, Claim } from '../../types/capabilities';
import { Profile } from '../../types/profile';
import { useUiStore } from '../../store/uiStore';
import { SlideRail } from './SlideRail';
import { SlideViewer } from './SlideViewer';
import { CritiqueSidePanel } from './CritiqueSidePanel';
import { Button } from '../../components/ui/Button';
import { AiLoadingState } from '../../components/ui/Skeleton';
import { ProvenanceLegend } from '../../components/provenance/ProvenanceLegend';
import { exportPitchDeckToPptx } from '../../utils/pptx';
import {
  Presentation,
  Download,
  ShieldAlert,
  Maximize2,
  X,
  ChevronLeft,
  ChevronRight,
} from 'lucide-react';
import { toast } from 'sonner';

const normalizePitch = (raw: any): Pitch | null => {
  if (!raw) return null;
  const slides = Array.isArray(raw.slides) ? raw.slides : [];
  return {
    ...raw,
    slides: slides.map((slide: any, index: number) => ({
      key: slide.key || `slide_${index + 1}`,
      title: slide.title || `Slide ${index + 1}`,
      bullets: Array.isArray(slide.bullets) ? slide.bullets : [],
      status: slide.status || 'complete',
    })),
  };
};

export const PitchDeckPage: React.FC = () => {
  const startupId = useUiStore((state) => state.currentStartupId) || 'hyperscale-ai-001';
  const [activeSlideIndex, setActiveSlideIndex] = useState(0);
  const [isCritiqueOpen, setIsCritiqueOpen] = useState(false);
  const [isExporting, setIsExporting] = useState(false);
  const [isFullscreen, setIsFullscreen] = useState(false);

  const { data: profileEnvelope } = useQuery({
    queryKey: ['profile', startupId],
    queryFn: () => apiClient<Profile>(ENDPOINTS.PROFILE_GET(startupId)),
    staleTime: 30000,
  });
  const startupName = profileEnvelope?.data?.identity?.startup_name || 'Current Startup';

  // 1. Fetch Pitch Deck
  const { data: envelope, isLoading } = useQuery({
    queryKey: ['pitch_deck', startupId],
    queryFn: () =>
      apiClient<Pitch>(ENDPOINTS.AI_GENERATE_PITCH, {
        method: 'POST',
        body: { startup_id: startupId },
      }),
  });

  const [pitch, setPitch] = useState<Pitch | null>(null);

  useEffect(() => {
    if (envelope?.data) {
      setPitch(normalizePitch(envelope.data));
    }
  }, [envelope?.data]);

  // Fullscreen keyboard escape
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isFullscreen) {
        setIsFullscreen(false);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isFullscreen]);

  const handleDownloadPptx = async () => {
    if (!pitch) return;
    setIsExporting(true);
    try {
      await exportPitchDeckToPptx(pitch, startupName);
      toast.success('Pitch Deck exported to .pptx successfully!', {
        description: 'Downloaded 12 widescreen presentation slides.',
      });
    } catch (err: any) {
      toast.error('Failed to export presentation', {
        description: err.message,
      });
    } finally {
      setIsExporting(false);
    }
  };

  const handleSelectSlideKey = (slideKey: string) => {
    if (!pitch) return;
    const idx = pitch.slides.findIndex((s) => s.key === slideKey);
    if (idx !== -1) {
      setActiveSlideIndex(idx);
      setIsCritiqueOpen(false);
    }
  };

  const handleAddBulletToCurrentSlide = (claim: Claim) => {
    if (!pitch) return;
    const updated = { ...pitch };
    updated.slides = [...updated.slides];
    updated.slides[activeSlideIndex] = {
      ...updated.slides[activeSlideIndex],
      bullets: [...(updated.slides[activeSlideIndex].bullets || []), claim],
    };
    setPitch({ ...updated });
  };

  if (isLoading || !pitch) {
    return (
      <AiLoadingState
        message="Generating 12-Slide Pitch Deck..."
        subtext="Structuring problem, solution, TAM, unit economics, and ask into institutional slides (10-30s)..."
      />
    );
  }

  if (pitch.slides.length === 0) {
    return (
      <div className="space-y-4">
        <h1 className="text-2xl font-bold text-slate-900">Pitch Deck</h1>
        <div className="rounded-xl border border-amber-200 bg-amber-50 p-5 text-sm text-amber-900">
          No slides were returned yet. Try regenerating after the startup profile has more detail.
        </div>
      </div>
    );
  }

  const currentSlide = pitch.slides[activeSlideIndex] || pitch.slides[0];

  return (
    <div className="space-y-6 pb-16">
      {/* Header & Actions */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="text-xs font-semibold text-brand-700 bg-brand-50 px-2.5 py-0.5 rounded-md border border-brand-200">
              AI Capability: generate_pitch
            </span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
            12-Slide Investor Pitch Deck
          </h1>
          <p className="text-base text-slate-500 mt-1">
            Standard institutional slide sequence with client-side PPTX export.
          </p>
        </div>

        <div className="flex items-center gap-2.5">
          <Button
            variant="outline"
            onClick={() => setIsFullscreen(true)}
            leftIcon={<Maximize2 className="w-4 h-4 text-slate-600" />}
            title="Open distraction-free presentation slideshow"
          >
            Present Slides
          </Button>

          <Button
            variant="outline"
            onClick={() => setIsCritiqueOpen(true)}
            leftIcon={<ShieldAlert className="w-4 h-4 text-rose-600" />}
          >
            AI Critique Panel
          </Button>

          <Button
            variant="primary"
            onClick={handleDownloadPptx}
            isLoading={isExporting}
            loadingText="Generating PPTX..."
            leftIcon={<Download className="w-4 h-4" />}
            className="shadow-sm"
          >
            Download PPTX
          </Button>
        </div>
      </div>

      <ProvenanceLegend />

      {/* Main Pitch Deck Viewer & Rail */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 items-start">
        {/* Left Thumbnails Rail */}
        <div className="lg:col-span-1">
          <SlideRail
            slides={pitch.slides}
            activeIndex={activeSlideIndex}
            onSelectSlide={(idx) => setActiveSlideIndex(idx)}
          />
        </div>

        {/* Right Large 16:9 Slide Viewer */}
        <div className="lg:col-span-3">
          <SlideViewer
            slide={currentSlide}
            index={activeSlideIndex}
            total={pitch.slides.length}
            startupName={startupName}
            onPrev={() => setActiveSlideIndex((prev) => Math.max(0, prev - 1))}
            onNext={() =>
              setActiveSlideIndex((prev) =>
                Math.min(pitch.slides.length - 1, prev + 1)
              )
            }
            onAddBullet={handleAddBulletToCurrentSlide}
          />
        </div>
      </div>

      {/* Fullscreen Presentation Mode */}
      {isFullscreen && (
        <div className="fixed inset-0 z-50 bg-slate-950/95 backdrop-blur-md flex flex-col justify-between p-6 sm:p-12 animate-in fade-in duration-200">
          <div className="flex items-center justify-between text-white border-b border-slate-800 pb-4">
            <div className="flex items-center gap-3">
              <span className="font-extrabold text-lg text-white">
                {startupName}
              </span>
              <span className="text-slate-500">•</span>
              <span className="text-sm font-semibold text-brand-400">
                Slide {activeSlideIndex + 1} of {pitch.slides.length}
              </span>
            </div>

            <button
              onClick={() => setIsFullscreen(false)}
              className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white transition-colors"
              aria-label="Exit fullscreen"
            >
              <X className="w-6 h-6" />
            </button>
          </div>

          <div className="w-full max-w-5xl mx-auto my-auto aspect-[16/9] shadow-2xl">
            <SlideViewer
              slide={currentSlide}
              index={activeSlideIndex}
              total={pitch.slides.length}
              startupName={startupName}
              onPrev={() => setActiveSlideIndex((prev) => Math.max(0, prev - 1))}
              onNext={() =>
                setActiveSlideIndex((prev) =>
                  Math.min(pitch.slides.length - 1, prev + 1)
                )
              }
              onAddBullet={handleAddBulletToCurrentSlide}
            />
          </div>

          <div className="text-center text-xs text-slate-500 pt-4">
            Press ESC or click close to exit • Use ← → arrow keys to navigate
          </div>
        </div>
      )}

      {/* Critique Side Panel */}
      <CritiqueSidePanel
        startupId={startupId}
        isOpen={isCritiqueOpen}
        onClose={() => setIsCritiqueOpen(false)}
        onSelectSlideKey={handleSelectSlideKey}
      />
    </div>
  );
};
