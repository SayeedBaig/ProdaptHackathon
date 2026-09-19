import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '../../api/client';
import { ENDPOINTS } from '../../api/endpoints';
import { ReadinessNarrative } from '../../types/capabilities';
import { useUiStore } from '../../store/uiStore';
import { CriteriaRadarChart } from '../../components/charts/CriteriaRadarChart';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { AiLoadingState } from '../../components/ui/Skeleton';
import { TOPIC_LABELS, Topic } from '../../types/contracts';
import {
  Award,
  Printer,
  CheckCircle2,
  AlertTriangle,
  FileCheck,
  TrendingUp,
  ShieldCheck,
  Calendar,
  CheckSquare,
  Square,
  Sparkles,
} from 'lucide-react';

const INITIAL_CHECKLIST = [
  { id: 'chk-1', text: '12-Slide Presentation Deck complete and exported to PPTX', checked: true },
  { id: 'chk-2', text: 'TAM/SAM/SOM audited calculation methodology documented', checked: true },
  { id: 'chk-3', text: 'Unit economics audited (LTV/CAC 6.19x > 3.0x benchmark)', checked: true },
  { id: 'chk-4', text: '8 active production pilot references documented with 0 SLA downtime', checked: true },
  { id: 'chk-5', text: 'Convert top 3 pilot customers to binding paid LOIs with committed ARR', checked: false },
  { id: 'chk-6', text: 'Publish enterprise SOC2 Type II compliance audit schedule', checked: false },
];

export const ReadinessReportPage: React.FC = () => {
  const startupId = useUiStore((state) => state.currentStartupId) || 'hyperscale-ai-001';
  const [checklist, setChecklist] = useState(INITIAL_CHECKLIST);

  const { data: envelope, isLoading } = useQuery({
    queryKey: ['readiness_narrative', startupId],
    queryFn: () =>
      apiClient<ReadinessNarrative>(ENDPOINTS.AI_GENERATE_READINESS_NARRATIVE, {
        method: 'POST',
        body: { startup_id: startupId },
      }),
  });

  const handlePrint = () => {
    window.print();
  };

  const handleToggleCheck = (id: string) => {
    setChecklist((prev) =>
      prev.map((item) =>
        item.id === id ? { ...item, checked: !item.checked } : item
      )
    );
  };

  if (isLoading) {
    return (
      <AiLoadingState
        message="Synthesizing Investor Readiness Narrative..."
        subtext="Aggregating practice scores, pitch deck critique, and diligence gaps into an institutional report (10-30s)..."
      />
    );
  }

  const report = envelope?.data;
  const completedChecks = checklist.filter((c) => c.checked).length;

  return (
    <div className="space-y-8 pb-20 print:p-0 print:space-y-4">
      {/* Action Header - Hidden during print */}
      <div className="flex flex-wrap items-center justify-between gap-4 print:hidden">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="text-xs font-semibold text-brand-700 bg-brand-50 px-2.5 py-0.5 rounded-md border border-brand-200">
              AI Capability: generate_readiness_narrative
            </span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
            Investor Readiness Diligence Report
          </h1>
          <p className="text-base text-slate-500 mt-1">
            Comprehensive scorecard, aggregate criteria radar, and priority action items.
          </p>
        </div>

        <Button
          variant="outline"
          onClick={handlePrint}
          leftIcon={<Printer className="w-4 h-4 text-slate-700" />}
          className="shadow-sm"
        >
          Print / Export PDF
        </Button>
      </div>

      {report && (
        <div className="space-y-6">
          {/* 1. Executive Summary & Verdict Card */}
          <Card className="border-brand-200 bg-gradient-to-r from-brand-50/50 via-white to-indigo-50/50 shadow-md relative overflow-hidden">
            <div className="absolute top-0 right-0 w-80 h-80 bg-brand-200/20 rounded-full blur-3xl pointer-events-none" />

            <CardContent className="p-6 sm:p-8 relative z-10">
              <div className="flex flex-wrap items-center justify-between gap-4 pb-6 border-b border-slate-200/80 mb-6">
                <div>
                  <span className="text-xs font-bold uppercase tracking-wider text-slate-400 block mb-1">
                    Evaluation Target
                  </span>
                  <h2 className="text-2xl font-black text-slate-900">
                    HyperScale AI — Series Seed Pitch
                  </h2>
                  <div className="text-xs text-slate-500 flex items-center gap-2 mt-1">
                    <Calendar className="w-3.5 h-3.5" />
                    Generated {new Date().toLocaleDateString()} by PitchPilot Coach
                  </div>
                </div>

                <div className="flex items-center gap-4">
                  <div className="text-right">
                    <span className="text-xs font-bold uppercase tracking-wider text-slate-400 block">
                      Readiness Index
                    </span>
                    <span className="text-4xl font-black text-brand-700">
                      {report.overall_score}
                      <span className="text-lg text-slate-400">/100</span>
                    </span>
                  </div>

                  <div className="p-3 bg-white rounded-2xl border border-brand-200 shadow-sm flex flex-col items-center">
                    <Award className="w-6 h-6 text-brand-600 mb-1" />
                    <span className="text-[11px] font-extrabold uppercase tracking-wider text-brand-900 text-center">
                      {report.verdict}
                    </span>
                  </div>
                </div>
              </div>

              <div>
                <span className="text-xs font-bold uppercase tracking-wider text-slate-500 block mb-2">
                  Executive Diligence Summary
                </span>
                <p className="text-base text-slate-800 leading-relaxed">
                  {report.executive_summary}
                </p>
              </div>

              <div className="mt-4 p-4 rounded-xl bg-white border border-brand-200 text-sm font-medium text-brand-950">
                <span className="font-bold text-brand-900 block mb-0.5">
                  Partner Committee Verdict:
                </span>
                {report.investor_verdict}
              </div>
            </CardContent>
          </Card>

          {/* 2. Radar Chart & Topic Coverage 2-col Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Radar */}
            <Card>
              <CardHeader>
                <div className="flex items-center gap-2">
                  <Award className="w-5 h-5 text-brand-600" />
                  <CardTitle>Aggregate Diligence Radar (6 Criteria)</CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                <CriteriaRadarChart scores={report.criteria_scores} height={300} />
              </CardContent>
            </Card>

            {/* Topic Coverage */}
            <Card>
              <CardHeader>
                <div className="flex items-center gap-2">
                  <TrendingUp className="w-5 h-5 text-indigo-600" />
                  <CardTitle>Diligence Topic Coverage & Robustness</CardTitle>
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                {(Object.keys(report.topic_coverage) as Topic[]).map((topic) => {
                  const val = report.topic_coverage[topic];
                  return (
                    <div key={topic} className="space-y-1">
                      <div className="flex items-center justify-between text-xs font-bold">
                        <span className="text-slate-700">{TOPIC_LABELS[topic] || topic}</span>
                        <span className="text-brand-700">{val}% Prepared</span>
                      </div>
                      <div className="w-full h-2.5 rounded-full bg-slate-100 overflow-hidden">
                        <div
                          style={{ width: `${val}%` }}
                          className="h-full bg-brand-600 rounded-full transition-all duration-500"
                        />
                      </div>
                    </div>
                  );
                })}
              </CardContent>
            </Card>
          </div>

          {/* 3. Strengths & Critical Gaps */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="w-5 h-5 text-emerald-600" />
                  <CardTitle>Key Diligence Strengths</CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2.5 text-sm text-slate-800">
                  {report.top_strengths.map((st, i) => (
                    <li key={i} className="flex items-start gap-2.5">
                      <span className="w-2 h-2 rounded-full bg-emerald-500 shrink-0 mt-2" />
                      <span className="leading-snug font-medium">{st}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <div className="flex items-center gap-2">
                  <AlertTriangle className="w-5 h-5 text-amber-500" />
                  <CardTitle>Critical Diligence Gaps to Resolve</CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2.5 text-sm text-slate-800">
                  {report.critical_gaps.map((gap, i) => (
                    <li key={i} className="flex items-start gap-2.5">
                      <span className="w-2 h-2 rounded-full bg-amber-500 shrink-0 mt-2" />
                      <span className="leading-snug font-medium">{gap}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          </div>

          {/* 4. Interactive Pre-Pitch Diligence Checklist */}
          <Card>
            <CardHeader>
              <div className="flex items-center gap-2">
                <CheckSquare className="w-5 h-5 text-brand-600" />
                <CardTitle>
                  Pre-Meeting Diligence Checklist ({completedChecks}/{checklist.length} Completed)
                </CardTitle>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-2.5">
                {checklist.map((item) => (
                  <button
                    key={item.id}
                    onClick={() => handleToggleCheck(item.id)}
                    className={`w-full text-left p-3.5 rounded-xl border transition-all flex items-center gap-3 ${
                      item.checked
                        ? 'bg-emerald-50/50 border-emerald-200 text-slate-800'
                        : 'bg-white border-slate-200 text-slate-600 hover:bg-slate-50'
                    }`}
                  >
                    {item.checked ? (
                      <CheckCircle2 className="w-5 h-5 text-emerald-600 shrink-0" />
                    ) : (
                      <Square className="w-5 h-5 text-slate-300 shrink-0" />
                    )}
                    <span className={`text-sm font-medium ${item.checked ? 'line-through text-slate-500' : ''}`}>
                      {item.text}
                    </span>
                  </button>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* 5. Priority Action Plan */}
          <Card className="border-slate-300">
            <CardHeader>
              <div className="flex items-center gap-2">
                <FileCheck className="w-5 h-5 text-brand-600" />
                <CardTitle>Prioritized Pre-Pitch Action Plan</CardTitle>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {report.action_items.map((act, i) => (
                  <div
                    key={i}
                    className="p-3.5 rounded-xl bg-slate-50 border border-slate-200 flex items-start gap-3 text-sm text-slate-800 font-medium"
                  >
                    <span className="w-5 h-5 rounded-full bg-slate-900 text-white flex items-center justify-center text-xs font-bold shrink-0 mt-0.5">
                      {i + 1}
                    </span>
                    <span className="leading-snug">{act}</span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
};
