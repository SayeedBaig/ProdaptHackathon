import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '../../api/client';
import { ENDPOINTS } from '../../api/endpoints';
import { FeedbackItemDraft, ProfilePatch } from '../../types/capabilities';
import { Profile } from '../../types/profile';
import { FeedbackStatus, Topic, TOPIC_LABELS, FEEDBACK_STATUS_VALUES } from '../../types/contracts';
import { useUiStore } from '../../store/uiStore';
import { mockStore } from '../../mocks/mockStore';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { Modal } from '../../components/ui/Modal';
import { EmptyState } from '../../components/ui/Skeleton';
import { renderNullSafe } from '../../components/ui/NullValue';
import {
  MessageSquareQuote,
  CheckCircle2,
  XCircle,
  Clock,
  Sparkles,
  FileDiff,
  Filter,
  Check,
  RotateCcw,
} from 'lucide-react';
import { toast } from 'sonner';

export const FeedbackPage: React.FC = () => {
  const queryClient = useQueryClient();
  const startupId = useUiStore((state) => state.currentStartupId) || 'hyperscale-ai-001';

  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [topicFilter, setTopicFilter] = useState<string>('all');
  const [selectedPatch, setSelectedPatch] = useState<{
    item: FeedbackItemDraft;
    patch: ProfilePatch;
  } | null>(null);

  // 1. Fetch current profile
  const { data: profileEnvelope } = useQuery({
    queryKey: ['profile', startupId],
    queryFn: () => apiClient<Profile>(ENDPOINTS.PROFILE_GET(startupId)),
  });
  const currentProfile = profileEnvelope?.data;

  // 2. Fetch feedback items (from mockStore or endpoint)
  const feedbackItems = mockStore.getFeedbackItems(startupId);

  // 3. Extract feedback patches mutation
  const extractPatchesMutation = useMutation({
    mutationFn: (feedbackItem: FeedbackItemDraft) =>
      apiClient<ProfilePatch>(ENDPOINTS.AI_EXTRACT_FEEDBACK_PATCHES, {
        method: 'POST',
        body: {
          startup_id: startupId,
          feedback_id: feedbackItem.id,
          feedback_text: `${feedbackItem.title}: ${feedbackItem.description}`,
          topic: feedbackItem.topic,
        },
      }),
    onSuccess: (res, item) => {
      setSelectedPatch({ item, patch: res.data });
    },
  });

  // 4. Apply patch to profile
  const applyPatchMutation = useMutation({
    mutationFn: (patch: ProfilePatch) =>
      apiClient<Profile>(ENDPOINTS.PROFILE_PATCH(startupId), {
        method: 'PATCH',
        body: {
          ops: patch.ops,
          expected_version: currentProfile?.schema_version,
        },
      }),
    onSuccess: () => {
      if (selectedPatch) {
        mockStore.updateFeedbackStatus(selectedPatch.item.id, 'accepted');
      }
      queryClient.invalidateQueries({ queryKey: ['profile', startupId] });
      toast.success('Feedback patch applied to startup profile!', {
        description: `Profile version incremented to v${(currentProfile?.schema_version || 1) + 1}`,
      });
      setSelectedPatch(null);
    },
  });

  const handleStatusChange = (id: string, newStatus: FeedbackStatus) => {
    mockStore.updateFeedbackStatus(id, newStatus);
    queryClient.invalidateQueries();
    toast.success(`Feedback status changed to "${newStatus}"`);
  };

  const handleAcceptFeedback = (item: FeedbackItemDraft) => {
    if (item.suggested_patch) {
      setSelectedPatch({ item, patch: item.suggested_patch });
    } else {
      extractPatchesMutation.mutate(item);
    }
  };

  const filteredItems = feedbackItems.filter((item) => {
    if (statusFilter !== 'all' && item.status !== statusFilter) return false;
    if (topicFilter !== 'all' && item.topic !== topicFilter) return false;
    return true;
  });

  const statusVariant = (status: FeedbackStatus): 'default' | 'success' | 'warning' | 'danger' => {
    if (status === 'accepted' || status === 'done') return 'success';
    if (status === 'dismissed') return 'danger';
    return 'warning';
  };

  return (
    <div className="space-y-6 pb-16">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="text-xs font-semibold text-brand-700 bg-brand-50 px-2.5 py-0.5 rounded-md border border-brand-200">
              AI Capability: extract_feedback_patches
            </span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
            Unified Feedback & Triage
          </h1>
          <p className="text-base text-slate-500 mt-1">
            Collect critiques, triage partner objections, and convert feedback into profile patches.
          </p>
        </div>
      </div>

      {/* Filter Bar */}
      <Card className="p-4">
        <div className="flex flex-wrap items-center justify-between gap-4">
          {/* Status Tabs */}
          <div className="flex items-center gap-1.5 flex-wrap">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-400 mr-1 flex items-center gap-1">
              <Filter className="w-3.5 h-3.5" /> Status:
            </span>
            <button
              onClick={() => setStatusFilter('all')}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
                statusFilter === 'all'
                  ? 'bg-slate-900 text-white shadow-xs'
                  : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
              }`}
            >
              All ({feedbackItems.length})
            </button>
            {FEEDBACK_STATUS_VALUES.map((st) => {
              const count = feedbackItems.filter((i) => i.status === st).length;
              return (
                <button
                  key={st}
                  onClick={() => setStatusFilter(st)}
                  className={`px-3 py-1.5 rounded-lg text-xs font-semibold uppercase tracking-wide transition-colors ${
                    statusFilter === st
                      ? 'bg-brand-600 text-white shadow-xs'
                      : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                  }`}
                >
                  {st} ({count})
                </button>
              );
            })}
          </div>

          {/* Topic Filter */}
          <div className="flex items-center gap-2">
            <span className="text-xs font-semibold text-slate-500">Topic:</span>
            <select
              value={topicFilter}
              onChange={(e) => setTopicFilter(e.target.value)}
              className="px-3 py-1.5 text-xs font-medium bg-slate-50 border border-slate-200 rounded-lg focus:ring-2 focus:ring-brand-500 outline-none"
            >
              <option value="all">All Topics</option>
              <option value="problem">Problem</option>
              <option value="market">Market</option>
              <option value="differentiation">Differentiation</option>
              <option value="business_model">Business Model</option>
              <option value="validation">Validation</option>
            </select>
          </div>
        </div>
      </Card>

      {/* Feedback Item Cards */}
      {filteredItems.length === 0 ? (
        <EmptyState
          title="No feedback matches the selected filters"
          description="Switch filters or generate a new pitch critique to view feedback."
          icon={<MessageSquareQuote className="w-8 h-8 text-slate-400" />}
        />
      ) : (
        <div className="space-y-4">
          {filteredItems.map((item) => (
            <Card
              key={item.id}
              className={`transition-all ${
                item.status === 'dismissed'
                  ? 'opacity-60 bg-slate-50/50'
                  : 'hover:shadow-card-hover'
              }`}
            >
              <CardContent className="p-5 space-y-3">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <div className="flex items-center gap-2">
                    <Badge variant={statusVariant(item.status)} size="sm">
                      {item.status.toUpperCase()}
                    </Badge>
                    <Badge variant="brand" size="sm">
                      {TOPIC_LABELS[item.topic] || item.topic}
                    </Badge>
                    <span className="text-xs text-slate-400">
                      Source: <strong className="capitalize">{item.source}</strong>
                    </span>
                  </div>

                  {/* Actions */}
                  <div className="flex items-center gap-1.5">
                    {item.status !== 'accepted' && (
                      <Button
                        size="sm"
                        variant="primary"
                        onClick={() => handleAcceptFeedback(item)}
                        isLoading={extractPatchesMutation.isPending}
                        leftIcon={<Sparkles className="w-3.5 h-3.5" />}
                        className="text-xs"
                      >
                        Accept & Patch
                      </Button>
                    )}

                    {item.status !== 'done' && (
                      <button
                        onClick={() => handleStatusChange(item.id, 'done')}
                        className="p-1.5 text-xs text-slate-500 hover:text-emerald-700 hover:bg-emerald-50 rounded-lg transition-colors"
                        title="Mark as Done"
                      >
                        <CheckCircle2 className="w-4 h-4" />
                      </button>
                    )}

                    {item.status !== 'dismissed' && (
                      <button
                        onClick={() => handleStatusChange(item.id, 'dismissed')}
                        className="p-1.5 text-xs text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-lg transition-colors"
                        title="Dismiss Feedback"
                      >
                        <XCircle className="w-4 h-4" />
                      </button>
                    )}

                    {item.status === 'dismissed' && (
                      <button
                        onClick={() => handleStatusChange(item.id, 'open')}
                        className="p-1.5 text-xs text-slate-400 hover:text-brand-600 hover:bg-brand-50 rounded-lg transition-colors"
                        title="Reopen Feedback"
                      >
                        <RotateCcw className="w-4 h-4" />
                      </button>
                    )}
                  </div>
                </div>

                <div>
                  <h3 className="text-base font-bold text-slate-900 mb-1">
                    {item.title}
                  </h3>
                  <p className="text-sm text-slate-700 leading-relaxed">
                    {item.description}
                  </p>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {/* Profile Patch Diff Modal */}
      {selectedPatch && (
        <Modal
          isOpen={true}
          onClose={() => setSelectedPatch(null)}
          title="Review & Apply Profile Patch"
          maxWidth="2xl"
        >
          <div className="space-y-5">
            <div className="p-3 bg-brand-50/70 border border-brand-200 rounded-xl text-sm">
              <span className="font-bold text-brand-900 block mb-1">
                Feedback Item: {selectedPatch.item.title}
              </span>
              <p className="text-xs text-slate-600">
                {selectedPatch.item.description}
              </p>
            </div>

            <div className="space-y-3 max-h-72 overflow-y-auto pr-1">
              <div className="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
                <FileDiff className="w-4 h-4 text-brand-600" /> Atomic Patch Operations ({selectedPatch.patch.ops.length})
              </div>

              {selectedPatch.patch.ops.map((op, idx) => (
                <div
                  key={idx}
                  className="p-3.5 rounded-xl border border-slate-200 bg-slate-50 text-sm space-y-2"
                >
                  <div className="flex items-center justify-between">
                    <span className="font-mono text-xs font-bold text-purple-700 bg-purple-50 px-2 py-0.5 rounded border border-purple-200">
                      {op.op.toUpperCase()} {op.path}
                    </span>
                    <span className="text-xs text-slate-500 italic">{op.reason}</span>
                  </div>

                  <div className="p-3 rounded-lg bg-emerald-50/60 border border-emerald-200 text-xs font-medium text-emerald-950">
                    <span className="text-[11px] font-bold text-emerald-700 uppercase block mb-1">
                      New Patch Value:
                    </span>
                    {typeof op.value === 'object'
                      ? JSON.stringify(op.value, null, 2)
                      : String(op.value)}
                  </div>
                </div>
              ))}
            </div>

            <div className="flex justify-end gap-2 pt-3 border-t border-slate-100">
              <Button
                variant="outline"
                onClick={() => setSelectedPatch(null)}
              >
                Cancel
              </Button>
              <Button
                variant="primary"
                onClick={() => applyPatchMutation.mutate(selectedPatch.patch)}
                isLoading={applyPatchMutation.isPending}
                loadingText="Applying Patch..."
                leftIcon={<Check className="w-4 h-4" />}
              >
                Apply Patch to Profile
              </Button>
            </div>
          </div>
        </Modal>
      )}
    </div>
  );
};
