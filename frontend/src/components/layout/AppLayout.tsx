import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { WorkspaceHeader } from './WorkspaceHeader';
import { SidebarStepper } from './SidebarStepper';
import { DegradedBanner } from './DegradedBanner';
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '../../api/client';
import { ENDPOINTS } from '../../api/endpoints';
import { Profile } from '../../types/profile';
import { useUiStore } from '../../store/uiStore';

export const AppLayout: React.FC = () => {
  const currentStartupId = useUiStore((state) => state.currentStartupId);
  const isMock = import.meta.env.VITE_USE_MOCKS === 'true';
  const effectiveStartupId = currentStartupId || (isMock ? 'hyperscale-ai-001' : null);

  // Fetch startup profile to keep header and version synced
  const { data: profileEnvelope } = useQuery({
    queryKey: ['profile', effectiveStartupId],
    queryFn: () => apiClient<Profile>(ENDPOINTS.PROFILE_GET(effectiveStartupId!)),
    staleTime: 30000,
    enabled: !!effectiveStartupId,
  });

  if (!effectiveStartupId) {
    return <Navigate to="/startups" replace />;
  }

  const startupName = profileEnvelope?.data?.identity?.startup_name || 'Current Startup';
  const warnings = profileEnvelope?.meta?.warnings || [];

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 text-slate-900">
      <DegradedBanner warnings={warnings} />
      <WorkspaceHeader startupName={startupName} />

      <div className="flex-1 flex max-w-7xl w-full mx-auto">
        <SidebarStepper />

        <main className="flex-1 min-w-0 p-4 sm:p-6 lg:p-8">
          <Outlet />
        </main>
      </div>
    </div>
  );
};
