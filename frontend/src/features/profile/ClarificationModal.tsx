import React, { useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '../../api/client';
import { ENDPOINTS } from '../../api/endpoints';
import { ClarificationQuestion, ProfilePatch } from '../../types/capabilities';
import { Gap, Profile } from '../../types/profile';
import { Modal } from '../../components/ui/Modal';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { TOPIC_LABELS } from '../../types/contracts';
import { renderNullSafe } from '../../components/ui/NullValue';
import { HelpCircle, Sparkles, Check, ArrowRight, FileDiff } from 'lucide-react';
import { toast } from 'sonner';

interface ClarificationModalProps {
  isOpen: boolean;
  onClose: () => void;
  startupId: string;
  currentProfile: Profile;
  targetGap?: Gap | null;
}

export const ClarificationModal: React.FC<ClarificationModalProps> = ({
  isOpen,
  onClose,
  startupId,
  currentProfile,
  targetGap,
}) => {
  const queryClient = useQueryClient();
  const [answer, setAnswer] = useState('');
  const [extractedPatch, setExtractedPatch] = useState<ProfilePatch | null>(null);

  // 1. Fetch clarification question
  const { data: questionEnvelope, isLoading: isQuestionLoading, refetch: refetchQuestion } = useQuery({
    queryKey: ['clarification_question', startupId, targetGap?.id],
    queryFn: () =>
      apiClient<ClarificationQuestion>(ENDPOINTS.AI_GENERATE_CLARIFICATION_QUESTION, {
        method: 'POST',
        body: {
          startup_id: startupId,
          target_gap_id: targetGap?.id,
          topic: targetGap?.topic,
        },
      }),
    enabled: isOpen,
  });

  const question = questionEnvelope?.data;

  // 2. Extract profile patch mutation
  const extractMutation = useMutation({
    mutationFn: (userAnswer: string) =>
      apiClient<ProfilePatch>(ENDPOINTS.AI_EXTRACT_PROFILE_PATCH, {
        method: 'POST',
        body: {
          startup_id: startupId,
          question_id: question?.id,
          answer: userAnswer,
          target_field: question?.target_field,
        },
      }),
    onSuccess: (res) => {
      setExtractedPatch(res.data);
      toast.success('AI extracted profile patch ops from your answer!');
    },
  });

  // 3. Apply profile patch mutation
  const applyPatchMutation = useMutation({
    mutationFn: (patch: ProfilePatch) =>
      apiClient<Profile>(ENDPOINTS.PROFILE_PATCH(startupId), {
        method: 'PATCH',
        body: {
          ops: patch.ops,
          expected_version: currentProfile.schema_version,
        },
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['profile', startupId] });
      toast.success('Profile patch applied successfully!', {
        description: `Profile version updated to v${currentProfile.schema_version + 1}`,
      });
      handleClose();
    },
    onError: (err: any) => {
      if (err.code === 'VERSION_CONFLICT') {
        queryClient.invalidateQueries({ queryKey: ['profile', startupId] });
        toast.warning('Profile was modified in another session. Refreshed.');
      }
    },
  });

  const handleClose = () => {
    setAnswer('');
    setExtractedPatch(null);
    onClose();
  };

  const handleExtract = (e: React.FormEvent) => {
    e.preventDefault();
    if (!answer.trim()) return;
    extractMutation.mutate(answer);
  };

  const handleApply = () => {
    if (!extractedPatch) return;
    applyPatchMutation.mutate(extractedPatch);
  };

  // Helper to extract current value from path for before/after diff
  const getCurrentValueAtPath = (path: string): unknown => {
    const parts = path.replace(/^\//, '').split('/');
    let curr: any = currentProfile;
    for (const part of parts) {
      if (curr === null || curr === undefined) return null;
      curr = curr[part];
    }
    return curr;
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={handleClose}
      title="AI Clarification & Profile Refinement"
      maxWidth="2xl"
    >
      <div className="space-y-6">
        {/* Question Header */}
        <div className="p-4 rounded-xl bg-brand-50/70 border border-brand-200/80">
          <div className="flex items-center justify-between gap-2 mb-2">
            <div className="flex items-center gap-2">
              <HelpCircle className="w-5 h-5 text-brand-600 shrink-0" />
              <span className="text-xs font-bold uppercase tracking-wider text-brand-700">
                Clarification Question
              </span>
            </div>
            {question?.topic && (
              <Badge variant="brand" size="sm">
                {TOPIC_LABELS[question.topic] || question.topic}
              </Badge>
            )}
          </div>

          {isQuestionLoading ? (
            <div className="h-12 bg-brand-100/50 animate-pulse rounded-lg" />
          ) : (
            <div>
              <p className="text-base font-semibold text-slate-900 leading-snug">
                {question?.text || 'How do you intend to scale customer acquisition?'}
              </p>
              {question?.target_field && (
                <div className="text-xs text-brand-700/80 mt-2 font-mono">
                  Target Field: <span className="font-semibold">{question.target_field}</span>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Answer Input */}
        {!extractedPatch ? (
          <form onSubmit={handleExtract} className="space-y-4">
            <div>
              <div className="flex items-center justify-between mb-1.5">
                <label className="block text-sm font-semibold text-slate-800">
                  Your Answer / Refinement
                </label>
                <span className="text-xs text-slate-400">
                  {answer.length} characters
                </span>
              </div>
              <textarea
                value={answer}
                onChange={(e) => setAnswer(e.target.value)}
                rows={4}
                placeholder="Type your clarification. PitchPilot AI will parse your response and produce an atomic profile patch..."
                required
                className="w-full px-3.5 py-2.5 text-base border border-slate-300 rounded-lg focus:ring-2 focus:ring-brand-500 focus:border-brand-500 outline-none resize-none"
              />

              <div className="flex items-center gap-1.5 flex-wrap mt-2">
                <span className="text-xs font-bold text-slate-400">Quick Presets:</span>
                <button
                  type="button"
                  onClick={() =>
                    setAnswer(
                      'We will start with two nearby hostel clusters and collect menu price, nutrition, distance, and student preference data from local vendors.'
                    )
                  }
                  className="text-xs px-2.5 py-1 rounded-md bg-slate-100 hover:bg-slate-200 text-slate-700 font-medium transition-colors"
                >
                  Campus Launch Plan
                </button>
                <button
                  type="button"
                  onClick={() =>
                    setAnswer(
                      'Students will use the app for free first; we will test vendor-paid promoted listings and subscription tools after validating repeat student usage.'
                    )
                  }
                  className="text-xs px-2.5 py-1 rounded-md bg-slate-100 hover:bg-slate-200 text-slate-700 font-medium transition-colors"
                >
                  Vendor Revenue Model
                </button>
              </div>
            </div>

            <div className="flex items-center justify-between pt-2">
              <Button
                type="button"
                variant="ghost"
                size="sm"
                onClick={() => refetchQuestion()}
              >
                Different Question
              </Button>
              <div className="flex gap-2">
                <Button type="button" variant="outline" onClick={handleClose}>
                  Cancel
                </Button>
                <Button
                  type="submit"
                  variant="primary"
                  isLoading={extractMutation.isPending}
                  loadingText="Analyzing & Extracting Patch..."
                  leftIcon={<Sparkles className="w-4 h-4" />}
                >
                  Generate Profile Patch
                </Button>
              </div>
            </div>
          </form>
        ) : (
          /* Before / After Diff Preview */
          <div className="space-y-4">
            <div className="flex items-center gap-2 text-slate-800 font-bold text-base pb-2 border-b border-slate-200">
              <FileDiff className="w-5 h-5 text-brand-600" />
              Proposed Profile Changes (Patch Ops)
            </div>

            <div className="space-y-3 max-h-72 overflow-y-auto pr-1">
              {extractedPatch.ops.map((op, idx) => {
                const beforeVal = getCurrentValueAtPath(op.path);
                return (
                  <div
                    key={idx}
                    className="p-3.5 rounded-xl border border-slate-200 bg-slate-50/70 text-sm space-y-2"
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2 font-mono text-xs">
                        <Badge variant="purple" size="sm">
                          {op.op.toUpperCase()}
                        </Badge>
                        <span className="font-semibold text-slate-700">{op.path}</span>
                      </div>
                      <span className="text-xs text-slate-500 italic">{op.reason}</span>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3 pt-1">
                      {/* Before */}
                      <div className="p-2.5 rounded-lg bg-rose-50/60 border border-rose-100">
                        <span className="text-[11px] font-bold uppercase text-rose-700 block mb-1">
                          Current Value
                        </span>
                        <div className="text-xs text-slate-700">
                          {renderNullSafe(beforeVal as string, (v) =>
                            typeof v === 'object' ? JSON.stringify(v, null, 2) : String(v)
                          )}
                        </div>
                      </div>

                      {/* After */}
                      <div className="p-2.5 rounded-lg bg-emerald-50/60 border border-emerald-100">
                        <span className="text-[11px] font-bold uppercase text-emerald-700 block mb-1">
                          Updated Value
                        </span>
                        <div className="text-xs text-slate-800 font-medium">
                          {typeof op.value === 'object'
                            ? JSON.stringify(op.value, null, 2)
                            : String(op.value)}
                        </div>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>

            <div className="flex items-center justify-between pt-3 border-t border-slate-200">
              <Button
                type="button"
                variant="ghost"
                onClick={() => setExtractedPatch(null)}
              >
                Back to Edit Answer
              </Button>
              <div className="flex gap-2">
                <Button type="button" variant="outline" onClick={handleClose}>
                  Discard
                </Button>
                <Button
                  type="button"
                  variant="primary"
                  onClick={handleApply}
                  isLoading={applyPatchMutation.isPending}
                  loadingText="Applying Patch..."
                  leftIcon={<Check className="w-4 h-4" />}
                >
                  Apply Patch to Profile
                </Button>
              </div>
            </div>
          </div>
        )}
      </div>
    </Modal>
  );
};
