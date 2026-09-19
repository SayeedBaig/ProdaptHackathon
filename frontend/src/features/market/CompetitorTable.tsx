import React, { useState } from 'react';
import { CompetitorDetail } from '../../types/capabilities';
import { ProvenanceBadge } from '../../components/provenance/ProvenanceBadge';
import { ExternalLink, Check, X, Search } from 'lucide-react';

interface CompetitorTableProps {
  competitors: CompetitorDetail[];
}

export const CompetitorTable: React.FC<CompetitorTableProps> = ({ competitors }) => {
  const [searchQuery, setSearchQuery] = useState('');

  const filtered = competitors.filter((c) => {
    const q = searchQuery.toLowerCase();
    return (
      c.name.toLowerCase().includes(q) ||
      c.description.toLowerCase().includes(q) ||
      c.differentiator.toLowerCase().includes(q)
    );
  });

  return (
    <div className="space-y-3">
      {/* Search Filter */}
      <div className="flex items-center justify-between gap-4">
        <div className="relative w-full max-w-xs">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Filter competitors..."
            className="w-full pl-9 pr-3 py-1.5 text-xs bg-white border border-slate-200 rounded-lg focus:ring-2 focus:ring-brand-500 outline-none"
          />
        </div>
        <span className="text-xs text-slate-500 font-medium">
          Showing {filtered.length} of {competitors.length} competitors
        </span>
      </div>

      <div className="overflow-x-auto rounded-xl border border-slate-200 shadow-sm bg-white">
        <table className="w-full text-left text-sm border-collapse">
          <thead>
            <tr className="bg-slate-50/90 border-b border-slate-200 text-slate-700 font-bold text-xs uppercase tracking-wider">
              <th className="p-4">Competitor</th>
              <th className="p-4">Market Share & Pricing</th>
              <th className="p-4">Strengths</th>
              <th className="p-4">Weaknesses / Vulnerabilities</th>
              <th className="p-4">Our Key Differentiator</th>
              <th className="p-4 text-center">Provenance</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {filtered.map((comp) => (
              <tr key={comp.name} className="hover:bg-slate-50/50 transition-colors">
                <td className="p-4 font-semibold text-slate-900 align-top">
                  <div className="text-base font-bold text-slate-900">{comp.name}</div>
                  <div className="text-xs text-slate-500 mt-1 max-w-xs leading-snug">
                    {comp.description}
                  </div>
                  {comp.source_urls && comp.source_urls.length > 0 && (
                    <div className="mt-2 flex items-center gap-1">
                      <a
                        href={comp.source_urls[0]}
                        target="_blank"
                        rel="noreferrer"
                        className="text-[11px] text-brand-600 hover:underline inline-flex items-center gap-0.5 font-medium"
                      >
                        Audit Link <ExternalLink className="w-2.5 h-2.5" />
                      </a>
                    </div>
                  )}
                </td>

                <td className="p-4 align-top">
                  <div className="font-semibold text-slate-800">{comp.pricing}</div>
                  <div className="text-xs text-slate-500 mt-1">
                    Share: <span className="font-medium text-slate-700">{comp.market_share}</span>
                  </div>
                </td>

                <td className="p-4 align-top">
                  <ul className="space-y-1 text-xs text-slate-600">
                    {comp.strengths.map((st, i) => (
                      <li key={i} className="flex items-start gap-1.5">
                        <Check className="w-3.5 h-3.5 text-emerald-600 shrink-0 mt-0.5" />
                        <span>{st}</span>
                      </li>
                    ))}
                  </ul>
                </td>

                <td className="p-4 align-top">
                  <ul className="space-y-1 text-xs text-slate-600">
                    {comp.weaknesses.map((wk, i) => (
                      <li key={i} className="flex items-start gap-1.5">
                        <X className="w-3.5 h-3.5 text-rose-500 shrink-0 mt-0.5" />
                        <span>{wk}</span>
                      </li>
                    ))}
                  </ul>
                </td>

                <td className="p-4 align-top">
                  <div className="p-2.5 rounded-lg bg-brand-50/80 border border-brand-100 text-xs font-medium text-brand-900 leading-snug">
                    {comp.differentiator}
                  </div>
                </td>

                <td className="p-4 align-top text-center">
                  <ProvenanceBadge provenance={comp.provenance} />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
