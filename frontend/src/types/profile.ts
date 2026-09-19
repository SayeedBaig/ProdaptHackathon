import { GapStatus, Provenance, Topic } from './contracts';

export interface Identity {
  startup_name: string;
  raw_idea: string;
  one_liner: string | null;
}

export interface Problem {
  statement: string | null;
  pain_points: string[];
}

export interface Customer {
  primary_segment: string | null;
  persona: string | null;
  segments: string[];
}

export interface Solution {
  description: string | null;
  key_features: string[];
}

export interface ValuePropositionData {
  one_line: string | null;
  elevator: string | null;
  differentiation: string | null;
  advantage: string | null;
}

export interface MarketSizeInputs {
  customers: string | null;
  price: string | null;
  frequency: string | null;
}

export interface Market {
  summary: string | null;
  size_inputs: MarketSizeInputs;
}

export interface CompetitorSummaryItem {
  name: string;
  competitor_id: string | null;
}

export interface BusinessModel {
  type: string | null;
  customer: string | null;
  payer: string | null;
  revenue_source: string | null;
  pricing: string | null;
  costs: string | null;
  go_to_market: string | null;
}

export interface Traction {
  interviews: string | null;
  interested: string | null;
  users: string | null;
  revenue: string | null;
  partnerships: string | null;
  notes: string | null;
}

export interface Assumption {
  id: string;
  text: string;
  status: 'unvalidated' | 'validated' | 'invalidated';
  source: 'founder' | 'ai';
}

export interface Risk {
  id: string;
  text: string;
  severity: 'low' | 'med' | 'high';
  source: 'founder' | 'ai';
}

export interface Gap {
  id: string;
  topic: Topic;
  text: string;
  severity: number;
  status: GapStatus;
  raised_by: 'idea_analysis' | 'critique' | 'investor';
}

export interface Profile {
  id?: string;
  schema_version: number;
  identity: Identity;
  problem: Problem;
  customer: Customer;
  solution: Solution;
  value_proposition: ValuePropositionData;
  market: Market;
  competitor_summary: CompetitorSummaryItem[];
  business_model: BusinessModel;
  traction: Traction;
  team: Record<string, unknown> | null;
  funding_ask: Record<string, unknown> | null;
  assumptions: Assumption[];
  risks: Risk[];
  gaps: Gap[];
  provenance: Record<string, Provenance | 'founder'>;
}

export interface StartupSummary {
  id: string;
  name: string;
  one_liner: string | null;
  updated_at: string;
  profile_version: number;
}
