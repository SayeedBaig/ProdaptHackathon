import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  FileText,
  Zap,
  TrendingUp,
  CircleDollarSign,
  Presentation,
  MessageSquareQuote,
  Bot,
  Award,
  Sparkles,
  ChevronRight,
} from 'lucide-react';
import { useUiStore } from '../../store/uiStore';

const STEP_ITEMS = [
  {
    path: '/',
    title: '1. Overview & Profile',
    desc: 'Idea analysis, profile, and clarification',
    icon: Sparkles,
  },
  {
    path: '/value-prop',
    title: '2. Value Proposition',
    desc: 'One-liner, elevator pitch & advantage',
    icon: Zap,
  },
  {
    path: '/market',
    title: '3. Market & Competition',
    desc: 'TAM/SAM/SOM & competitor landscape',
    icon: TrendingUp,
  },
  {
    path: '/business-model',
    title: '4. Business Model',
    desc: 'Revenue streams & unit economics',
    icon: CircleDollarSign,
  },
  {
    path: '/pitch-deck',
    title: '5. Pitch Deck',
    desc: '12-slide deck & PPTX export',
    icon: Presentation,
  },
  {
    path: '/feedback',
    title: '6. Feedback',
    desc: 'Critiques, triage & profile patches',
    icon: MessageSquareQuote,
  },
  {
    path: '/investor-practice',
    title: '7. Investor Practice',
    desc: 'Interactive Q&A & radar scoring',
    icon: Bot,
  },
  {
    path: '/readiness-report',
    title: '8. Readiness Report',
    desc: 'Executive summary & scorecard',
    icon: Award,
  },
];

export const SidebarStepper: React.FC = () => {
  const sidebarOpen = useUiStore((state) => state.sidebarOpen);

  return (
    <aside
      className={`fixed md:sticky top-16 z-30 h-[calc(100vh-4rem)] w-72 bg-white border-r border-slate-200/80 transition-transform duration-200 ease-in-out shrink-0 overflow-y-auto ${
        sidebarOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'
      }`}
    >
      <div className="p-4 space-y-1">
        <div className="px-3 py-2 text-xs font-bold uppercase tracking-wider text-slate-400">
          Startup Readiness Journey
        </div>

        {STEP_ITEMS.map((step) => {
          const Icon = step.icon;
          return (
            <NavLink
              key={step.path}
              to={step.path}
              end={step.path === '/'}
              className={({ isActive }) =>
                `flex items-center justify-between p-3 rounded-xl text-sm transition-all duration-150 group ${
                  isActive
                    ? 'bg-brand-50 text-brand-900 font-semibold shadow-xs border border-brand-200/60'
                    : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
                }`
              }
            >
              {({ isActive }) => (
                <>
                  <div className="flex items-center gap-3">
                    <div
                      className={`p-2 rounded-lg transition-colors ${
                        isActive
                          ? 'bg-brand-600 text-white shadow-xs'
                          : 'bg-slate-100 text-slate-500 group-hover:bg-slate-200 group-hover:text-slate-800'
                      }`}
                    >
                      <Icon className="w-4 h-4" />
                    </div>
                    <div>
                      <div className="leading-tight">{step.title}</div>
                      <div className="text-[11px] text-slate-400 font-normal leading-tight mt-0.5">
                        {step.desc}
                      </div>
                    </div>
                  </div>
                  <ChevronRight
                    className={`w-4 h-4 transition-transform ${
                      isActive
                        ? 'text-brand-600 translate-x-0.5'
                        : 'text-slate-300 opacity-0 group-hover:opacity-100'
                    }`}
                  />
                </>
              )}
            </NavLink>
          );
        })}
      </div>
    </aside>
  );
};
