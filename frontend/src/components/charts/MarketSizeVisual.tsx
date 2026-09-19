import React from 'react';
import { MarketTier } from '../../types/capabilities';
import { ProvenanceBadge } from '../provenance/ProvenanceBadge';
import { ExternalLink } from 'lucide-react';

interface MarketSizeVisualProps {
  tam: MarketTier;
  sam: MarketTier;
  som: MarketTier;
}

export const MarketSizeVisual: React.FC<MarketSizeVisualProps> = ({ tam, sam, som }) => {
  const tiers = {
    tam: {
      ...tam,
      calculation_steps: tam.calculation_steps || [],
      sources: tam.sources || [],
    },
    sam: {
      ...sam,
      calculation_steps: sam.calculation_steps || [],
      sources: sam.sources || [],
    },
    som: {
      ...som,
      calculation_steps: som.calculation_steps || [],
      sources: som.sources || [],
    },
  };

  return (
    <div className="space-y-6">
      {/* Tiered Nested Cards */}
      <div className="space-y-4">
        {/* TAM */}
        <div className="p-5 rounded-2xl bg-gradient-to-r from-blue-50 to-indigo-50/60 border border-blue-200">
          <div className="flex flex-wrap items-center justify-between gap-2 mb-2">
            <div className="flex items-center gap-3">
              <span className="px-2.5 py-1 rounded-md bg-blue-600 text-white font-bold text-xs tracking-wider uppercase">
                Total Addressable Market (TAM)
              </span>
              <span className="text-2xl sm:text-3xl font-extrabold text-blue-950">
                {tiers.tam.formatted}
              </span>
            </div>
            <ProvenanceBadge provenance={tiers.tam.provenance} showLabel />
          </div>
          <p className="text-sm font-medium text-blue-900 mb-3">{tiers.tam.description}</p>
          <div className="p-3 bg-white/80 rounded-xl text-xs space-y-1 text-slate-600 border border-blue-100">
            <div className="font-semibold text-slate-700">Calculation Baseline:</div>
            {tiers.tam.calculation_steps.map((step, i) => (
              <div key={i} className="flex items-center gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-blue-500 shrink-0" />
                <span>{step}</span>
              </div>
            ))}
            {tiers.tam.sources.length > 0 && (
              <div className="pt-2 mt-2 border-t border-slate-100 flex flex-wrap items-center gap-2 text-blue-700">
                <span className="font-semibold">Sources:</span>
                {tiers.tam.sources.map((src, i) => (
                  <span key={i} className="inline-flex items-center gap-1 bg-blue-50 px-2 py-0.5 rounded text-[11px]">
                    {src} <ExternalLink className="w-3 h-3" />
                  </span>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* SAM */}
        <div className="p-5 rounded-2xl bg-gradient-to-r from-indigo-50 to-purple-50/60 border border-indigo-200 ml-0 sm:ml-4">
          <div className="flex flex-wrap items-center justify-between gap-2 mb-2">
            <div className="flex items-center gap-3">
              <span className="px-2.5 py-1 rounded-md bg-indigo-600 text-white font-bold text-xs tracking-wider uppercase">
                Serviceable Addressable Market (SAM)
              </span>
              <span className="text-2xl sm:text-3xl font-extrabold text-indigo-950">
                {tiers.sam.formatted}
              </span>
            </div>
            <ProvenanceBadge provenance={tiers.sam.provenance} showLabel />
          </div>
          <p className="text-sm font-medium text-indigo-900 mb-3">{tiers.sam.description}</p>
          <div className="p-3 bg-white/80 rounded-xl text-xs space-y-1 text-slate-600 border border-indigo-100">
            <div className="font-semibold text-slate-700">Calculation Baseline:</div>
            {tiers.sam.calculation_steps.map((step, i) => (
              <div key={i} className="flex items-center gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-indigo-500 shrink-0" />
                <span>{step}</span>
              </div>
            ))}
            {tiers.sam.sources.length > 0 && (
              <div className="pt-2 mt-2 border-t border-slate-100 flex flex-wrap items-center gap-2 text-indigo-700">
                <span className="font-semibold">Sources:</span>
                {tiers.sam.sources.map((src, i) => (
                  <span key={i} className="inline-flex items-center gap-1 bg-indigo-50 px-2 py-0.5 rounded text-[11px]">
                    {src} <ExternalLink className="w-3 h-3" />
                  </span>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* SOM */}
        <div className="p-5 rounded-2xl bg-gradient-to-r from-emerald-50 to-teal-50/60 border border-emerald-200 ml-0 sm:ml-8">
          <div className="flex flex-wrap items-center justify-between gap-2 mb-2">
            <div className="flex items-center gap-3">
              <span className="px-2.5 py-1 rounded-md bg-emerald-600 text-white font-bold text-xs tracking-wider uppercase">
                Serviceable Obtainable Market (SOM)
              </span>
              <span className="text-2xl sm:text-3xl font-extrabold text-emerald-950">
                {tiers.som.formatted}
              </span>
            </div>
            <ProvenanceBadge provenance={tiers.som.provenance} showLabel />
          </div>
          <p className="text-sm font-medium text-emerald-900 mb-3">{tiers.som.description}</p>
          <div className="p-3 bg-white/80 rounded-xl text-xs space-y-1 text-slate-600 border border-emerald-100">
            <div className="font-semibold text-slate-700">Bottoms-up Beachhead Calculation:</div>
            {tiers.som.calculation_steps.map((step, i) => (
              <div key={i} className="flex items-center gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 shrink-0" />
                <span>{step}</span>
              </div>
            ))}
            {tiers.som.sources.length > 0 && (
              <div className="pt-2 mt-2 border-t border-slate-100 flex flex-wrap items-center gap-2 text-emerald-700">
                <span className="font-semibold">Sources:</span>
                {tiers.som.sources.map((src, i) => (
                  <span key={i} className="inline-flex items-center gap-1 bg-emerald-50 px-2 py-0.5 rounded text-[11px]">
                    {src} <ExternalLink className="w-3 h-3" />
                  </span>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
