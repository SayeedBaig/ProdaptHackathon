import {
  CriteriaKey,
  FeedbackStatus,
  Provenance,
  SlideKey,
  Topic,
  TurnIntent,
} from './contracts';
import { Gap } from './profile';

export interface IdeaAnalysis {
  problem: string;
  target_customer: string;
  solution: string;
  pain_points: string[];
  assumptions: string[];
  risks: string[];
  missing_information: string[];
  first_question: {
    text: string;
    target_field: string;
    topic: Topic;
  };
}

export interface ClarificationQuestion {
  id: string;
  text: string;
  target_field: string;
  topic?: Topic;
  reasoning?: string;
}

export interface ProfilePatchOp {
  op: 'set' | 'add' | 'remove';
  path: string;
  value: unknown;
  reason: string;
}

export interface ProfilePatch {
  ops: ProfilePatchOp[];
}

export interface Claim {
  text: string;
  provenance: Provenance;
  evidence_ids?: string[];
  supporting_quote?: string | null;
}

export interface SlideContent {
  key: SlideKey;
  title: string;
  bullets: Array<Claim | string>;
  status: 'complete' | 'needs_input';
}

export interface Pitch {
  slides: SlideContent[];
}

export interface PitchCritiqueIssue {
  slide_key: SlideKey;
  severity: 'low' | 'med' | 'high';
  title: string;
  explanation: string;
  suggestion: string;
}

export interface PitchCritique {
  overall_score: number;
  issues: PitchCritiqueIssue[];
  investor_objections: string[];
  top_priorities: string[];
}

export interface ValueProposition {
  one_line: string;
  elevator: string;
  differentiation: string;
  advantage: string;
  target_segment: string;
  customer_problem_alignment: string;
  provenance: Record<string, Provenance>;
}

export interface CompetitorDetail {
  name: string;
  description: string;
  strengths: string[];
  weaknesses: string[];
  pricing: string;
  market_share: string;
  differentiator: string;
  provenance: Provenance;
  source_urls: string[];
}

export interface CompetitorPosition {
  name: string;
  x: number; // -10 to 10
  y: number; // -10 to 10
  is_self?: boolean;
}

export interface CompetitorAnalysis {
  direct_competitors: CompetitorDetail[];
  indirect_competitors: Array<{ name: string; description: string }>;
  matrix_axes: {
    x_axis: string;
    y_axis: string;
  };
  competitor_positions: CompetitorPosition[];
}

export interface MarketTier {
  value: number;
  formatted: string;
  description: string;
  calculation_steps: string[];
  provenance: Provenance;
  sources: string[];
}

export interface MarketAnalysis {
  tam: MarketTier;
  sam: MarketTier;
  som: MarketTier;
  cagr: number;
  growth_drivers: string[];
  market_risks: string[];
  assumptions: string[];
}

export interface RevenueStream {
  name: string;
  model_type: string;
  price_point: string;
  frequency: string;
  margin: string;
  calculated: boolean;
  provenance: Provenance;
}

export interface PricingTier {
  tier_name: string;
  price: string;
  billing: string;
  features: string[];
  target_audience: string;
}

export interface UnitEconomics {
  cac: number;
  ltv: number;
  payback_months: number;
  gross_margin: number;
  ltv_cac_ratio: number;
  provenance: Provenance;
  formulas: Record<string, string>;
}

export interface BusinessModelAnalysis {
  type: string;
  revenue_streams: RevenueStream[];
  pricing_tiers: PricingTier[];
  unit_economics: UnitEconomics;
  cost_structure: string[];
}

export interface InvestorQuestion {
  id: string;
  text: string;
  intent: TurnIntent;
  topic: Topic;
}

export interface AnswerEvaluation {
  scores: Record<CriteriaKey, number>;
  explanation: string;
  strengths: string[];
  weaknesses: string[];
  recommended_improvement: string;
  weakest_criterion: CriteriaKey;
  claims_made: string[];
  follow_up_question: string | null;
  new_gaps?: Gap[];
}

export interface ReadinessNarrative {
  overall_score: number;
  verdict: string;
  executive_summary: string;
  criteria_scores: Record<CriteriaKey, number>;
  topic_coverage: Record<Topic, number>;
  top_strengths: string[];
  critical_gaps: string[];
  action_items: string[];
  investor_verdict: string;
}

export interface FeedbackItemDraft {
  id: string;
  topic: Topic;
  title: string;
  description: string;
  source: 'critique' | 'investor' | 'peer';
  status: FeedbackStatus;
  suggested_patch: ProfilePatch | null;
}
