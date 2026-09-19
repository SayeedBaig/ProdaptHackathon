import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '../../api/client';
import { ENDPOINTS } from '../../api/endpoints';
import { StartupSummary } from '../../types/profile';
import { useUiStore } from '../../store/uiStore';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Modal } from '../../components/ui/Modal';
import { Badge } from '../../components/ui/Badge';
import { renderNullSafe } from '../../components/ui/NullValue';
import { Plus, Rocket, ArrowRight, Clock } from 'lucide-react';
import { toast } from 'sonner';

export const StartupListPage: React.FC = () => {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const setCurrentStartupId = useUiStore((state) => state.setCurrentStartupId);
  const [isCreateOpen, setIsCreateOpen] = useState(false);
  const [name, setName] = useState('');
  const [rawIdea, setRawIdea] = useState('');

  const { data: envelope, isLoading } = useQuery({
    queryKey: ['startups'],
    queryFn: () => apiClient<StartupSummary[]>(ENDPOINTS.STARTUPS),
  });

  const createMutation = useMutation({
    mutationFn: (newStartup: { name: string; raw_idea: string }) =>
      apiClient<StartupSummary>(ENDPOINTS.STARTUPS, {
        method: 'POST',
        body: newStartup,
      }),
    onSuccess: (res) => {
      queryClient.invalidateQueries({ queryKey: ['startups'] });
      setCurrentStartupId(res.data.id);
      toast.success(`Startup "${res.data.name}" created!`);
      setIsCreateOpen(false);
      setName('');
      setRawIdea('');
      navigate('/');
    },
  });

  const handleSelectStartup = (startup: StartupSummary) => {
    setCurrentStartupId(startup.id);
    navigate('/');
  };

  const handleCreate = (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim() || !rawIdea.trim()) {
      toast.error('Please provide both startup name and initial idea.');
      return;
    }
    createMutation.mutate({ name, raw_idea: rawIdea });
  };

  const startups = envelope?.data || [];

  return (
    <div className="min-h-screen bg-slate-50 p-6 md:p-12">
      <div className="max-w-4xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <div className="p-2 rounded-lg bg-brand-600 text-white shadow-sm">
                <Rocket className="w-5 h-5" />
              </div>
              <h1 className="text-2xl font-bold text-slate-900">Your Startups</h1>
            </div>
            <p className="text-sm text-slate-500">
              Select an active startup workspace or create a new pitch deck
            </p>
          </div>

          <Button
            onClick={() => setIsCreateOpen(true)}
            leftIcon={<Plus className="w-4 h-4" />}
          >
            New Startup
          </Button>
        </div>

        {isLoading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="h-36 bg-slate-200 animate-pulse rounded-xl" />
            <div className="h-36 bg-slate-200 animate-pulse rounded-xl" />
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {startups.map((s) => (
              <Card
                key={s.id}
                hoverEffect
                className="cursor-pointer border-slate-200 hover:border-brand-400 transition-all"
                onClick={() => handleSelectStartup(s)}
              >
                <CardHeader className="pb-2">
                  <div className="flex items-center justify-between w-full">
                    <CardTitle className="text-lg">{s.name}</CardTitle>
                    <Badge variant="brand" size="sm">
                      v{s.profile_version}
                    </Badge>
                  </div>
                </CardHeader>
                <CardContent className="pt-1">
                  <p className="text-sm text-slate-600 line-clamp-2 min-h-[2.5rem]">
                    {renderNullSafe(s.one_liner, (text) => text)}
                  </p>

                  <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-400">
                    <span className="flex items-center gap-1">
                      <Clock className="w-3.5 h-3.5" />
                      {new Date(s.updated_at).toLocaleDateString()}
                    </span>
                    <span className="font-semibold text-brand-600 flex items-center gap-1 group">
                      Open Workspace <ArrowRight className="w-3.5 h-3.5" />
                    </span>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}

        {/* Create Startup Modal */}
        <Modal
          isOpen={isCreateOpen}
          onClose={() => setIsCreateOpen(false)}
          title="Create New Startup Pitch"
        >
          <form onSubmit={handleCreate} className="space-y-4">
            <div>
              <label className="block text-sm font-semibold text-slate-700 mb-1">
                Startup Name
              </label>
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="e.g. Acme Quantum"
                required
                className="w-full px-3.5 py-2 text-base border border-slate-300 rounded-lg focus:ring-2 focus:ring-brand-500 focus:border-brand-500 outline-none"
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-slate-700 mb-1">
                Raw Idea / Value Proposition
              </label>
              <textarea
                value={rawIdea}
                onChange={(e) => setRawIdea(e.target.value)}
                rows={4}
                placeholder="Describe your product, target customer problem, and how you solve it..."
                required
                className="w-full px-3.5 py-2 text-base border border-slate-300 rounded-lg focus:ring-2 focus:ring-brand-500 focus:border-brand-500 outline-none resize-none"
              />
            </div>

            <div className="flex justify-end gap-2 pt-2">
              <Button
                type="button"
                variant="outline"
                onClick={() => setIsCreateOpen(false)}
              >
                Cancel
              </Button>
              <Button
                type="submit"
                variant="primary"
                isLoading={createMutation.isPending}
                loadingText="Initializing..."
              >
                Create Workspace
              </Button>
            </div>
          </form>
        </Modal>
      </div>
    </div>
  );
};
