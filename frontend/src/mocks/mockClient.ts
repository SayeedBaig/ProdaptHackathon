import { SuccessEnvelope, ResponseMeta, ErrorEnvelope } from '../types/api';
import { ApiError } from '../api/errors';
import { mockStore } from './mockStore';
import analyzeIdeaFixture from './fixtures/analyze_idea.json';
import generateClarifyFixture from './fixtures/generate_clarification_question.json';
import extractPatchFixture from './fixtures/extract_profile_patch.json';
import generateValuePropFixture from './fixtures/generate_value_proposition.json';
import analyzeCompetitorsFixture from './fixtures/analyze_competitors.json';
import analyzeMarketFixture from './fixtures/analyze_market.json';
import analyzeBusinessModelFixture from './fixtures/analyze_business_model.json';
import generatePitchFixture from './fixtures/generate_pitch.json';
import critiquePitchFixture from './fixtures/critique_pitch.json';
import generateInvestorQFixture from './fixtures/generate_investor_question.json';
import evaluateAnswerFixture from './fixtures/evaluate_answer.json';
import generateReadinessFixture from './fixtures/generate_readiness_narrative.json';
import extractFeedbackPatchesFixture from './fixtures/extract_feedback_patches.json';
import { ErrorCode, ERROR_CODE_STATUSES } from '../types/contracts';

function delay(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function getRandomLatency(): number {
  return Math.floor(Math.random() * (1200 - 600 + 1)) + 600;
}

function checkMockErrorParam(): void {
  try {
    if (typeof window === 'undefined') return;
    const urlParams = new URLSearchParams(window.location.search);
    const mockError = urlParams.get('mock_error');
    if (mockError) {
      const code = mockError as ErrorCode;
      const status = ERROR_CODE_STATUSES[code] || 500;
      const envelope: ErrorEnvelope = {
        error: {
          code,
          message: `Simulated dev error for ${code}: The system encountered a mock error condition requested by ?mock_error=${code}.`,
          details:
            code === 'VALIDATION_ERROR'
              ? { idea: 'Idea statement must be at least 15 characters long.' }
              : {},
          request_id: `req-sim-${Math.random().toString(36).substring(2, 9)}`,
        },
      };
      throw ApiError.fromEnvelope(envelope, status);
    }
  } catch (err) {
    if (err instanceof ApiError) throw err;
  }
}

export async function handleMockRequest<T>(
  endpoint: string,
  method: string,
  body?: unknown,
  profileVersion = 1
): Promise<SuccessEnvelope<T>> {
  await delay(getRandomLatency());
  checkMockErrorParam();

  let data: unknown;
  const meta: ResponseMeta = {
    ai_mode: 'mock',
    model: 'gemini-2.0-flash-mock',
    degraded: false,
    warnings: [],
    profile_version: profileVersion,
  };

  const parsedBody = (body || {}) as Record<string, unknown>;

  // Route matches
  if (endpoint.includes('/api/auth/login')) {
    data = {
      token: 'mock-jwt-token-demo-founder',
      user: {
        id: '00000000-0000-0000-0000-000000000001',
        email: 'founder@hyperscale.ai',
        name: 'Alex Vance',
      },
    };
  } else if (endpoint.includes('/api/auth/register')) {
    data = {
      token: 'mock-jwt-token-demo-founder',
      user: {
        id: '00000000-0000-0000-0000-000000000001',
        email: (parsedBody.email as string) || 'founder@hyperscale.ai',
        name: (parsedBody.name as string) || 'Alex Vance',
      },
    };
  } else if (endpoint.includes('/api/startups') && method === 'GET') {
    data = mockStore.listStartups();
  } else if (endpoint.includes('/api/startups') && method === 'POST') {
    data = mockStore.createStartup(
      (parsedBody.name as string) || 'My New Startup',
      (parsedBody.raw_idea as string) || ''
    );
  } else if (endpoint.includes('/api/profile/') && method === 'GET') {
    const startupId = endpoint.split('/').pop() || 'hyperscale-ai-001';
    const profile = mockStore.getProfile(startupId);
    data = profile;
    meta.profile_version = profile.schema_version;
  } else if (endpoint.includes('/api/profile/') && method === 'PATCH') {
    const startupId = endpoint.split('/').pop() || 'hyperscale-ai-001';
    const ops = (parsedBody.ops || []) as any[];
    const expectedVer = parsedBody.expected_version as number | undefined;
    const profile = mockStore.patchProfile(startupId, ops, expectedVer);
    data = profile;
    meta.profile_version = profile.schema_version;
  }
  // AI capabilities
  else if (endpoint.includes('/api/ai/analyze_idea')) {
    data = analyzeIdeaFixture;
  } else if (endpoint.includes('/api/ai/generate_clarification_question')) {
    data = generateClarifyFixture;
  } else if (endpoint.includes('/api/ai/extract_profile_patch')) {
    data = extractPatchFixture;
  } else if (endpoint.includes('/api/ai/generate_value_proposition')) {
    data = generateValuePropFixture;
  } else if (endpoint.includes('/api/ai/analyze_competitors')) {
    data = analyzeCompetitorsFixture;
  } else if (endpoint.includes('/api/ai/analyze_market')) {
    data = analyzeMarketFixture;
  } else if (endpoint.includes('/api/ai/analyze_business_model')) {
    data = analyzeBusinessModelFixture;
  } else if (endpoint.includes('/api/ai/generate_pitch')) {
    data = generatePitchFixture;
  } else if (endpoint.includes('/api/ai/critique_pitch')) {
    data = critiquePitchFixture;
  } else if (endpoint.includes('/api/ai/generate_investor_question')) {
    data = generateInvestorQFixture;
  } else if (endpoint.includes('/api/ai/evaluate_answer')) {
    data = evaluateAnswerFixture;
  } else if (endpoint.includes('/api/ai/generate_readiness_narrative')) {
    data = generateReadinessFixture;
  } else if (endpoint.includes('/api/ai/extract_feedback_patches')) {
    data = extractFeedbackPatchesFixture;
  } else {
    // Default fallback
    data = { success: true };
  }

  return {
    data: data as T,
    meta,
  };
}
