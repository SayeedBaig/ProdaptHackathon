import React from 'react';
import { CompetitorPosition } from '../../types/capabilities';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Compass } from 'lucide-react';

interface CompetitorMatrix2x2Props {
  axes: { x_axis: string; y_axis: string };
  positions: CompetitorPosition[];
}

export const CompetitorMatrix2x2: React.FC<CompetitorMatrix2x2Props> = ({
  axes,
  positions,
}) => {
  return (
    <Card>
      <CardHeader>
        <div className="flex items-center gap-2">
          <Compass className="w-5 h-5 text-brand-600" />
          <CardTitle>Strategic 2x2 Competitive Positioning</CardTitle>
        </div>
      </CardHeader>
      <CardContent>
        <div className="relative w-full aspect-video max-h-96 bg-slate-50 rounded-xl border border-slate-200 p-8 flex flex-col justify-center items-center select-none overflow-hidden">
          {/* Grid lines */}
          <div className="absolute inset-x-8 top-1/2 border-t-2 border-dashed border-slate-300 -translate-y-1/2" />
          <div className="absolute inset-y-8 left-1/2 border-l-2 border-dashed border-slate-300 -translate-x-1/2" />

          {/* Axis Labels */}
          {/* Top Y */}
          <div className="absolute top-2 inset-x-0 text-center text-xs font-bold text-slate-600 uppercase tracking-wider">
            ↑ {axes.y_axis.split('→')[1] || 'Granular Pod/Workload Level'}
          </div>
          {/* Bottom Y */}
          <div className="absolute bottom-2 inset-x-0 text-center text-xs font-semibold text-slate-400 uppercase tracking-wider">
            ↓ {axes.y_axis.split('→')[0] || 'Node & VM Level'}
          </div>
          {/* Left X */}
          <div className="absolute left-2 inset-y-0 flex items-center text-xs font-semibold text-slate-400 uppercase tracking-wider [writing-mode:vertical-lr] rotate-180">
            ← {axes.x_axis.split('→')[0] || 'Passive Reporting'}
          </div>
          {/* Right X */}
          <div className="absolute right-2 inset-y-0 flex items-center text-xs font-bold text-brand-700 uppercase tracking-wider [writing-mode:vertical-lr]">
            {axes.x_axis.split('→')[1] || 'Autonomous Closed-Loop Action'} →
          </div>

          {/* Competitor Nodes */}
          {positions.map((pos) => {
            // Coordinate mapping: x from -10 to 10 mapped to 15% to 85%
            const leftPct = ((pos.x + 10) / 20) * 70 + 15;
            // y from -10 to 10 inverted (positive y is up) mapped to 85% to 15%
            const topPct = ((-pos.y + 10) / 20) * 70 + 15;

            return (
              <div
                key={pos.name}
                style={{ left: `${leftPct}%`, top: `${topPct}%` }}
                className={`absolute -translate-x-1/2 -translate-y-1/2 flex flex-col items-center group transition-transform ${
                  pos.is_self ? 'scale-110 z-10' : ''
                }`}
              >
                <div
                  className={`w-6 h-6 rounded-full flex items-center justify-center font-bold text-xs shadow-md transition-all ${
                    pos.is_self
                      ? 'bg-brand-600 text-white ring-4 ring-brand-200 animate-pulse'
                      : 'bg-slate-700 text-white'
                  }`}
                >
                  {pos.name.charAt(0)}
                </div>
                <span
                  className={`mt-1 text-xs font-bold px-2 py-0.5 rounded shadow-xs whitespace-nowrap ${
                    pos.is_self
                      ? 'bg-brand-600 text-white'
                      : 'bg-white text-slate-800 border border-slate-200'
                  }`}
                >
                  {pos.name} {pos.is_self && '(You)'}
                </span>
              </div>
            );
          })}
        </div>
      </CardContent>
    </Card>
  );
};
