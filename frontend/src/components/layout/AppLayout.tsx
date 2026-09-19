import React from 'react';
import { Outlet } from 'react-router-dom';
import { WorkspaceHeader } from './WorkspaceHeader';
import { SidebarStepper } from './SidebarStepper';
import { DegradedBanner } from './DegradedBanner';
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '../../api/client';
import { ENDPOINTS } from '../../api/endpoints';
import { Profile } from '../../types/profile';
import { useUiStore } from '../../store/uiStore';

export const AppLayout: React.FC = () => {
  const currentStartupId = useUiStore((state) => state.currentStartupId) || 'hyperscale-ai-001';

  // Fetch startup profile to keep header and version synced
  const { data: profileEnvelope } = useQuery({
    queryKey: ['profile', currentStartupId],
    queryFn: () => apiClient<Profile>(ENDPOINTS.PROFILE_GET(currentStartupId)),
    staleTime: 30000,
  });

  const startupName = profileEnvelope?.data?.identity?.startup_name || 'HyperScale AI';
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
