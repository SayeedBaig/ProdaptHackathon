import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '../../api/client';
import { ENDPOINTS } from '../../api/endpoints';
import { Gap, Profile } from '../../types/profile';
import { IdeaAnalysis } from '../../types/capabilities';
import { useUiStore } from '../../store/uiStore';
import { ProfileFields } from './ProfileFields';
import { ClarificationModal } from './ClarificationModal';
import { GapList } from '../../components/gaps/GapList';
import { ProvenanceLegend } from '../../components/provenance/ProvenanceLegend';
import { Button } from '../../components/ui/Button';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { AiLoadingState } from '../../components/ui/Skeleton';
import { Modal } from '../../components/ui/Modal';
import { mockStore } from '../../mocks/mockStore';
import {
  Sparkles,
  MessageSquarePlus,
  Edit3,
  Check,
  TrendingUp,
  AlertCircle,
  Layers,
  Zap,
} from 'lucide-react';
import { toast } from 'sonner';

const IDEA_PRESETS = [
  {
    title: 'Kubernetes FinOps (Default)',
    idea: 'Autonomous Kubernetes infrastructure optimization agent that analyzes real-time telemetry to right-size CPU/RAM allocations, reducing cloud bills by 35% with zero downtime.',
  },
  {
    title: 'Clinical Trial AI',
    idea: 'AI platform connecting oncology clinical trials with underrepresented patient cohorts by analyzing electronic health record (EHR) genomics in real-time, accelerating trial enrollment by 4x.',
  },
  {
    title: 'Cyber Incident Co-Pilot',
    idea: 'Autonomous tier-1 Security Operations Center (SOC) agent that correlates cloud threat alerts, writes forensic timelines, and automatically isolates compromised AWS IAM credentials.',
  },
];

export const OverviewProfilePage: React.FC = () => {
  const queryClient = useQueryClient();
  const startupId = useUiStore((state) => state.currentStartupId) || 'hyperscale-ai-001';

  const [ideaInput, setIdeaInput] = useState('');
  const [isClarifyOpen, setIsClarifyOpen] = useState(false);
  const [selectedGap, setSelectedGap] = useState<Gap | null>(null);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);

  // 1. Fetch current profile
  const { data: profileEnvelope, isLoading: isProfileLoading } = useQuery({
    queryKey: ['profile', startupId],
    queryFn: () => apiClient<Profile>(ENDPOINTS.PROFILE_GET(startupId)),
  });

  const profile = profileEnvelope?.data;

  // Editable profile state for manual tweak modal
  const [editProblem, setEditProblem] = useState('');
  const [editSolution, setEditSolution] = useState('');
  const [editCustomer, setEditCustomer] = useState('');

  React.useEffect(() => {
    if (profile?.identity?.raw_idea && !ideaInput) {
      setIdeaInput(profile.identity.raw_idea);
    }
    if (profile) {
      setEditProblem(profile.problem.statement || '');
      setEditSolution(profile.solution.description || '');
      setEditCustomer(profile.customer.primary_segment || '');
    }
  }, [profile]);

  // 2. Analyze Idea mutation
  const analyzeIdeaMutation = useMutation({
    mutationFn: (idea: string) =>
      apiClient<IdeaAnalysis>(ENDPOINTS.AI_ANALYZE_IDEA, {
        method: 'POST',
        body: {
          startup_id: startupId,
          raw_idea: idea,
        },
      }),
    onSuccess: (res) => {
      const ops = [
        { op: 'set' as const, path: '/identity/raw_idea', value: ideaInput, reason: 'Updated raw idea' },
        { op: 'set' as const, path: '/problem/statement', value: res.data.problem, reason: 'AI idea analysis' },
        { op: 'set' as const, path: '/problem/pain_points', value: res.data.pain_points, reason: 'AI idea analysis' },
        { op: 'set' as const, path: '/solution/description', value: res.data.solution, reason: 'AI idea analysis' },
        { op: 'set' as const, path: '/customer/primary_segment', value: res.data.target_customer, reason: 'AI idea analysis' },
      ];

      apiClient<Profile>(ENDPOINTS.PROFILE_PATCH(startupId), {
        method: 'PATCH',
        body: { ops, expected_version: profile?.schema_version },
      }).then(() => {
        queryClient.invalidateQueries({ queryKey: ['profile', startupId] });
        toast.success('Idea analyzed & structured profile updated!', {
          description: 'Problem statement, customer segments, and risks updated.',
        });
      });
    },
  });

  // 3. Manual Edit Profile mutation
  const editProfileMutation = useMutation({
    mutationFn: () => {
      const ops = [
        { op: 'set' as const, path: '/problem/statement', value: editProblem, reason: 'Manual founder refinement' },
        { op: 'set' as const, path: '/solution/description', value: editSolution, reason: 'Manual founder refinement' },
        { op: 'set' as const, path: '/customer/primary_segment', value: editCustomer, reason: 'Manual founder refinement' },
      ];
      return apiClient<Profile>(ENDPOINTS.PROFILE_PATCH(startupId), {
        method: 'PATCH',
        body: { ops, expected_version: profile?.schema_version },
      });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['profile', startupId] });
      toast.success('Profile updated successfully!');
      setIsEditModalOpen(false);
    },
  });

  const handleAnalyzeIdea = (e: React.FormEvent) => {
    e.preventDefault();
    if (!ideaInput.trim()) {
      toast.error('Please enter a description of your startup idea.');
      return;
    }
    analyzeIdeaMutation.mutate(ideaInput);
  };

  const handleSelectPreset = (presetIdea: string) => {
    setIdeaInput(presetIdea);
    analyzeIdeaMutation.mutate(presetIdea);
  };

  const handleToggleGap = (gapId: string) => {
    mockStore.toggleGapStatus(startupId, gapId);
    queryClient.invalidateQueries({ queryKey: ['profile', startupId] });
  };

  const handleAnswerGap = (gap: Gap) => {
    setSelectedGap(gap);
    setIsClarifyOpen(true);
  };

  const handleOpenClarification = () => {
    setSelectedGap(null);
    setIsClarifyOpen(true);
  };

  if (isProfileLoading || !profile) {
    return (
      <AiLoadingState
        message="Loading Startup Profile..."
        subtext="Fetching versioned profile fields and provenance telemetry..."
      />
    );
  }

  const openGapsCount = profile.gaps.filter((g) => g.status === 'open').length;
  const resolvedGapsCount = profile.gaps.filter((g) => g.status === 'resolved').length;
  const totalGaps = profile.gaps.length;
  const validationPct = totalGaps > 0 ? Math.round((resolvedGapsCount / totalGaps) * 100) : 100;

  return (
    <div className="space-y-8 pb-16">
      {/* Header & Quick Actions */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
            Overview & Startup Profile
          </h1>
          <p className="text-base text-slate-500 mt-1">
            Build, refine, and stress-test your startup thesis with full provenance tracking.
          </p>
        </div>

        <div className="flex items-center gap-2.5">
          <Button
            variant="outline"
            onClick={() => setIsEditModalOpen(true)}
            leftIcon={<Edit3 className="w-4 h-4 text-slate-600" />}
          >
            Edit Profile Fields
          </Button>

          <Button
            variant="primary"
            onClick={handleOpenClarification}
            leftIcon={<MessageSquarePlus className="w-4 h-4" />}
            className="shadow-sm"
          >
            Ask AI Clarification
          </Button>
        </div>
      </div>

      {/* Metrics Banner */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="p-4 rounded-xl bg-white border border-slate-200/80 shadow-xs flex items-center gap-3.5">
          <div className="p-3 rounded-xl bg-brand-50 text-brand-700">
            <Layers className="w-5 h-5" />
          </div>
          <div>
            <span className="text-xs font-bold uppercase text-slate-400 block">Profile Status</span>
            <div className="text-lg font-extrabold text-slate-900">
              Version v{profile.schema_version} Active
            </div>
          </div>
        </div>

        <div className="p-4 rounded-xl bg-white border border-slate-200/80 shadow-xs flex items-center gap-3.5">
          <div className="p-3 rounded-xl bg-amber-50 text-amber-700">
            <AlertCircle className="w-5 h-5" />
          </div>
          <div>
            <span className="text-xs font-bold uppercase text-slate-400 block">Open Diligence Gaps</span>
            <div className="text-lg font-extrabold text-amber-900">
              {openGapsCount} Need Validation
            </div>
          </div>
        </div>

        <div className="p-4 rounded-xl bg-white border border-slate-200/80 shadow-xs flex items-center gap-3.5">
          <div className="p-3 rounded-xl bg-emerald-50 text-emerald-700">
            <TrendingUp className="w-5 h-5" />
          </div>
          <div>
            <span className="text-xs font-bold uppercase text-slate-400 block">Diligence Completion</span>
            <div className="text-lg font-extrabold text-emerald-800">
              {validationPct}% Validated
            </div>
          </div>
        </div>
      </div>

      {/* Idea Input & Decompose Card */}
      <Card className="border-brand-200/80 bg-gradient-to-b from-white to-brand-50/20 shadow-sm">
        <CardHeader>
          <div className="flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-brand-600" />
            <CardTitle>Initial Idea Decomposer</CardTitle>
          </div>
          <span className="text-xs font-semibold text-brand-700 bg-brand-50 px-2.5 py-1 rounded-md border border-brand-200">
            AI Capability: analyze_idea
          </span>
        </CardHeader>
        <CardContent className="space-y-4">
          <form onSubmit={handleAnalyzeIdea} className="space-y-3">
            <label className="block text-sm font-semibold text-slate-700">
              Pitch your startup idea (problem, solution, target customer, or rough notes):
            </label>
            <textarea
              value={ideaInput}
              onChange={(e) => setIdeaInput(e.target.value)}
              rows={3}
              placeholder="e.g. An autonomous Kubernetes cost optimization agent that right-sizes pod allocations to reduce cloud bills by 35% with zero downtime..."
              className="w-full px-3.5 py-2.5 text-base border border-slate-300 rounded-lg focus:ring-2 focus:ring-brand-500 focus:border-brand-500 outline-none resize-none bg-white"
            />

            <div className="flex flex-wrap items-center justify-between gap-3 pt-1">
              {/* Quick Presets */}
              <div className="flex items-center gap-1.5 flex-wrap">
                <span className="text-xs font-bold text-slate-400 mr-1 flex items-center gap-1">
                  <Zap className="w-3 h-3 text-amber-500" /> Demo Presets:
                </span>
                {IDEA_PRESETS.map((p) => (
                  <button
                    key={p.title}
                    type="button"
                    onClick={() => handleSelectPreset(p.idea)}
                    className="text-xs px-2.5 py-1 rounded-md bg-white border border-slate-200 text-slate-700 font-medium hover:bg-slate-50 hover:border-brand-300 transition-colors"
                  >
                    {p.title}
                  </button>
                ))}
              </div>

              <Button
                type="submit"
                variant="primary"
                isLoading={analyzeIdeaMutation.isPending}
                loadingText="Decomposing idea with AI (10-30s)..."
                leftIcon={<Sparkles className="w-4 h-4" />}
              >
                Analyze Idea & Update Profile
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>

      {/* Provenance Legend Bar */}
      <ProvenanceLegend />

      {/* Structured Profile Fields */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-bold text-slate-900">
            Versioned Profile Specification (v{profile.schema_version})
          </h2>
        </div>

        <ProfileFields profile={profile} />
      </div>

      {/* Diligence Gaps & Red Flags Section */}
      <Card className="p-6 shadow-sm">
        <GapList
          gaps={profile.gaps}
          onToggleStatus={handleToggleGap}
          onAnswerGap={handleAnswerGap}
        />
      </Card>

      {/* Manual Edit Profile Modal */}
      <Modal
        isOpen={isEditModalOpen}
        onClose={() => setIsEditModalOpen(false)}
        title="Refine Profile Fields Directly"
        maxWidth="xl"
      >
        <form
          onSubmit={(e) => {
            e.preventDefault();
            editProfileMutation.mutate();
          }}
          className="space-y-4"
        >
          <div>
            <label className="block text-sm font-semibold text-slate-700 mb-1">
              Problem Statement
            </label>
            <textarea
              value={editProblem}
              onChange={(e) => setEditProblem(e.target.value)}
              rows={3}
              required
              className="w-full px-3 py-2 text-base border border-slate-300 rounded-lg focus:ring-2 focus:ring-brand-500 outline-none"
            />
          </div>

          <div>
            <label className="block text-sm font-semibold text-slate-700 mb-1">
              Solution Description
            </label>
            <textarea
              value={editSolution}
              onChange={(e) => setEditSolution(e.target.value)}
              rows={3}
              required
              className="w-full px-3 py-2 text-base border border-slate-300 rounded-lg focus:ring-2 focus:ring-brand-500 outline-none"
            />
          </div>

          <div>
            <label className="block text-sm font-semibold text-slate-700 mb-1">
              Primary Customer Segment / ICP
            </label>
            <input
              type="text"
              value={editCustomer}
              onChange={(e) => setEditCustomer(e.target.value)}
              required
              className="w-full px-3 py-2 text-base border border-slate-300 rounded-lg focus:ring-2 focus:ring-brand-500 outline-none"
            />
          </div>

          <div className="flex justify-end gap-2 pt-2 border-t border-slate-100">
            <Button
              type="button"
              variant="outline"
              onClick={() => setIsEditModalOpen(false)}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              variant="primary"
              isLoading={editProfileMutation.isPending}
              loadingText="Saving..."
              leftIcon={<Check className="w-4 h-4" />}
            >
              Save Changes (Bump to v{profile.schema_version + 1})
            </Button>
          </div>
        </form>
      </Modal>

      {/* Clarification Chat & Patch Modal */}
      <ClarificationModal
        isOpen={isClarifyOpen}
        onClose={() => setIsClarifyOpen(false)}
        startupId={startupId}
        currentProfile={profile}
        targetGap={selectedGap}
      />
    </div>
  );
};
