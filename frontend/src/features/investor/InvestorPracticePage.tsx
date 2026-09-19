import React, { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '../../api/client';
import { ENDPOINTS } from '../../api/endpoints';
import {
  InvestorQuestion,
  AnswerEvaluation,
} from '../../types/capabilities';
import {
  TurnIntent,
  Topic,
  TOPIC_LABELS,
  TURN_INTENT_LABELS,
  SessionStatus,
} from '../../types/contracts';
import { useUiStore } from '../../store/uiStore';
import { mockStore } from '../../mocks/mockStore';
import { CriteriaRadarChart } from '../../components/charts/CriteriaRadarChart';
import { CriteriaBarChart } from '../../components/charts/CriteriaBarChart';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import {
  Bot,
  User,
  Send,
  Sparkles,
  ArrowRight,
  RotateCcw,
  CheckCircle2,
  AlertTriangle,
  Lightbulb,
  Award,
  Flag,
  Briefcase,
  Zap,
} from 'lucide-react';
import { toast } from 'sonner';
import { Link } from 'react-router-dom';

interface Turn {
  id: string;
  question: InvestorQuestion;
  founderAnswer?: string;
  evaluation?: AnswerEvaluation;
}

const INVESTOR_PERSONAS = [
  {
    id: 'marc',
    name: 'Marc A.',
    title: 'General Partner (Growth Fund)',
    focus: 'Market size, monetization, and validation evidence',
    avatar: '💼',
  },
  {
    id: 'elena',
    name: 'Dr. Elena R.',
    title: 'Product Partner',
    focus: 'Product differentiation and user behavior',
    avatar: '🧭',
  },
  {
    id: 'jason',
    name: 'Jason K.',
    title: 'Operator-in-Residence',
    focus: 'Launch operations and execution risk',
    avatar: '🛠️',
  },
];

const ANSWER_TEMPLATES = [
  {
    label: 'Pilot Evidence',
    text: 'We will validate demand with 50 hostel student interviews, track the top meal-selection criteria, and run a two-week pilot with nearby food vendors to measure repeat usage.',
  },
  {
    label: 'Defend Differentiation',
    text: 'Unlike generic food delivery apps, we focus on student-specific ranking across price, nutrition, distance, and preferences, with campus-level vendor data and feedback loops.',
  },
  {
    label: 'Business Model',
    text: 'We will start free for students, then test vendor partner subscriptions, promoted healthy meal listings, and student premium filters after usage is validated.',
  },
];

const normalizeQuestion = (raw: any): InvestorQuestion => ({
  id: raw?.id || `inv-q-${Date.now()}`,
  text: raw?.text || 'What is the strongest evidence that this startup can win its initial market?',
  intent: raw?.intent || 'follow_up',
  topic: raw?.topic || 'validation',
});

const normalizeEvaluation = (raw: any): AnswerEvaluation => ({
  scores: raw?.scores || {
    clarity: 6,
    specificity: 5,
    evidence: 4,
    business_reasoning: 5,
    differentiation: 5,
    scalability: 5,
  },
  explanation: raw?.explanation || 'The answer was evaluated, but the model returned limited narrative detail.',
  strengths: raw?.strengths || [],
  weaknesses: raw?.weaknesses || [],
  recommended_improvement: raw?.recommended_improvement || 'Add concrete customer evidence, numbers, and defensibility.',
  weakest_criterion: raw?.weakest_criterion || 'evidence',
  claims_made: raw?.claims_made || [],
  follow_up_question: raw?.follow_up_question || null,
  new_gaps: raw?.new_gaps || [],
});

export const InvestorPracticePage: React.FC = () => {
  const queryClient = useQueryClient();
  const startupId = useUiStore((state) => state.currentStartupId) || 'hyperscale-ai-001';

  // Session state
  const [selectedPersona, setSelectedPersona] = useState(INVESTOR_PERSONAS[0]);
  const [sessionStatus, setSessionStatus] = useState<SessionStatus>('active');
  const [turns, setTurns] = useState<Turn[]>([]);
  const [currentTurnIntent, setCurrentTurnIntent] = useState<TurnIntent>('opening');
  const [currentTopic, setCurrentTopic] = useState<Topic>('differentiation');
  const [founderInput, setFounderInput] = useState('');
  const [currentQuestion, setCurrentQuestion] = useState<InvestorQuestion>({
    id: 'inv-q-001',
    text: 'What evidence will prove that your target users will choose this product instead of their current alternatives?',
    intent: 'opening',
    topic: 'validation',
  });

  // 1. Generate Next Question Mutation
  const nextQuestionMutation = useMutation({
    mutationFn: ({ intent, topic }: { intent: TurnIntent; topic?: Topic }) =>
      apiClient<InvestorQuestion>(ENDPOINTS.AI_GENERATE_INVESTOR_QUESTION, {
        method: 'POST',
        body: {
          startup_id: startupId,
          intent,
          topic: topic || currentTopic,
          persona: selectedPersona.name,
          previous_question_id: currentQuestion?.id,
        },
      }),
    onSuccess: (res) => {
      const question = normalizeQuestion(res.data);
      setCurrentQuestion(question);
      setCurrentTurnIntent(question.intent);
      setCurrentTopic(question.topic);
      setFounderInput('');
      toast.success(`${selectedPersona.name} formulated next question`);
    },
  });

  // 2. Evaluate Answer Mutation
  const evaluateMutation = useMutation({
    mutationFn: (answerText: string) =>
      apiClient<AnswerEvaluation>(ENDPOINTS.AI_EVALUATE_ANSWER, {
        method: 'POST',
        body: {
          startup_id: startupId,
          question_id: currentQuestion.id,
          answer: answerText,
          topic: currentQuestion.topic,
          persona: selectedPersona.name,
        },
      }),
    onSuccess: (res) => {
      const evaluation = normalizeEvaluation(res.data);
      const newTurn: Turn = {
        id: `turn-${Date.now()}`,
        question: currentQuestion,
        founderAnswer: founderInput,
        evaluation,
      };

      setTurns((prev) => [...prev, newTurn]);

      // If new gaps were raised by the investor, add them to profile gaps
      if (evaluation.new_gaps && evaluation.new_gaps.length > 0) {
        evaluation.new_gaps.forEach((gap) => {
          mockStore.addGap(startupId, gap);
        });
        queryClient.invalidateQueries({ queryKey: ['profile', startupId] });
        toast.info('New diligence gap identified and recorded on your profile.');
      }

      toast.success('Partner evaluated your answer!');
    },
  });

  const handleSubmitAnswer = (e: React.FormEvent) => {
    e.preventDefault();
    if (!founderInput.trim() || evaluateMutation.isPending) return;
    if (sessionStatus !== 'active') {
      toast.error('This session has been completed or closed.');
      return;
    }
    evaluateMutation.mutate(founderInput);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmitAnswer(e);
    }
  };

  const handleNextTurn = (intent: TurnIntent) => {
    nextQuestionMutation.mutate({ intent });
  };

  const handleEndSession = () => {
    setSessionStatus('completed');
    toast.success('Investor practice session completed!', {
      description: 'Your responses are aggregated into the Readiness Report.',
    });
  };

  const handleRestart = () => {
    setSessionStatus('active');
    setTurns([]);
    setCurrentQuestion({
      id: 'inv-q-001',
      text: 'What evidence will prove that your target users will choose this product instead of their current alternatives?',
      intent: 'opening',
      topic: 'validation',
    });
    setFounderInput('');
  };

  const latestTurn = turns[turns.length - 1];

  const intentBadgeStyle = (intent: TurnIntent): 'brand' | 'warning' | 'purple' => {
    if (intent === 'opening') return 'brand';
    if (intent === 'follow_up') return 'warning';
    return 'purple';
  };

  return (
    <div className="space-y-6 pb-16">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="text-xs font-semibold text-brand-700 bg-brand-50 px-2.5 py-0.5 rounded-md border border-brand-200">
              AI Capabilities: generate_investor_question & evaluate_answer
            </span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
            Simulated Investor Diligence Practice
          </h1>
          <p className="text-base text-slate-500 mt-1">
            Field partner-level questions, test your defensibility, and score your answers on 6 criteria.
          </p>
        </div>

        {/* Session Status & End Control */}
        <div className="flex items-center gap-2">
          <Badge
            variant={sessionStatus === 'active' ? 'success' : 'default'}
            size="md"
          >
            Session: {sessionStatus.toUpperCase()}
          </Badge>

          {sessionStatus === 'active' ? (
            <Button
              variant="outline"
              size="sm"
              onClick={handleEndSession}
              leftIcon={<Flag className="w-4 h-4 text-slate-500" />}
            >
              End Session
            </Button>
          ) : (
            <Button
              variant="outline"
              size="sm"
              onClick={handleRestart}
              leftIcon={<RotateCcw className="w-4 h-4" />}
            >
              Start New Session
            </Button>
          )}
        </div>
      </div>

      {/* Investor Persona Selector Card */}
      <Card className="p-4 bg-gradient-to-r from-slate-900 via-slate-800 to-indigo-950 text-white shadow-md">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <div className="text-xs font-bold uppercase tracking-wider text-brand-300 mb-1 flex items-center gap-1.5">
              <Briefcase className="w-3.5 h-3.5" /> Diligence Partner Room
            </div>
            <div className="text-base font-bold text-white flex items-center gap-2">
              <span>{selectedPersona.avatar}</span>
              <span>Interviewing with {selectedPersona.name}</span>
              <span className="text-xs font-normal text-slate-400">({selectedPersona.title})</span>
            </div>
            <div className="text-xs text-slate-300 mt-0.5">
              Focus: <strong className="text-brand-200">{selectedPersona.focus}</strong>
            </div>
          </div>

          {/* Persona Pills */}
          <div className="flex items-center gap-2 flex-wrap">
            {INVESTOR_PERSONAS.map((p) => (
              <button
                key={p.id}
                type="button"
                onClick={() => setSelectedPersona(p)}
                className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all flex items-center gap-1.5 ${
                  selectedPersona.id === p.id
                    ? 'bg-brand-600 text-white shadow-sm ring-2 ring-brand-300'
                    : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
                }`}
              >
                <span>{p.avatar}</span>
                <span>{p.name}</span>
              </button>
            ))}
          </div>
        </div>
      </Card>

      {/* Session Closed Banner */}
      {sessionStatus === 'completed' && (
        <div className="p-4 rounded-xl bg-emerald-50 border border-emerald-200 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <CheckCircle2 className="w-6 h-6 text-emerald-600" />
            <div>
              <div className="font-bold text-emerald-950">
                Practice Session Concluded
              </div>
              <div className="text-xs text-emerald-700">
                You evaluated {turns.length} investor questions. View your final scorecard in the Readiness Report.
              </div>
            </div>
          </div>

          <Link to="/readiness-report">
            <Button variant="primary" size="sm" rightIcon={<ArrowRight className="w-4 h-4" />}>
              View Readiness Report
            </Button>
          </Link>
        </div>
      )}

      {/* Active Investor Chat Container */}
      <div className="space-y-6">
        {/* Past Evaluated Turns History */}
        {turns.map((turn, i) => (
          <div key={turn.id} className="space-y-4 opacity-95">
            {/* Investor Question Bubble */}
            <div className="flex items-start gap-3">
              <div className="w-10 h-10 rounded-full bg-slate-900 text-white flex items-center justify-center font-bold text-base shrink-0 mt-1 shadow-sm">
                {selectedPersona.avatar}
              </div>
              <div className="flex-1 bg-slate-100 rounded-2xl p-4 border border-slate-200 shadow-xs">
                <div className="flex items-center gap-2 mb-2">
                  <span className="text-xs font-bold text-slate-800">
                    {selectedPersona.name} ({selectedPersona.title})
                  </span>
                  <Badge variant={intentBadgeStyle(turn.question.intent)} size="sm">
                    {TURN_INTENT_LABELS[turn.question.intent]}
                  </Badge>
                  <Badge variant="default" size="sm">
                    {TOPIC_LABELS[turn.question.topic]}
                  </Badge>
                </div>
                <p className="text-base text-slate-900 font-semibold leading-relaxed">
                  {turn.question.text}
                </p>
              </div>
            </div>

            {/* Founder Answer Bubble */}
            {turn.founderAnswer && (
              <div className="flex items-start gap-3 justify-end">
                <div className="flex-1 max-w-2xl bg-brand-600 text-white rounded-2xl p-4 shadow-sm">
                  <div className="flex items-center gap-2 mb-1 text-brand-200 text-xs font-semibold">
                    <User className="w-3.5 h-3.5" /> Your Response
                  </div>
                  <p className="text-base leading-relaxed whitespace-pre-wrap">
                    {turn.founderAnswer}
                  </p>
                </div>
                <div className="w-10 h-10 rounded-full bg-brand-700 text-white flex items-center justify-center font-bold text-sm shrink-0 mt-1 shadow-sm">
                  <User className="w-5 h-5" />
                </div>
              </div>
            )}

            {/* Turn Evaluation Card */}
            {turn.evaluation && (
              <Card className="ml-12 border-brand-200 bg-white shadow-md">
                <CardHeader className="bg-slate-50/80 pb-3">
                  <div className="flex items-center gap-2">
                    <Award className="w-5 h-5 text-brand-600" />
                    <CardTitle className="text-base">
                      Turn {i + 1} Diligence Assessment
                    </CardTitle>
                  </div>
                  <span className="text-xs text-slate-500 font-mono">
                    Weakest: <strong className="text-rose-600 uppercase">{turn.evaluation.weakest_criterion}</strong>
                  </span>
                </CardHeader>
                <CardContent className="p-5 space-y-5">
                  {/* Radar & Bars Grid */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6 items-center">
                    <div>
                      <span className="text-xs font-bold uppercase text-slate-400 block text-center mb-1">
                        6 Diligence Criteria Radar
                      </span>
                      <CriteriaRadarChart scores={turn.evaluation.scores} height={260} />
                    </div>

                    <div className="space-y-4">
                      <span className="text-xs font-bold uppercase text-slate-400 block mb-1">
                        Scoring Breakdown (0-10)
                      </span>
                      <CriteriaBarChart scores={turn.evaluation.scores} />
                    </div>
                  </div>

                  {/* Written Feedback */}
                  <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 text-sm">
                    <div className="font-semibold text-slate-800 mb-1">
                      Partner Commentary:
                    </div>
                    <p className="text-slate-700 leading-relaxed">
                      {turn.evaluation.explanation}
                    </p>
                  </div>

                  {/* Strengths & Weaknesses 2-col */}
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
                    <div className="p-3 rounded-lg bg-emerald-50/70 border border-emerald-200 space-y-1">
                      <div className="font-bold text-emerald-900 flex items-center gap-1.5">
                        <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                        Effective Proof Points:
                      </div>
                      <ul className="list-disc list-inside text-emerald-800 space-y-1">
                        {turn.evaluation.strengths.map((str, sIdx) => (
                          <li key={sIdx} className="leading-snug">{str}</li>
                        ))}
                      </ul>
                    </div>

                    <div className="p-3 rounded-lg bg-amber-50/70 border border-amber-200 space-y-1">
                      <div className="font-bold text-amber-900 flex items-center gap-1.5">
                        <AlertTriangle className="w-4 h-4 text-amber-600" />
                        Vulnerabilities to Address:
                      </div>
                      <ul className="list-disc list-inside text-amber-800 space-y-1">
                        {turn.evaluation.weaknesses.map((wk, wIdx) => (
                          <li key={wIdx} className="leading-snug">{wk}</li>
                        ))}
                      </ul>
                    </div>
                  </div>

                  {/* Recommendation */}
                  <div className="p-3 rounded-lg bg-brand-50/60 border border-brand-200 text-xs flex items-start gap-2 text-brand-950">
                    <Lightbulb className="w-4 h-4 text-brand-600 shrink-0 mt-0.5" />
                    <div>
                      <span className="font-bold">Next Pitch Iteration: </span>
                      {turn.evaluation.recommended_improvement}
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        ))}

        {/* Current Active Question (If session is active) */}
        {sessionStatus === 'active' && (
          <div className="space-y-4 pt-2">
            {/* Investor Question Prompt Bubble */}
            <div className="flex items-start gap-3">
              <div className="w-10 h-10 rounded-full bg-slate-900 text-white flex items-center justify-center font-bold text-base shrink-0 mt-1 shadow-sm">
                {selectedPersona.avatar}
              </div>
              <div className="flex-1 bg-white rounded-2xl p-5 border-2 border-brand-300 shadow-md">
                <div className="flex flex-wrap items-center justify-between gap-2 mb-2">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-bold text-slate-900">
                      {selectedPersona.name} ({selectedPersona.title})
                    </span>
                    <Badge variant={intentBadgeStyle(currentQuestion.intent)} size="sm">
                      {TURN_INTENT_LABELS[currentQuestion.intent]}
                    </Badge>
                    <Badge variant="default" size="sm">
                      {TOPIC_LABELS[currentQuestion.topic]}
                    </Badge>
                  </div>
                  <span className="text-xs text-brand-600 font-semibold animate-pulse">
                    Awaiting your answer
                  </span>
                </div>

                <p className="text-lg font-bold text-slate-900 leading-snug">
                  {currentQuestion.text}
                </p>
              </div>
            </div>

            {/* Founder Answer Textarea */}
            <form onSubmit={handleSubmitAnswer} className="ml-12 space-y-3">
              <div className="relative">
                <textarea
                  value={founderInput}
                  onChange={(e) => setFounderInput(e.target.value)}
                  onKeyDown={handleKeyDown}
                  rows={4}
                  placeholder="Type your response to the investor... (Press Enter to submit, Shift+Enter for new line)"
                  className="w-full px-4 py-3 text-base border border-slate-300 rounded-xl focus:ring-2 focus:ring-brand-500 focus:border-brand-500 outline-none resize-none shadow-sm bg-white"
                />
              </div>

              {/* Quick Answer Templates */}
              <div className="flex items-center gap-1.5 flex-wrap">
                <span className="text-xs font-bold text-slate-400 mr-1 flex items-center gap-1">
                  <Zap className="w-3 h-3 text-amber-500" /> Quick Response Templates:
                </span>
                {ANSWER_TEMPLATES.map((tmpl) => (
                  <button
                    key={tmpl.label}
                    type="button"
                    onClick={() => setFounderInput(tmpl.text)}
                    className="text-xs px-2.5 py-1 rounded-md bg-white border border-slate-200 text-slate-700 font-medium hover:bg-slate-50 hover:border-brand-300 transition-colors shadow-2xs"
                  >
                    {tmpl.label}
                  </button>
                ))}
              </div>

              <div className="flex flex-wrap items-center justify-between gap-2 pt-1">
                <span className="text-xs text-slate-400">
                  Tip: Back up assumptions with interviews, pilot evidence, usage metrics, or willingness-to-pay data.
                </span>

                <Button
                  type="submit"
                  variant="primary"
                  disabled={!founderInput.trim()}
                  isLoading={evaluateMutation.isPending}
                  loadingText="Evaluating with AI..."
                  rightIcon={<Send className="w-4 h-4" />}
                >
                  Submit Answer for Scoring
                </Button>
              </div>
            </form>

            {/* Next Turn Options (If latest turn evaluated) */}
            {latestTurn && !evaluateMutation.isPending && (
              <div className="ml-12 p-4 rounded-xl bg-slate-50 border border-slate-200 flex flex-wrap items-center justify-between gap-3">
                <span className="text-xs font-semibold text-slate-600">
                  Ready for the next challenge?
                </span>
                <div className="flex items-center gap-2">
                  <Button
                    size="sm"
                    variant="outline"
                    onClick={() => handleNextTurn('follow_up')}
                    isLoading={nextQuestionMutation.isPending}
                  >
                    Follow-Up Probe
                  </Button>
                  <Button
                    size="sm"
                    variant="secondary"
                    onClick={() => handleNextTurn('new_topic')}
                    isLoading={nextQuestionMutation.isPending}
                  >
                    Pivot to New Topic
                  </Button>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
