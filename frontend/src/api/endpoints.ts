/**
 * Centralized endpoint path registry.
 * If backend routes change, edit here in one place.
 */

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const ENDPOINTS = {
  // Auth
  AUTH_LOGIN: `${BASE_URL}/api/auth/login`,
  AUTH_REGISTER: `${BASE_URL}/api/auth/register`,
  AUTH_ME: `${BASE_URL}/api/auth/me`,

  // Startup Management
  STARTUPS: `${BASE_URL}/api/startups`,
  STARTUP_DETAIL: (id: string) => `${BASE_URL}/api/startups/${id}`,

  // Profile CRUD & Versioning
  PROFILE_GET: (id: string) => `${BASE_URL}/api/profile/${id}`,
  PROFILE_PATCH: (id: string) => `${BASE_URL}/api/profile/${id}`,

  // AI Capabilities (13 endpoints)
  AI_ANALYZE_IDEA: `${BASE_URL}/api/ai/analyze_idea`,
  AI_GENERATE_CLARIFICATION_QUESTION: `${BASE_URL}/api/ai/generate_clarification_question`,
  AI_EXTRACT_PROFILE_PATCH: `${BASE_URL}/api/ai/extract_profile_patch`,
  AI_GENERATE_VALUE_PROPOSITION: `${BASE_URL}/api/ai/generate_value_proposition`,
  AI_ANALYZE_COMPETITORS: `${BASE_URL}/api/ai/analyze_competitors`,
  AI_ANALYZE_MARKET: `${BASE_URL}/api/ai/analyze_market`,
  AI_ANALYZE_BUSINESS_MODEL: `${BASE_URL}/api/ai/analyze_business_model`,
  AI_GENERATE_PITCH: `${BASE_URL}/api/ai/generate_pitch`,
  AI_CRITIQUE_PITCH: `${BASE_URL}/api/ai/critique_pitch`,
  AI_GENERATE_INVESTOR_QUESTION: `${BASE_URL}/api/ai/generate_investor_question`,
  AI_EVALUATE_ANSWER: `${BASE_URL}/api/ai/evaluate_answer`,
  AI_GENERATE_READINESS_NARRATIVE: `${BASE_URL}/api/ai/generate_readiness_narrative`,
  AI_EXTRACT_FEEDBACK_PATCHES: `${BASE_URL}/api/ai/extract_feedback_patches`,

  // Investor Session Management
  INVESTOR_SESSIONS: `${BASE_URL}/api/investor/sessions`,
  INVESTOR_SESSION_DETAIL: (id: string) => `${BASE_URL}/api/investor/sessions/${id}`,
  INVESTOR_SESSION_END: (id: string) => `${BASE_URL}/api/investor/sessions/${id}/end`,
};
