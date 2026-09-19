import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '../../api/client';
import { ENDPOINTS } from '../../api/endpoints';
import { ValueProposition } from '../../types/capabilities';
import { useUiStore } from '../../store/uiStore';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { ProvenanceBadge } from '../../components/provenance/ProvenanceBadge';
import { AiLoadingState } from '../../components/ui/Skeleton';
import { ProvenanceLegend } from '../../components/provenance/ProvenanceLegend';
import {
  Zap,
  RefreshCw,
  Quote,
  ShieldCheck,
  Target,
  Layers,
  Copy,
  Check,
  Share2,
  Sparkles,
} from 'lucide-react';
import { toast } from 'sonner';

export const ValuePropPage: React.FC = () => {
  const queryClient = useQueryClient();
  const startupId = useUiStore((state) => state.currentStartupId) || 'hyperscale-ai-001';

  const [activeFramework, setActiveFramework] = useState<'yc' | 'venture' | 'category'>('yc');
  const [copiedField, setCopiedField] = useState<string | null>(null);

  const { data: envelope, isLoading } = useQuery({
    queryKey: ['value_proposition', startupId],
    queryFn: () =>
      apiClient<ValueProposition>(ENDPOINTS.AI_GENERATE_VALUE_PROPOSITION, {
        method: 'POST',
        body: { startup_id: startupId },
      }),
  });

  const regenerateMutation = useMutation({
    mutationFn: () =>
      apiClient<ValueProposition>(ENDPOINTS.AI_GENERATE_VALUE_PROPOSITION, {
        method: 'POST',
        body: { startup_id: startupId, force_refresh: true, framework: activeFramework },
      }),
    onSuccess: (res) => {
      queryClient.setQueryData(['value_proposition', startupId], res);
      toast.success(`Value proposition regenerated using ${activeFramework.toUpperCase()} framework!`);
    },
  });

  const handleCopy = (text: string, fieldName: string) => {
    navigator.clipboard.writeText(text);
    setCopiedField(fieldName);
    toast.success(`${fieldName} copied to clipboard!`);
    setTimeout(() => setCopiedField(null), 2000);
  };

  if (isLoading) {
    return (
      <AiLoadingState
        message="Synthesizing Value Proposition..."
        subtext="Distilling startup thesis into an investor-grade elevator pitch and unfair advantage..."
      />
    );
  }

  const vp = envelope?.data;
  const prov = vp?.provenance || {};

  return (
    <div className="space-y-8 pb-16">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="text-xs font-semibold text-brand-700 bg-brand-50 px-2.5 py-0.5 rounded-md border border-brand-200">
              AI Capability: generate_value_proposition
            </span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
            Value Proposition & Positioning
          </h1>
          <p className="text-base text-slate-500 mt-1">
            Crystal-clear positioning, elevator pitch, and defensible moats.
          </p>
        </div>

        <div className="flex items-center gap-2">
          {/* Framework Pills */}
          <div className="hidden sm:flex items-center bg-slate-100 p-1 rounded-xl text-xs font-semibold border border-slate-200">
            <button
              onClick={() => setActiveFramework('yc')}
              className={`px-3 py-1.5 rounded-lg transition-all ${
                activeFramework === 'yc'
                  ? 'bg-white text-slate-900 shadow-xs'
                  : 'text-slate-500 hover:text-slate-800'
              }`}
            >
              YC Essential
            </button>
            <button
              onClick={() => setActiveFramework('venture')}
              className={`px-3 py-1.5 rounded-lg transition-all ${
                activeFramework === 'venture'
                  ? 'bg-white text-slate-900 shadow-xs'
                  : 'text-slate-500 hover:text-slate-800'
              }`}
            >
              Venture Scale
            </button>
            <button
              onClick={() => setActiveFramework('category')}
              className={`px-3 py-1.5 rounded-lg transition-all ${
                activeFramework === 'category'
                  ? 'bg-white text-slate-900 shadow-xs'
                  : 'text-slate-500 hover:text-slate-800'
              }`}
            >
              Category Creator
            </button>
          </div>

          <Button
            variant="outline"
            onClick={() => regenerateMutation.mutate()}
            isLoading={regenerateMutation.isPending}
            loadingText="Regenerating with AI..."
            leftIcon={<RefreshCw className="w-4 h-4 text-brand-600" />}
          >
            Regenerate
          </Button>
        </div>
      </div>

      <ProvenanceLegend />

      {vp && (
        <div className="space-y-6">
          {/* 1. The One-Liner */}
          <Card className="border-brand-300 shadow-md bg-gradient-to-r from-brand-50/40 via-white to-indigo-50/40 relative overflow-hidden group">
            <CardHeader className="pb-2">
              <div className="flex items-center gap-2">
                <Zap className="w-5 h-5 text-brand-600" />
                <CardTitle className="text-brand-950 font-bold">
                  The Anchor One-Liner
                </CardTitle>
              </div>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => handleCopy(vp.one_line, 'One-Liner')}
                  className="p-1.5 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-100 transition-colors"
                  title="Copy to clipboard"
                  aria-label="Copy one liner"
                >
                  {copiedField === 'One-Liner' ? (
                    <Check className="w-4 h-4 text-emerald-600" />
                  ) : (
                    <Copy className="w-4 h-4" />
                  )}
                </button>
                <ProvenanceBadge
                  provenance={prov['one_line'] || 'ai_analysis'}
                  showLabel
                />
              </div>
            </CardHeader>
            <CardContent>
              <blockquote className="text-xl sm:text-2xl font-black text-slate-900 leading-snug tracking-tight">
                &ldquo;{vp.one_line}&rdquo;
              </blockquote>
            </CardContent>
          </Card>

          {/* 2. The 30-Second Elevator Pitch */}
          <Card className="shadow-xs">
            <CardHeader className="pb-2">
              <div className="flex items-center gap-2">
                <Quote className="w-5 h-5 text-indigo-600" />
                <CardTitle>The 30-Second Elevator Pitch</CardTitle>
              </div>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => handleCopy(vp.elevator, 'Elevator Pitch')}
                  className="p-1.5 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-100 transition-colors"
                  title="Copy to clipboard"
                  aria-label="Copy elevator pitch"
                >
                  {copiedField === 'Elevator Pitch' ? (
                    <Check className="w-4 h-4 text-emerald-600" />
                  ) : (
                    <Copy className="w-4 h-4" />
                  )}
                </button>
                <ProvenanceBadge
                  provenance={prov['elevator'] || 'ai_analysis'}
                  showLabel
                />
              </div>
            </CardHeader>
            <CardContent>
              <p className="text-lg text-slate-800 leading-relaxed bg-slate-50/80 p-5 rounded-xl border border-slate-200">
                {vp.elevator}
              </p>
            </CardContent>
          </Card>

          {/* 3. Differentiation & Unfair Advantage 2-column */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Card className="shadow-xs">
              <CardHeader className="pb-2">
                <div className="flex items-center gap-2">
                  <Layers className="w-5 h-5 text-brand-600" />
                  <CardTitle>Core Differentiation</CardTitle>
                </div>
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => handleCopy(vp.differentiation, 'Differentiation')}
                    className="p-1.5 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-100 transition-colors"
                    title="Copy to clipboard"
                    aria-label="Copy differentiation"
                  >
                    {copiedField === 'Differentiation' ? (
                      <Check className="w-4 h-4 text-emerald-600" />
                    ) : (
                      <Copy className="w-4 h-4" />
                    )}
                  </button>
                  <ProvenanceBadge
                    provenance={prov['differentiation'] || 'ai_analysis'}
                    showLabel
                  />
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-base text-slate-700 leading-relaxed">
                  {vp.differentiation}
                </p>
              </CardContent>
            </Card>

            <Card className="shadow-xs">
              <CardHeader className="pb-2">
                <div className="flex items-center gap-2">
                  <ShieldCheck className="w-5 h-5 text-emerald-600" />
                  <CardTitle>Unfair Advantage / Moat</CardTitle>
                </div>
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => handleCopy(vp.advantage, 'Unfair Advantage')}
                    className="p-1.5 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-100 transition-colors"
                    title="Copy to clipboard"
                    aria-label="Copy unfair advantage"
                  >
                    {copiedField === 'Unfair Advantage' ? (
                      <Check className="w-4 h-4 text-emerald-600" />
                    ) : (
                      <Copy className="w-4 h-4" />
                    )}
                  </button>
                  <ProvenanceBadge
                    provenance={prov['advantage'] || 'founder_assumption'}
                    showLabel
                  />
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-base text-slate-700 leading-relaxed">
                  {vp.advantage}
                </p>
              </CardContent>
            </Card>
          </div>

          {/* 4. Target ICP Alignment */}
          <Card className="shadow-xs">
            <CardHeader className="pb-2">
              <div className="flex items-center gap-2">
                <Target className="w-5 h-5 text-rose-500" />
                <CardTitle>Customer-Problem Alignment</CardTitle>
              </div>
              <ProvenanceBadge
                provenance={prov['target_segment'] || 'source_backed'}
                showLabel
              />
            </CardHeader>
            <CardContent className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
              <div className="p-4 rounded-xl bg-slate-50 border border-slate-100">
                <span className="text-xs font-bold uppercase tracking-wider text-slate-400 block mb-1">
                  Target Customer Segment
                </span>
                <p className="text-base font-semibold text-slate-800">
                  {vp.target_segment}
                </p>
              </div>

              <div className="p-4 rounded-xl bg-slate-50 border border-slate-100">
                <span className="text-xs font-bold uppercase tracking-wider text-slate-400 block mb-1">
                  Why They Urgently Buy Now
                </span>
                <p className="text-base font-medium text-slate-700">
                  {vp.customer_problem_alignment}
                </p>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
};
