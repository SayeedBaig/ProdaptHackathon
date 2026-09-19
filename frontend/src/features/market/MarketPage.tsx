import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '../../api/client';
import { ENDPOINTS } from '../../api/endpoints';
import { CompetitorAnalysis, MarketAnalysis } from '../../types/capabilities';
import { useUiStore } from '../../store/uiStore';
import { MarketSizeVisual } from '../../components/charts/MarketSizeVisual';
import { CompetitorTable } from './CompetitorTable';
import { CompetitorMatrix2x2 } from './CompetitorMatrix2x2';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { AiLoadingState } from '../../components/ui/Skeleton';
import { ProvenanceLegend } from '../../components/provenance/ProvenanceLegend';
import { ProvenanceBadge } from '../../components/provenance/ProvenanceBadge';
import {
  TrendingUp,
  Users,
  AlertTriangle,
  PieChart,
  Sliders,
  Calculator,
} from 'lucide-react';

const fallbackMarketTier = (
  label: string,
  value?: number | null,
  description?: string | null
) => ({
  value: value || 0,
  formatted: value ? `$${value.toLocaleString()}` : 'Requires validation',
  description: description || `${label} sizing requires validation.`,
  calculation_steps: ['Founder inputs and market sizing assumptions need validation.'],
  provenance: 'founder_assumption' as const,
  sources: [],
});

const normalizeMarket = (raw: any): MarketAnalysis | null => {
  if (!raw) return null;

  return {
    ...raw,
    tam: raw.tam || fallbackMarketTier('TAM', raw.market_size?.tam, raw.market_size?.status),
    sam: raw.sam || fallbackMarketTier('SAM', raw.market_size?.sam, raw.market_size?.status),
    som: raw.som || fallbackMarketTier('SOM', raw.market_size?.som, raw.market_size?.status),
    cagr: raw.cagr ?? 0,
    growth_drivers: raw.growth_drivers || raw.opportunities?.map((item: any) => item.text || String(item)) || [],
    market_risks: raw.market_risks || raw.threats?.map((item: any) => item.text || String(item)) || [],
    assumptions: raw.assumptions || [],
  };
};

const normalizeCompetitors = (raw: any): CompetitorAnalysis | null => {
  if (!raw) return null;

  const directCompetitors = raw.direct_competitors || raw.competitors || [];
  return {
    ...raw,
    direct_competitors: directCompetitors.map((comp: any) => ({
      name: comp.name || 'Unnamed competitor',
      description: comp.description || comp.differentiation || 'No description available.',
      strengths: comp.strengths || [],
      weaknesses: comp.weaknesses || [],
      pricing: comp.pricing || 'Not available',
      market_share: comp.market_share || 'Not available',
      differentiator: comp.differentiator || comp.differentiation || 'Differentiation requires validation.',
      provenance: comp.provenance || 'ai_analysis',
      source_urls: comp.source_urls || [],
    })),
    indirect_competitors: raw.indirect_competitors || [],
    matrix_axes: raw.matrix_axes || {
      x_axis: 'Passive reporting -> Autonomous action',
      y_axis: 'Broad market -> Focused niche',
    },
    competitor_positions: raw.competitor_positions || directCompetitors.map((comp: any, index: number) => ({
      name: comp.name || `Competitor ${index + 1}`,
      x: -6 + index * 4,
      y: 4 - index * 2,
      is_self: false,
    })),
  };
};

export const MarketPage: React.FC = () => {
  const startupId = useUiStore((state) => state.currentStartupId) || 'hyperscale-ai-001';

  // Sizing Sandbox interactive state
  const [activeTab, setActiveTab] = useState<'baseline' | 'sandbox'>('baseline');
  const [simAccounts, setSimAccounts] = useState(50000);
  const [simAcv, setSimAcv] = useState(57000);

  // 1. Fetch Market Analysis
  const { data: marketEnvelope, isLoading: isMarketLoading } = useQuery({
    queryKey: ['market_analysis', startupId],
    queryFn: () =>
      apiClient<MarketAnalysis>(ENDPOINTS.AI_ANALYZE_MARKET, {
        method: 'POST',
        body: { startup_id: startupId },
      }),
  });

  // 2. Fetch Competitor Analysis
  const { data: competitorEnvelope, isLoading: isCompetitorLoading } = useQuery({
    queryKey: ['competitor_analysis', startupId],
    queryFn: () =>
      apiClient<CompetitorAnalysis>(ENDPOINTS.AI_ANALYZE_COMPETITORS, {
        method: 'POST',
        body: { startup_id: startupId },
      }),
  });

  if (isMarketLoading || isCompetitorLoading) {
    return (
      <AiLoadingState
        message="Analyzing Market Size & Competitive Dynamics..."
        subtext="Crunching market reports, TAM/SAM/SOM baselines, and competitor feature vectors (10-30s)..."
      />
    );
  }

  const market = normalizeMarket(marketEnvelope?.data);
  const comp = normalizeCompetitors(competitorEnvelope?.data);

  // Calculated sandbox values
  const simTam = simAccounts * simAcv;
  const simSam = Math.round(simTam * 0.2175);
  const simSom = Math.round(simSam * 0.0725);

  const formatCurrency = (val: number): string => {
    if (val >= 1e9) return `$${(val / 1e9).toFixed(1)}B`;
    if (val >= 1e6) return `$${(val / 1e6).toFixed(0)}M`;
    return `$${val.toLocaleString()}`;
  };

  return (
    <div className="space-y-8 pb-16">
      {/* Header */}
      <div>
        <div className="flex items-center gap-2 mb-1">
          <span className="text-xs font-semibold text-brand-700 bg-brand-50 px-2.5 py-0.5 rounded-md border border-brand-200">
            AI Capabilities: analyze_market & analyze_competitors
          </span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
          Market Sizing & Competitive Landscape
        </h1>
        <p className="text-base text-slate-500 mt-1">
          Institutional-grade market breakdown, interactive sizing sandbox, and competitor positioning.
        </p>
      </div>

      <ProvenanceLegend />

      {/* 1. Market Sizing Visualization with Sandbox Toggle */}
      {market && (
        <div className="space-y-6">
          <Card>
            <CardHeader className="flex-wrap gap-4">
              <div className="flex items-center gap-2">
                <PieChart className="w-5 h-5 text-blue-600" />
                <CardTitle>Market Opportunity: TAM / SAM / SOM Breakdown</CardTitle>
              </div>

              <div className="flex items-center gap-3">
                <div className="flex items-center bg-slate-100 p-1 rounded-xl text-xs font-semibold border border-slate-200">
                  <button
                    onClick={() => setActiveTab('baseline')}
                    className={`px-3 py-1.5 rounded-lg transition-all ${
                      activeTab === 'baseline'
                        ? 'bg-white text-slate-900 shadow-xs'
                        : 'text-slate-500 hover:text-slate-800'
                    }`}
                  >
                    Audited Baseline
                  </button>
                  <button
                    onClick={() => setActiveTab('sandbox')}
                    className={`px-3 py-1.5 rounded-lg transition-all flex items-center gap-1.5 ${
                      activeTab === 'sandbox'
                        ? 'bg-white text-slate-900 shadow-xs'
                        : 'text-slate-500 hover:text-slate-800'
                    }`}
                  >
                    <Sliders className="w-3.5 h-3.5 text-brand-600" />
                    Interactive Sandbox
                  </button>
                </div>

                {market.cagr > 0 && (
                  <span className="text-xs font-extrabold text-emerald-600 bg-emerald-50 px-2.5 py-1 rounded-md border border-emerald-200">
                    +{market.cagr}% CAGR
                  </span>
                )}
              </div>
            </CardHeader>
            <CardContent>
              {activeTab === 'baseline' ? (
                <MarketSizeVisual
                  tam={market.tam}
                  sam={market.sam}
                  som={market.som}
                />
              ) : (
                /* Interactive Sandbox Mode */
                <div className="space-y-6">
                  <div className="p-4 rounded-xl bg-purple-50/70 border border-purple-200 flex items-center justify-between">
                    <div className="flex items-center gap-2 text-purple-900 text-xs font-semibold">
                      <Calculator className="w-4 h-4 text-purple-600" />
                      Dynamic TAM/SAM/SOM Sizing Sandbox (Simulate different market penetration assumptions)
                    </div>
                    <ProvenanceBadge provenance="calculated" showLabel />
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6 p-4 bg-slate-50 rounded-xl border border-slate-200">
                    <div>
                      <div className="flex justify-between text-xs font-bold text-slate-700 mb-2">
                        <span>Target Global Enterprises:</span>
                        <span className="font-extrabold text-brand-700">
                          {simAccounts.toLocaleString()} accounts
                        </span>
                      </div>
                      <input
                        type="range"
                        min="10000"
                        max="100000"
                        step="5000"
                        value={simAccounts}
                        onChange={(e) => setSimAccounts(Number(e.target.value))}
                        className="w-full accent-brand-600 cursor-pointer"
                      />
                      <div className="flex justify-between text-[11px] text-slate-400 mt-1">
                        <span>10,000</span>
                        <span>100,000</span>
                      </div>
                    </div>

                    <div>
                      <div className="flex justify-between text-xs font-bold text-slate-700 mb-2">
                        <span>Average Annual Contract Value (ACV):</span>
                        <span className="font-extrabold text-brand-700">
                          ${simAcv.toLocaleString()} / year
                        </span>
                      </div>
                      <input
                        type="range"
                        min="15000"
                        max="120000"
                        step="5000"
                        value={simAcv}
                        onChange={(e) => setSimAcv(Number(e.target.value))}
                        className="w-full accent-brand-600 cursor-pointer"
                      />
                      <div className="flex justify-between text-[11px] text-slate-400 mt-1">
                        <span>$15,000</span>
                        <span>$120,000</span>
                      </div>
                    </div>
                  </div>

                  {/* Sandbox Simulated Results Grid */}
                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                    <div className="p-4 rounded-xl bg-blue-50 border border-blue-200">
                      <span className="text-xs font-bold uppercase text-blue-700 block">
                        Simulated TAM
                      </span>
                      <div className="text-3xl font-black text-blue-950 mt-1">
                        {formatCurrency(simTam)}
                      </div>
                      <span className="text-[11px] text-blue-600 mt-1 block">
                        100% of global accounts
                      </span>
                    </div>

                    <div className="p-4 rounded-xl bg-indigo-50 border border-indigo-200">
                      <span className="text-xs font-bold uppercase text-indigo-700 block">
                        Simulated SAM
                      </span>
                      <div className="text-3xl font-black text-indigo-950 mt-1">
                        {formatCurrency(simSam)}
                      </div>
                      <span className="text-[11px] text-indigo-600 mt-1 block">
                        21.8% containerized spend
                      </span>
                    </div>

                    <div className="p-4 rounded-xl bg-emerald-50 border border-emerald-200">
                      <span className="text-xs font-bold uppercase text-emerald-700 block">
                        Simulated SOM
                      </span>
                      <div className="text-3xl font-black text-emerald-950 mt-1">
                        {formatCurrency(simSom)}
                      </div>
                      <span className="text-[11px] text-emerald-700 font-semibold mt-1 block">
                        7.3% bottoms-up pipeline
                      </span>
                    </div>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Growth Drivers & Market Risks */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <div className="flex items-center gap-2">
                  <TrendingUp className="w-5 h-5 text-emerald-600" />
                  <CardTitle>Market Growth Catalysts</CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2 text-sm text-slate-700">
                  {market.growth_drivers.length > 0 ? market.growth_drivers.map((driver, i) => (
                    <li key={i} className="flex items-start gap-2">
                      <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 shrink-0 mt-2" />
                      <span>{driver}</span>
                    </li>
                  )) : (
                    <li className="text-slate-500">No growth catalysts have been validated yet.</li>
                  )}
                </ul>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <div className="flex items-center gap-2">
                  <AlertTriangle className="w-5 h-5 text-amber-500" />
                  <CardTitle>Market Headwinds & Risks</CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2 text-sm text-slate-700">
                  {market.market_risks.length > 0 ? market.market_risks.map((risk, i) => (
                    <li key={i} className="flex items-start gap-2">
                      <span className="w-1.5 h-1.5 rounded-full bg-amber-500 shrink-0 mt-2" />
                      <span>{risk}</span>
                    </li>
                  )) : (
                    <li className="text-slate-500">No market risks have been recorded yet.</li>
                  )}
                </ul>
              </CardContent>
            </Card>
          </div>
        </div>
      )}

      {/* 2. Competitor Landscape */}
      {comp && (
        <div className="space-y-6 pt-4 border-t border-slate-200">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2">
                <Users className="w-5 h-5 text-indigo-600" />
                Direct & Indirect Competitor Analysis
              </h2>
              <p className="text-xs text-slate-500 mt-0.5">
                Evaluated against existing market offerings with source verification.
              </p>
            </div>
          </div>

          <CompetitorTable competitors={comp.direct_competitors} />

          {comp.competitor_positions.length > 0 && (
            <CompetitorMatrix2x2
              axes={comp.matrix_axes}
              positions={comp.competitor_positions}
            />
          )}
        </div>
      )}
    </div>
  );
};
