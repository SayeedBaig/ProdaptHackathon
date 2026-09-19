/**
 * Centralized endpoint path registry.
 * If backend routes change, edit here in one place.
 */

const BASE_URL = (import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1').replace(/\/$/, '');

export const ENDPOINTS = {
  // Auth
  AUTH_LOGIN: `${BASE_URL}/auth/login`,
  AUTH_REGISTER: `${BASE_URL}/auth/register`,
  AUTH_ME: `${BASE_URL}/auth/me`,

  // Startup Management
  STARTUPS: `${BASE_URL}/startups`,
  STARTUP_DETAIL: (id: string) => `${BASE_URL}/startups/${id}`,

  // Profile CRUD & Versioning
  PROFILE_GET: (id: string) => `${BASE_URL}/profile/${id}`,
  PROFILE_PATCH: (id: string) => `${BASE_URL}/profile/${id}`,

  // AI Capabilities (13 endpoints)
  AI_ANALYZE_IDEA: `${BASE_URL}/ai/analyze_idea`,
  AI_GENERATE_CLARIFICATION_QUESTION: `${BASE_URL}/ai/generate_clarification_question`,
  AI_EXTRACT_PROFILE_PATCH: `${BASE_URL}/ai/extract_profile_patch`,
  AI_GENERATE_VALUE_PROPOSITION: `${BASE_URL}/ai/generate_value_proposition`,
  AI_ANALYZE_COMPETITORS: `${BASE_URL}/ai/analyze_competitors`,
  AI_ANALYZE_MARKET: `${BASE_URL}/ai/analyze_market`,
  AI_ANALYZE_BUSINESS_MODEL: `${BASE_URL}/ai/analyze_business_model`,
  AI_GENERATE_PITCH: `${BASE_URL}/ai/generate_pitch`,
  AI_CRITIQUE_PITCH: `${BASE_URL}/ai/critique_pitch`,
  AI_GENERATE_INVESTOR_QUESTION: `${BASE_URL}/ai/generate_investor_question`,
  AI_EVALUATE_ANSWER: `${BASE_URL}/ai/evaluate_answer`,
  AI_GENERATE_READINESS_NARRATIVE: `${BASE_URL}/ai/generate_readiness_narrative`,
  AI_EXTRACT_FEEDBACK_PATCHES: `${BASE_URL}/ai/extract_feedback_patches`,

  // Investor Session Management
  INVESTOR_SESSIONS: `${BASE_URL}/investor/sessions`,
  INVESTOR_SESSION_DETAIL: (id: string) => `${BASE_URL}/investor/sessions/${id}`,
  INVESTOR_SESSION_END: (id: string) => `${BASE_URL}/investor/sessions/${id}/finish`,
};
