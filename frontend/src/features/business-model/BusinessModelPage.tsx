import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '../../api/client';
import { ENDPOINTS } from '../../api/endpoints';
import { BusinessModelAnalysis } from '../../types/capabilities';
import { useUiStore } from '../../store/uiStore';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { ProvenanceBadge } from '../../components/provenance/ProvenanceBadge';
import { AiLoadingState } from '../../components/ui/Skeleton';
import { ProvenanceLegend } from '../../components/provenance/ProvenanceLegend';
import { Badge } from '../../components/ui/Badge';
import {
  CircleDollarSign,
  Calculator,
  Check,
  Percent,
  Layers,
  BarChart3,
  Sliders,
  Sparkles,
} from 'lucide-react';

const normalizeBusinessModel = (raw: any): BusinessModelAnalysis | null => {
  if (!raw) return null;

  const revenueStreams = raw.revenue_streams || [
    {
      name: 'Primary Revenue',
      model_type: raw.revenue_source || raw.type || 'Revenue model requires validation',
      price_point: raw.pricing || 'Pricing requires validation',
      frequency: 'TBD',
      margin: 'TBD',
      calculated: false,
      provenance: 'founder_assumption',
    },
  ];

  const pricingTiers = raw.pricing_tiers || [
    {
      tier_name: 'Initial Offer',
      price: raw.pricing || 'TBD',
      billing: 'Requires validation',
      features: [raw.go_to_market || 'Go-to-market plan requires validation'],
      target_audience: raw.customer || raw.payer || 'Target customer requires validation',
    },
  ];

  return {
    ...raw,
    type: raw.type || 'Business model requires validation',
    revenue_streams: revenueStreams,
    pricing_tiers: pricingTiers,
    unit_economics: raw.unit_economics || null,
    cost_structure: raw.cost_structure || (raw.costs ? [raw.costs] : []),
  };
};

export const BusinessModelPage: React.FC = () => {
  const startupId = useUiStore((state) => state.currentStartupId) || 'hyperscale-ai-001';

  // Interactive Unit Economics Sensitivity Sandbox state
  const [activeTab, setActiveTab] = useState<'audited' | 'sandbox'>('audited');
  const [simCac, setSimCac] = useState(6200);
  const [simMonthlyArpu, setSimMonthlyArpu] = useState(1350);
  const [simMargin, setSimMargin] = useState(87.5);
  const [simChurn, setSimChurn] = useState(1.5); // 1.5% monthly churn

  const { data: envelope, isLoading } = useQuery({
    queryKey: ['business_model_analysis', startupId],
    queryFn: () =>
      apiClient<BusinessModelAnalysis>(ENDPOINTS.AI_ANALYZE_BUSINESS_MODEL, {
        method: 'POST',
        body: { startup_id: startupId },
      }),
  });

  if (isLoading) {
    return (
      <AiLoadingState
        message="Evaluating Business Model & Unit Economics..."
        subtext="Modeling pricing tiers, CAC, LTV, payback periods, and software margins (10-30s)..."
      />
    );
  }

  const bm = normalizeBusinessModel(envelope?.data);
  const ue = bm?.unit_economics;

  // Sandbox Live Calculations
  const simCustomerLifetimeMonths = Math.round(100 / simChurn);
  const simLtv = Math.round(simMonthlyArpu * (simMargin / 100) * simCustomerLifetimeMonths);
  const simLtvCac = Number((simLtv / (simCac || 1)).toFixed(2));
  const simPayback = Number(((simCac / (simMonthlyArpu * (simMargin / 100))) || 0).toFixed(1));

  const getLtvCacBadge = (ratio: number) => {
    if (ratio >= 5.0) return { label: '🔥 Top-Decile Scale (>5x)', variant: 'success' as const };
    if (ratio >= 3.0) return { label: '✓ Healthy Venture Scale (3-5x)', variant: 'brand' as const };
    return { label: '⚠️ Requires Optimization (<3x)', variant: 'warning' as const };
  };

  const currentBadge = getLtvCacBadge(simLtvCac);

  return (
    <div className="space-y-8 pb-16">
      {/* Header */}
      <div>
        <div className="flex items-center gap-2 mb-1">
          <span className="text-xs font-semibold text-brand-700 bg-brand-50 px-2.5 py-0.5 rounded-md border border-brand-200">
            AI Capability: analyze_business_model
          </span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
          Business Model & Unit Economics
        </h1>
        <p className="text-base text-slate-500 mt-1">
          Pricing architecture, revenue monetization streams, and calculated economics.
        </p>
      </div>

      <ProvenanceLegend />

      {bm && (
        <div className="space-y-8">
          {/* 1. Model Type Banner */}
          <div className="p-4 rounded-xl bg-purple-50/80 border border-purple-200 flex flex-wrap items-center justify-between gap-3">
            <div>
              <span className="text-xs font-bold uppercase tracking-wider text-purple-700 block">
                Primary Business Architecture
              </span>
              <span className="text-xl font-bold text-purple-950">{bm.type}</span>
            </div>
            <Badge variant="purple" size="md">
              High-Margin Software
            </Badge>
          </div>

          {/* 2. Unit Economics Cards with Sandbox Switcher */}
          <div className="space-y-4">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <div className="flex items-center gap-2">
                <Calculator className="w-5 h-5 text-purple-600" />
                <h2 className="text-xl font-bold text-slate-900">
                  Unit Economics & SaaS Metrics
                </h2>
              </div>

              <div className="flex items-center gap-3">
                <div className="flex items-center bg-slate-100 p-1 rounded-xl text-xs font-semibold border border-slate-200">
                  <button
                    onClick={() => setActiveTab('audited')}
                    className={`px-3 py-1.5 rounded-lg transition-all ${
                      activeTab === 'audited'
                        ? 'bg-white text-slate-900 shadow-xs'
                        : 'text-slate-500 hover:text-slate-800'
                    }`}
                  >
                    Audited Metrics
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
                    Sensitivity Sandbox
                  </button>
                </div>
                <ProvenanceBadge provenance="calculated" showLabel />
              </div>
            </div>

            {activeTab === 'audited' && ue ? (
              <>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
                  {/* LTV / CAC */}
                  <Card className="border-purple-200 bg-gradient-to-b from-white to-purple-50/30 shadow-xs">
                    <CardContent className="p-4">
                      <span className="text-xs font-bold uppercase text-slate-500 block">
                        LTV / CAC Ratio
                      </span>
                      <div className="text-2xl font-black text-purple-700 mt-1">
                        {ue.ltv_cac_ratio}x
                      </div>
                      <span className="text-[11px] text-emerald-700 font-semibold mt-1 inline-block">
                        ✓ Benchmark &gt; 3.0x
                      </span>
                    </CardContent>
                  </Card>

                  {/* CAC */}
                  <Card className="border-slate-200 shadow-xs">
                    <CardContent className="p-4">
                      <span className="text-xs font-bold uppercase text-slate-500 block">
                        Customer Acq Cost (CAC)
                      </span>
                      <div className="text-2xl font-black text-slate-900 mt-1">
                        ${ue.cac.toLocaleString()}
                      </div>
                      <span className="text-[11px] text-slate-500 mt-1 inline-block">
                        Blended across GTM
                      </span>
                    </CardContent>
                  </Card>

                  {/* LTV */}
                  <Card className="border-slate-200 shadow-xs">
                    <CardContent className="p-4">
                      <span className="text-xs font-bold uppercase text-slate-500 block">
                        Customer Lifetime (LTV)
                      </span>
                      <div className="text-2xl font-black text-slate-900 mt-1">
                        ${ue.ltv.toLocaleString()}
                      </div>
                      <span className="text-[11px] text-slate-500 mt-1 inline-block">
                        3-Year Horizon
                      </span>
                    </CardContent>
                  </Card>

                  {/* Payback */}
                  <Card className="border-slate-200 shadow-xs">
                    <CardContent className="p-4">
                      <span className="text-xs font-bold uppercase text-slate-500 block">
                        CAC Payback Period
                      </span>
                      <div className="text-2xl font-black text-slate-900 mt-1">
                        {ue.payback_months} mo
                      </div>
                      <span className="text-[11px] text-emerald-700 font-semibold mt-1 inline-block">
                        ✓ Target &lt; 12 mo
                      </span>
                    </CardContent>
                  </Card>

                  {/* Gross Margin */}
                  <Card className="border-slate-200 shadow-xs">
                    <CardContent className="p-4">
                      <span className="text-xs font-bold uppercase text-slate-500 block">
                        Gross Software Margin
                      </span>
                      <div className="text-2xl font-black text-emerald-600 mt-1">
                        {ue.gross_margin}%
                      </div>
                      <span className="text-[11px] text-slate-500 mt-1 inline-block">
                        Net Cloud Compute
                      </span>
                    </CardContent>
                  </Card>
                </div>

                {/* Mathematical Formula Breakdown */}
                <div className="p-4 rounded-xl bg-slate-50 border border-slate-200/80 text-xs text-slate-600 space-y-1.5">
                  <div className="font-bold text-slate-800 flex items-center gap-1.5 mb-1">
                    <span>🔢 Mathematical Calculation Formulas & Assumptions:</span>
                  </div>
                  {Object.entries(ue.formulas || {}).map(([key, formula]) => (
                    <div key={key} className="flex items-center gap-2 font-mono">
                      <span className="w-1.5 h-1.5 rounded-full bg-purple-500 shrink-0" />
                      <span className="font-semibold text-slate-700">{key}:</span>
                      <span className="text-slate-600">{formula}</span>
                    </div>
                  ))}
                </div>
              </>
            ) : (
              /* Sensitivity Sandbox Interactive View */
              <div className="space-y-6">
                <div className="p-4 rounded-xl bg-purple-50/70 border border-purple-200 flex flex-wrap items-center justify-between gap-2">
                  <span className="text-xs font-bold text-purple-900">
                    Adjust key levers below to test unit economics viability:
                  </span>
                  <Badge variant={currentBadge.variant} size="md">
                    {currentBadge.label}
                  </Badge>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 p-5 bg-slate-50 rounded-xl border border-slate-200">
                  <div>
                    <div className="flex justify-between text-xs font-bold text-slate-700 mb-1.5">
                      <span>CAC ($):</span>
                      <span className="text-brand-700 font-extrabold">${simCac.toLocaleString()}</span>
                    </div>
                    <input
                      type="range"
                      min="2000"
                      max="15000"
                      step="500"
                      value={simCac}
                      onChange={(e) => setSimCac(Number(e.target.value))}
                      className="w-full accent-brand-600 cursor-pointer"
                    />
                  </div>

                  <div>
                    <div className="flex justify-between text-xs font-bold text-slate-700 mb-1.5">
                      <span>Monthly ARPU ($):</span>
                      <span className="text-brand-700 font-extrabold">${simMonthlyArpu.toLocaleString()}</span>
                    </div>
                    <input
                      type="range"
                      min="500"
                      max="4000"
                      step="100"
                      value={simMonthlyArpu}
                      onChange={(e) => setSimMonthlyArpu(Number(e.target.value))}
                      className="w-full accent-brand-600 cursor-pointer"
                    />
                  </div>

                  <div>
                    <div className="flex justify-between text-xs font-bold text-slate-700 mb-1.5">
                      <span>Gross Margin (%):</span>
                      <span className="text-brand-700 font-extrabold">{simMargin}%</span>
                    </div>
                    <input
                      type="range"
                      min="65"
                      max="95"
                      step="0.5"
                      value={simMargin}
                      onChange={(e) => setSimMargin(Number(e.target.value))}
                      className="w-full accent-brand-600 cursor-pointer"
                    />
                  </div>

                  <div>
                    <div className="flex justify-between text-xs font-bold text-slate-700 mb-1.5">
                      <span>Monthly Churn (%):</span>
                      <span className="text-brand-700 font-extrabold">{simChurn}%</span>
                    </div>
                    <input
                      type="range"
                      min="0.5"
                      max="5.0"
                      step="0.1"
                      value={simChurn}
                      onChange={(e) => setSimChurn(Number(e.target.value))}
                      className="w-full accent-brand-600 cursor-pointer"
                    />
                  </div>
                </div>

                {/* Sandbox Results */}
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                  <div className="p-5 rounded-xl bg-purple-50 border border-purple-200">
                    <span className="text-xs font-bold uppercase text-purple-700 block">
                      Calculated LTV / CAC
                    </span>
                    <div className="text-3xl font-black text-purple-950 mt-1">
                      {simLtvCac}x
                    </div>
                    <span className="text-xs text-purple-700 font-medium mt-1 block">
                      LTV: ${simLtv.toLocaleString()}
                    </span>
                  </div>

                  <div className="p-5 rounded-xl bg-indigo-50 border border-indigo-200">
                    <span className="text-xs font-bold uppercase text-indigo-700 block">
                      Payback Period
                    </span>
                    <div className="text-3xl font-black text-indigo-950 mt-1">
                      {simPayback} mo
                    </div>
                    <span className="text-xs text-indigo-700 font-medium mt-1 block">
                      Target &lt; 12 months
                    </span>
                  </div>

                  <div className="p-5 rounded-xl bg-emerald-50 border border-emerald-200">
                    <span className="text-xs font-bold uppercase text-emerald-700 block">
                      Customer Retention
                    </span>
                    <div className="text-3xl font-black text-emerald-950 mt-1">
                      {simCustomerLifetimeMonths} mo
                    </div>
                    <span className="text-xs text-emerald-700 font-medium mt-1 block">
                      Lifetime based on {simChurn}% churn
                    </span>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* 3. Revenue Streams */}
          <div className="space-y-4">
            <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2">
              <CircleDollarSign className="w-5 h-5 text-emerald-600" />
              Monetization Streams
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {bm.revenue_streams.map((rev) => (
                <Card key={rev.name} className="hover:shadow-card-hover transition-all">
                  <CardHeader className="pb-2">
                    <CardTitle className="text-base font-bold">{rev.name}</CardTitle>
                    <ProvenanceBadge provenance={rev.provenance || 'founder_assumption'} />
                  </CardHeader>
                  <CardContent className="space-y-2 text-sm">
                    <div>
                      <span className="text-xs font-bold uppercase text-slate-400 block">Model</span>
                      <div className="font-medium text-slate-800">{rev.model_type}</div>
                    </div>
                    <div>
                      <span className="text-xs font-bold uppercase text-slate-400 block">Price Point</span>
                      <div className="text-base font-extrabold text-brand-700">{rev.price_point}</div>
                    </div>
                    <div className="flex items-center justify-between text-xs pt-2 border-t border-slate-100">
                      <span className="text-slate-500">Billing: {rev.frequency}</span>
                      <span className="font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded">
                        {rev.margin} Margin
                      </span>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>

          {/* 4. Pricing Tiers */}
          <div className="space-y-4">
            <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2">
              <Layers className="w-5 h-5 text-indigo-600" />
              Packaging & Pricing Tiers
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {bm.pricing_tiers.map((tier, idx) => (
                <Card
                  key={tier.tier_name}
                  className={`flex flex-col justify-between ${
                    idx === 1
                      ? 'border-brand-500 ring-2 ring-brand-200 shadow-md relative'
                      : 'shadow-xs'
                  }`}
                >
                  {idx === 1 && (
                    <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-brand-600 text-white px-3 py-0.5 rounded-full text-xs font-bold uppercase tracking-wider shadow-sm">
                      Recommended
                    </div>
                  )}
                  <CardContent className="p-6">
                    <div className="text-lg font-bold text-slate-900 mb-1">
                      {tier.tier_name}
                    </div>
                    <div className="text-2xl font-extrabold text-slate-900 mb-1">
                      {tier.price}
                    </div>
                    <div className="text-xs text-slate-500 mb-4">{tier.billing}</div>

                    <div className="text-xs text-slate-500 mb-4 p-2.5 bg-slate-50 rounded-lg">
                      <span className="font-semibold text-slate-700">Target: </span>
                      {tier.target_audience}
                    </div>

                    <ul className="space-y-2 text-xs text-slate-700">
                      {(tier.features || []).map((feat, i) => (
                        <li key={i} className="flex items-start gap-2">
                          <Check className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                          <span>{feat}</span>
                        </li>
                      ))}
                    </ul>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
