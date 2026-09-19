import React, { useState } from 'react';
import { useUiStore } from '../../store/uiStore';
import { useAuthStore } from '../../store/authStore';
import { Badge } from '../ui/Badge';
import { Button } from '../ui/Button';
import { mockStore } from '../../mocks/mockStore';
import { useQueryClient } from '@tanstack/react-query';
import { toast } from 'sonner';
import { Sparkles, LogOut, Rocket, Menu, Bug, Award } from 'lucide-react';
import { Link } from 'react-router-dom';

interface WorkspaceHeaderProps {
  startupName?: string;
}

export const WorkspaceHeader: React.FC<WorkspaceHeaderProps> = ({
  startupName = 'HyperScale AI',
}) => {
  const queryClient = useQueryClient();
  const aiMode = useUiStore((state) => state.aiMode);
  const profileVersion = useUiStore((state) => state.profileVersion);
  const toggleSidebar = useUiStore((state) => state.toggleSidebar);
  const user = useAuthStore((state) => state.user);
  const logout = useAuthStore((state) => state.logout);

  const [currentMockError, setCurrentMockError] = useState(() => {
    if (typeof window !== 'undefined') {
      const p = new URLSearchParams(window.location.search);
      return p.get('mock_error') || 'NONE';
    }
    return 'NONE';
  });

  const handleResetSampleStartup = () => {
    mockStore.resetToSample();
    queryClient.invalidateQueries();
    toast.success('Workspace reset to sample startup!', {
      description: 'Loaded HyperScale AI with all 12 slides, profile, and feedback.',
    });
  };

  const handleSimulateError = (code: string) => {
    const url = new URL(window.location.href);
    if (code === 'NONE') {
      url.searchParams.delete('mock_error');
    } else {
      url.searchParams.set('mock_error', code);
    }
    window.history.pushState({}, '', url.toString());
    setCurrentMockError(code);
    window.location.reload();
  };

  const aiModeLabels = {
    live: { label: 'Live AI', variant: 'success' as const, dot: 'bg-emerald-500' },
    fallback_provider: { label: 'Backup Model', variant: 'warning' as const, dot: 'bg-amber-500' },
    mock: { label: 'Demo Data', variant: 'purple' as const, dot: 'bg-purple-500' },
  };

  const currentModeInfo = aiModeLabels[aiMode] || aiModeLabels.mock;

  return (
    <header className="h-16 bg-white/95 backdrop-blur-md border-b border-slate-200/80 px-4 sm:px-6 flex items-center justify-between sticky top-0 z-20 shadow-xs">
      {/* Left: Mobile menu & Brand/Startup info */}
      <div className="flex items-center gap-3">
        <button
          onClick={toggleSidebar}
          className="md:hidden p-2 text-slate-500 hover:text-slate-800 hover:bg-slate-100 rounded-lg"
          aria-label="Toggle navigation menu"
        >
          <Menu className="w-5 h-5" />
        </button>

        <Link to="/" className="flex items-center gap-2.5 group">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-brand-700 via-indigo-600 to-violet-500 flex items-center justify-center text-white font-bold shadow-md shadow-brand-500/20 group-hover:scale-105 transition-transform">
            <Rocket className="w-4 h-4" />
          </div>
          <span className="font-extrabold text-xl tracking-tight text-slate-900 hidden sm:inline">
            PitchPilot
          </span>
        </Link>

        <span className="text-slate-300 hidden sm:inline">/</span>

        <div className="flex items-center gap-2">
          <h2 className="text-base font-bold text-slate-800 truncate max-w-[180px] md:max-w-xs">
            {startupName}
          </h2>
          <Badge variant="default" size="sm" title="Active Startup Profile Version">
            v{profileVersion}
          </Badge>
        </div>

        {/* Live Pitch Readiness Pill */}
        <Link
          to="/readiness-report"
          className="hidden lg:flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs font-semibold hover:bg-emerald-100 transition-colors shadow-2xs"
          title="Overall Investor Readiness Index. Click to view full report."
        >
          <Award className="w-3.5 h-3.5 text-emerald-600" />
          <span>Readiness: <strong className="font-extrabold text-emerald-950">82/100</strong></span>
        </Link>
      </div>

      {/* Right: Error simulator, Mode badge, Demo Safety Net button, User info */}
      <div className="flex items-center gap-3">
        {/* Dev Error Simulator Dropdown */}
        <div className="hidden xl:flex items-center gap-1.5 text-xs text-slate-500 bg-slate-100/80 px-2 py-1 rounded-lg border border-slate-200">
          <Bug className="w-3.5 h-3.5 text-slate-600" />
          <span className="font-semibold text-slate-700">Simulate Error:</span>
          <select
            value={currentMockError}
            onChange={(e) => handleSimulateError(e.target.value)}
            className="bg-transparent font-medium text-slate-800 outline-none cursor-pointer text-xs"
          >
            <option value="NONE">None (Healthy)</option>
            <option value="LLM_UNAVAILABLE">503 LLM_UNAVAILABLE</option>
            <option value="LLM_INVALID_OUTPUT">502 LLM_INVALID_OUTPUT</option>
            <option value="VERSION_CONFLICT">409 VERSION_CONFLICT</option>
            <option value="SESSION_CLOSED">409 SESSION_CLOSED</option>
            <option value="RATE_LIMITED">429 RATE_LIMITED</option>
            <option value="VALIDATION_ERROR">422 VALIDATION_ERROR</option>
          </select>
        </div>

        {/* AI Mode Badge */}
        <div className="flex items-center gap-1.5" title={`Current AI Engine Mode: ${aiMode}`}>
          <span className={`w-2 h-2 rounded-full ${currentModeInfo.dot} animate-pulse`} />
          <Badge variant={currentModeInfo.variant} size="sm">
            {currentModeInfo.label}
          </Badge>
        </div>

        {/* Demo Safety Net: Load Sample Startup */}
        <Button
          variant="outline"
          size="sm"
          onClick={handleResetSampleStartup}
          leftIcon={<Sparkles className="w-3.5 h-3.5 text-brand-600" />}
          className="text-xs hidden md:inline-flex border-brand-200 bg-brand-50/50 hover:bg-brand-100/50 text-brand-800 font-medium"
          title="Instantly fills the workspace with complete sample data if wifi or backend fails"
        >
          Load sample startup
        </Button>

        {/* User / Logout */}
        {user && (
          <div className="flex items-center gap-2 pl-2 border-l border-slate-200">
            <div className="hidden lg:block text-right">
              <div className="text-xs font-semibold text-slate-800 leading-tight">
                {user.name}
              </div>
              <div className="text-[11px] text-slate-500 leading-tight">
                {user.email}
              </div>
            </div>
            <button
              onClick={logout}
              className="p-1.5 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-lg transition-colors"
              title="Sign Out"
              aria-label="Sign out"
            >
              <LogOut className="w-4 h-4" />
            </button>
          </div>
        )}
      </div>
    </header>
  );
};
