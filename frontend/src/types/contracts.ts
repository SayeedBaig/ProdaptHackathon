/**
 * Single source of truth for all contract enums.
 * Derived directly from CONVENTIONS.md section 3.2.
 * Strictly no magic strings outside this file.
 */

// 1. Provenance
export const PROVENANCE_VALUES = [
  'source_backed',
  'founder_assumption',
  'calculated',
  'ai_analysis',
] as const;
export type Provenance = (typeof PROVENANCE_VALUES)[number];

export const PROVENANCE_ICONS: Record<Provenance, string> = {
  source_backed: '🟢',
  founder_assumption: '🟡',
  ai_analysis: '🔵',
  calculated: '🔢',
};

export const PROVENANCE_LABELS: Record<Provenance, string> = {
  source_backed: 'Source-Backed Fact',
  founder_assumption: 'Founder Assumption',
  ai_analysis: 'AI Analysis & Inference',
  calculated: 'Calculated Metric',
};

// 2. Topic
export const TOPIC_VALUES = [
  'problem',
  'market',
  'differentiation',
  'business_model',
  'validation',
] as const;
export type Topic = (typeof TOPIC_VALUES)[number];

export const TOPIC_LABELS: Record<Topic, string> = {
  problem: 'Problem & Pain',
  market: 'Market & Opportunity',
  differentiation: 'Differentiation & Moat',
  business_model: 'Business Model & Unit Economics',
  validation: 'Validation & Traction',
};

// 3. Criteria keys (ints 0-10)
export const CRITERIA_KEYS = [
  'clarity',
  'specificity',
  'evidence',
  'business_reasoning',
  'differentiation',
  'scalability',
] as const;
export type CriteriaKey = (typeof CRITERIA_KEYS)[number];

export const CRITERIA_LABELS: Record<CriteriaKey, string> = {
  clarity: 'Clarity',
  specificity: 'Specificity',
  evidence: 'Evidence',
  business_reasoning: 'Business Reasoning',
  differentiation: 'Differentiation',
  scalability: 'Scalability',
};

// 4. Slide keys
export const SLIDE_KEYS = [
  'problem',
  'solution',
  'product',
  'target_market',
  'market_opportunity',
  'competition',
  'advantage',
  'business_model',
  'gtm',
  'traction',
  'team',
  'ask',
] as const;
export type SlideKey = (typeof SLIDE_KEYS)[number];

export const SLIDE_TITLES: Record<SlideKey, string> = {
  problem: '1. The Problem',
  solution: '2. The Solution',
  product: '3. Product & Demo',
  target_market: '4. Target Customer',
  market_opportunity: '5. Market Opportunity (TAM/SAM/SOM)',
  competition: '6. Competitive Landscape',
  advantage: '7. Unfair Advantage',
  business_model: '8. Business Model & Pricing',
  gtm: '9. Go-To-Market Strategy',
  traction: '10. Traction & Milestones',
  team: '11. The Team',
  ask: '12. The Ask & Use of Funds',
};

// 5. Gap status
export const GAP_STATUS_VALUES = ['open', 'resolved'] as const;
export type GapStatus = (typeof GAP_STATUS_VALUES)[number];

// 6. Feedback status
export const FEEDBACK_STATUS_VALUES = ['open', 'accepted', 'dismissed', 'done'] as const;
export type FeedbackStatus = (typeof FEEDBACK_STATUS_VALUES)[number];

// 7. Session status
export const SESSION_STATUS_VALUES = ['active', 'completed', 'abandoned'] as const;
export type SessionStatus = (typeof SESSION_STATUS_VALUES)[number];

// 8. Turn intent
export const TURN_INTENT_VALUES = ['opening', 'follow_up', 'new_topic'] as const;
export type TurnIntent = (typeof TURN_INTENT_VALUES)[number];

export const TURN_INTENT_LABELS: Record<TurnIntent, string> = {
  opening: 'Opening Question',
  follow_up: 'Follow-up Probe',
  new_topic: 'Pivot to New Topic',
};

// 9. AI capability names
export const AI_CAPABILITY_NAMES = [
  'analyze_idea',
  'generate_clarification_question',
  'extract_profile_patch',
  'generate_value_proposition',
  'analyze_competitors',
  'analyze_market',
  'analyze_business_model',
  'generate_pitch',
  'critique_pitch',
  'generate_investor_question',
  'evaluate_answer',
  'generate_readiness_narrative',
  'extract_feedback_patches',
] as const;
export type AiCapabilityName = (typeof AI_CAPABILITY_NAMES)[number];

// 10. Error codes and corresponding HTTP statuses
export const ERROR_CODES = [
  'VALIDATION_ERROR',
  'UNAUTHENTICATED',
  'NOT_FOUND',
  'VERSION_CONFLICT',
  'SESSION_CLOSED',
  'RATE_LIMITED',
  'LLM_INVALID_OUTPUT',
  'LLM_UNAVAILABLE',
] as const;
export type ErrorCode = (typeof ERROR_CODES)[number];

export const ERROR_CODE_STATUSES: Record<ErrorCode, number> = {
  VALIDATION_ERROR: 422,
  UNAUTHENTICATED: 401,
  NOT_FOUND: 404,
  VERSION_CONFLICT: 409,
  SESSION_CLOSED: 409,
  RATE_LIMITED: 429,
  LLM_INVALID_OUTPUT: 502,
  LLM_UNAVAILABLE: 503,
};

// 11. AI Modes
export const AI_MODES = ['live', 'fallback_provider', 'mock'] as const;
export type AiMode = (typeof AI_MODES)[number];
