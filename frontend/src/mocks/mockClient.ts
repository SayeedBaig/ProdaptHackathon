import { SuccessEnvelope, ResponseMeta, ErrorEnvelope } from '../types/api';
import { ApiError } from '../api/errors';
import { mockStore } from './mockStore';
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

function getStartupId(parsedBody: Record<string, unknown>, endpoint: string): string {
  return (
    (parsedBody.startup_id as string) ||
    endpoint.split('/').filter(Boolean).pop() ||
    'hyperscale-ai-001'
  );
}

function getContext(parsedBody: Record<string, unknown>, endpoint: string) {
  const startupId = getStartupId(parsedBody, endpoint);
  const profile = mockStore.getProfile(startupId);
  const idea = profile.identity.raw_idea || '';
  const lower = idea.toLowerCase();
  const isFood = lower.includes('food') || lower.includes('meal') || lower.includes('hostel') || lower.includes('student');
  const name =
    isFood && profile.identity.startup_name === 'HyperScale AI'
      ? 'CampusMeal Finder'
      : profile.identity.startup_name || 'Your Startup';
  return { startupId, profile, name, idea, isFood };
}

function generateIdeaAnalysis(ctx: ReturnType<typeof getContext>) {
  if (ctx.isFood) {
    return {
      problem: 'College students living in hostels struggle to find meals that are affordable, healthy, nearby, and matched to their preferences.',
      target_customer: 'College students living in hostels near campus',
      solution: 'A discovery app that ranks nearby food options by price, nutrition, distance, and student preferences so students can choose healthier meals without overspending.',
      pain_points: [
        'Healthy meals near campus are hard to compare by price and nutrition',
        'Students often choose cheap food without knowing nutrition tradeoffs',
        'Hostel students have limited time, transport, and cooking options',
      ],
      assumptions: [
        'Students will use nutrition and price filters before deciding where to eat',
        'Nearby vendors will keep menu, price, and nutrition data updated',
      ],
      risks: [
        'Food listings may become outdated without vendor participation',
        'Large food delivery apps could add student-focused healthy meal filters',
      ],
      missing_information: [
        'Initial campus launch geography',
        'Vendor onboarding plan',
        'Student willingness to pay or monetization model',
      ],
      first_question: {
        id: `clarify-${Date.now()}`,
        text: 'Which campus or hostel cluster will you launch with first, and how will you verify menu prices and nutrition data?',
        target_field: 'market.summary',
        topic: 'market',
      },
    };
  }

  return {
    problem: ctx.profile.problem.statement || `Target customers need a clearer way to solve the problem described by: ${ctx.idea}`,
    target_customer: ctx.profile.customer.primary_segment || 'Initial target customer segment requires validation',
    solution: ctx.profile.solution.description || ctx.idea,
    pain_points: ctx.profile.problem.pain_points?.length ? ctx.profile.problem.pain_points : ['Customer pain points require validation'],
    assumptions: ctx.profile.assumptions?.map((a) => a.text) || [],
    risks: ctx.profile.risks?.map((r) => r.text) || [],
    missing_information: ['Target segment', 'Pricing model', 'Evidence of demand'],
    first_question: {
      id: `clarify-${Date.now()}`,
      text: 'Who is the first narrow customer segment, and what evidence proves this problem is urgent for them?',
      target_field: 'customer.primary_segment',
      topic: 'validation',
    },
  };
}

function generateValueProposition(ctx: ReturnType<typeof getContext>) {
  if (ctx.isFood) {
    return {
      one_line: `${ctx.name} helps hostel students find affordable, healthy meals near campus without guessing on price or nutrition.`,
      elevator: `For college students living in hostels who want healthy food without overspending, ${ctx.name} ranks nearby meals by price, nutrition, distance, and preferences so students can quickly choose better options.`,
      differentiation: 'Student-first ranking that combines affordability, nutrition, distance, and preferences instead of only showing restaurants by popularity or delivery speed.',
      advantage: 'Campus-level food data and student preference feedback can create a local recommendation loop that generic food apps do not optimize for.',
      target_segment: 'College students living in hostels near campus',
      customer_problem_alignment: 'They need frequent low-cost meals, have limited cooking options, and make daily food choices under time and budget pressure.',
      provenance: {
        one_line: 'ai_analysis',
        elevator: 'ai_analysis',
        differentiation: 'ai_analysis',
        advantage: 'founder_assumption',
        target_segment: 'founder_assumption',
      },
    };
  }

  return {
    one_line: ctx.profile.identity.one_liner || `${ctx.name} helps its target customers solve a validated, high-priority problem.`,
    elevator: `${ctx.name} is built around this thesis: ${ctx.idea}`,
    differentiation: ctx.profile.value_proposition.differentiation || 'Differentiation requires validation against alternatives.',
    advantage: ctx.profile.value_proposition.advantage || 'Defensibility requires more evidence.',
    target_segment: ctx.profile.customer.primary_segment || 'Target segment requires validation',
    customer_problem_alignment: ctx.profile.problem.statement || 'Problem-customer fit requires validation.',
    provenance: {},
  };
}

function fallbackMarketTier(label: string, value?: number | null, description?: string | null) {
  return {
    value: value || 0,
    formatted: value ? `$${value.toLocaleString()}` : 'Requires validation',
    description: description || `${label} sizing requires validation.`,
    calculation_steps: ['Define the launch segment', 'Estimate reachable customers', 'Validate conversion and pricing assumptions'],
    provenance: 'founder_assumption',
    sources: [],
  };
}

function generateMarket(ctx: ReturnType<typeof getContext>) {
  if (ctx.isFood) {
    return {
      tam: {
        value: 0,
        formatted: 'Requires validation',
        description: 'Total college student food spend across launchable campus markets.',
        calculation_steps: ['Estimate students living in hostels', 'Multiply by average monthly outside-food spend'],
        provenance: 'founder_assumption',
        sources: [],
      },
      sam: {
        value: 0,
        formatted: 'Requires validation',
        description: 'Students reachable in the first city or campus cluster.',
        calculation_steps: ['Select first launch campuses', 'Estimate reachable hostel students and nearby food vendors'],
        provenance: 'founder_assumption',
        sources: [],
      },
      som: {
        value: 0,
        formatted: 'Requires validation',
        description: 'First-year obtainable market from active student users and vendor partners.',
        calculation_steps: ['Target pilot hostels', 'Estimate weekly active users and monetization per user/vendor'],
        provenance: 'calculated',
        sources: [],
      },
      cagr: 0,
      growth_drivers: [
        'Students increasingly compare food options digitally before purchase',
        'Rising demand for affordable healthier meals near campuses',
        'Dense hostel clusters make campus-by-campus launches practical',
      ],
      market_risks: [
        'Vendor data quality may be hard to maintain',
        'Existing food delivery platforms can copy basic filtering features',
      ],
      assumptions: ['Students will trust nutrition and price data if it is accurate and frequently updated'],
    };
  }
  return {
    tam: fallbackMarketTier('TAM', null, 'Total addressable market requires validation.'),
    sam: fallbackMarketTier('SAM', null, 'Serviceable market requires a focused launch segment.'),
    som: fallbackMarketTier('SOM', null, 'Obtainable market requires pilot conversion assumptions.'),
    cagr: 0,
    growth_drivers: ['Customer demand and market growth drivers require validation'],
    market_risks: ['Competitive alternatives and adoption risks require validation'],
    assumptions: ['Market size assumptions need source-backed research'],
  };
}

function generateCompetitors(ctx: ReturnType<typeof getContext>) {
  if (ctx.isFood) {
    return {
      direct_competitors: [
        {
          name: 'Food delivery apps',
          description: 'Large delivery platforms with broad restaurant coverage.',
          strengths: ['Large vendor network', 'Strong brand awareness', 'Existing ordering behavior'],
          weaknesses: ['Optimized for ordering, not student nutrition decisions', 'Delivery fees can make daily meals expensive'],
          pricing: 'Delivery fee, commissions, restaurant pricing',
          market_share: 'High in urban food discovery and delivery',
          differentiator: `${ctx.name} focuses on hostel students choosing affordable healthy meals nearby, not just delivery convenience.`,
          provenance: 'ai_analysis',
          source_urls: [],
        },
        {
          name: 'Campus mess and canteens',
          description: 'Default food options for hostel students.',
          strengths: ['Convenient', 'Low-cost', 'Habitual student usage'],
          weaknesses: ['Limited variety', 'Nutrition transparency is low', 'Fixed menus and timings'],
          pricing: 'Low-cost daily meals',
          market_share: 'High within hostel routines',
          differentiator: `${ctx.name} helps students compare alternatives when mess food is repetitive or unhealthy.`,
          provenance: 'founder_assumption',
          source_urls: [],
        },
      ],
      indirect_competitors: [
        { name: 'Google Maps', description: 'Generic nearby food search without student nutrition or budget ranking.' },
      ],
      matrix_axes: {
        x_axis: 'Generic discovery -> Student-personalized ranking',
        y_axis: 'Convenience only -> Health and affordability',
      },
      competitor_positions: [
        { name: 'Delivery apps', x: -2, y: -1, is_self: false },
        { name: 'Campus canteen', x: -6, y: 2, is_self: false },
        { name: ctx.name, x: 7, y: 7, is_self: true },
      ],
    };
  }
  return {
    direct_competitors: [
      {
        name: 'Current alternatives',
        description: 'The existing way customers solve this problem today.',
        strengths: ['Already familiar to customers'],
        weaknesses: ['May not solve the problem completely'],
        pricing: 'Varies',
        market_share: 'Requires validation',
        differentiator: `${ctx.name} needs to prove a sharper wedge against current alternatives.`,
        provenance: 'ai_analysis',
        source_urls: [],
      },
    ],
    indirect_competitors: [],
    matrix_axes: {
      x_axis: 'Generic alternative -> Purpose-built solution',
      y_axis: 'Low urgency -> High urgency',
    },
    competitor_positions: [
      { name: 'Alternatives', x: -4, y: 0, is_self: false },
      { name: ctx.name, x: 5, y: 5, is_self: true },
    ],
  };
}

function generateBusinessModel(ctx: ReturnType<typeof getContext>) {
  if (ctx.isFood) {
    return {
      type: 'Campus marketplace and recommendation platform',
      revenue_streams: [
        {
          name: 'Vendor promoted listings',
          model_type: 'Local advertising / sponsored placement',
          price_point: 'Requires pilot validation',
          frequency: 'Monthly',
          margin: 'TBD',
          calculated: false,
          provenance: 'founder_assumption',
        },
        {
          name: 'Student premium filters',
          model_type: 'Optional subscription',
          price_point: 'Low-cost student plan TBD',
          frequency: 'Monthly',
          margin: 'TBD',
          calculated: false,
          provenance: 'founder_assumption',
        },
      ],
      pricing_tiers: [
        {
          tier_name: 'Student Free',
          price: 'Free',
          billing: 'Free access',
          features: ['Nearby meal discovery', 'Price and distance filters', 'Basic nutrition tags'],
          target_audience: 'Hostel students',
        },
        {
          tier_name: 'Vendor Partner',
          price: 'TBD',
          billing: 'Monthly',
          features: ['Menu listing', 'Student insights', 'Promoted healthy meal offers'],
          target_audience: 'Campus food vendors',
        },
      ],
      unit_economics: null,
      cost_structure: ['Vendor onboarding', 'Menu and nutrition data verification', 'Campus ambassador acquisition'],
    };
  }
  return {
    type: ctx.profile.business_model.type || 'Business model requires validation',
    revenue_streams: [
      {
        name: 'Primary revenue stream',
        model_type: ctx.profile.business_model.revenue_source || 'Revenue source requires validation',
        price_point: ctx.profile.business_model.pricing || 'Pricing requires validation',
        frequency: 'TBD',
        margin: 'TBD',
        calculated: false,
        provenance: 'founder_assumption',
      },
    ],
    pricing_tiers: [
      {
        tier_name: 'Initial offer',
        price: ctx.profile.business_model.pricing || 'TBD',
        billing: 'Requires validation',
        features: ['Core product access'],
        target_audience: ctx.profile.customer.primary_segment || 'Initial customer segment',
      },
    ],
    unit_economics: null,
    cost_structure: ctx.profile.business_model.costs ? [ctx.profile.business_model.costs] : [],
  };
}

function generatePitch(ctx: ReturnType<typeof getContext>) {
  const vp = generateValueProposition(ctx);
  const market = generateMarket(ctx);
  return {
    slides: [
      { key: 'problem', title: 'The Problem', status: 'complete', bullets: [ctx.isFood ? 'Hostel students struggle to find meals that are affordable, healthy, nearby, and preference-matched.' : (ctx.profile.problem.statement || ctx.idea)] },
      { key: 'solution', title: `The Solution: ${ctx.name}`, status: 'complete', bullets: [ctx.isFood ? `${ctx.name} ranks nearby food options by price, nutrition, distance, and student preferences.` : ctx.idea] },
      { key: 'product', title: 'Product Experience', status: 'complete', bullets: ['Personalized discovery', 'Comparison filters', 'Saved preferences and feedback loops'] },
      { key: 'target_market', title: 'Target Customer', status: 'complete', bullets: [vp.target_segment] },
      { key: 'market_opportunity', title: 'Market Opportunity', status: 'needs_input', bullets: [market.tam.description, market.sam.description, market.som.description] },
      { key: 'competition', title: 'Competition', status: 'complete', bullets: [ctx.isFood ? 'Competes with food delivery apps, campus mess/canteens, and generic map search.' : 'Competitive landscape requires validation.'] },
      { key: 'advantage', title: 'Differentiation', status: 'complete', bullets: [vp.differentiation, vp.advantage] },
      { key: 'business_model', title: 'Business Model', status: 'needs_input', bullets: [ctx.isFood ? 'Potential revenue from vendor partnerships, promoted listings, and optional student premium features.' : 'Pricing requires validation.'] },
      { key: 'gtm', title: 'Go-To-Market', status: 'needs_input', bullets: [ctx.isFood ? 'Launch campus-by-campus through hostel ambassadors and nearby vendor onboarding.' : 'Go-to-market plan requires validation.'] },
      { key: 'traction', title: 'Traction', status: 'needs_input', bullets: ['Add student interviews, pilot campus usage, vendor signups, and repeat usage metrics.'] },
      { key: 'team', title: 'Team', status: 'needs_input', bullets: ['Add founder background and relevant campus/vendor operations experience.'] },
      { key: 'ask', title: 'Ask', status: 'needs_input', bullets: ['Define funding ask, pilot milestones, and launch metrics.'] },
    ],
  };
}

function generateInvestorQuestion(ctx: ReturnType<typeof getContext>, parsedBody: Record<string, unknown>) {
  const topic = (parsedBody.topic as string) || 'validation';
  if (ctx.isFood) {
    return {
      id: `inv-q-${Date.now()}`,
      intent: parsedBody.intent || 'opening',
      topic,
      text: topic === 'business_model'
        ? 'Who pays in your model: students, food vendors, or both, and what evidence shows they will pay?'
        : 'How will you prove students trust your price and nutrition data enough to change where they eat?',
    };
  }
  return {
    id: `inv-q-${Date.now()}`,
    intent: parsedBody.intent || 'opening',
    topic,
    text: 'What evidence proves this problem is urgent enough that customers will switch from their current alternative?',
  };
}

function generateReadiness(ctx: ReturnType<typeof getContext>) {
  return {
    overall_score: 58,
    verdict: 'Promising but needs validation',
    executive_summary: ctx.isFood
      ? `${ctx.name} has a clear student pain point around affordable healthy food discovery, but needs campus pilot evidence, vendor onboarding proof, and a sharper monetization model before investor meetings.`
      : `${ctx.name} has a promising thesis but needs stronger evidence across customer validation, market sizing, and business model assumptions.`,
    criteria_scores: { clarity: 7, specificity: 6, evidence: 4, business_reasoning: 5, differentiation: 5, scalability: 6 },
    topic_coverage: { problem: 75, market: 45, differentiation: 50, business_model: 40, validation: 35 },
    top_strengths: ctx.isFood
      ? ['Clear daily-use student pain point', 'Focused initial customer segment', 'Potential for campus-by-campus rollout']
      : ['Clear initial concept'],
    critical_gaps: ctx.isFood
      ? ['Interview 30-50 hostel students', 'Validate vendor willingness to share accurate menu and nutrition data', 'Define who pays and why']
      : ['Validate customer demand', 'Define pricing', 'Map competitive alternatives'],
    action_items: ctx.isFood
      ? ['Run a hostel student survey', 'Pilot with 5-10 nearby food vendors', 'Measure weekly repeat usage and meal selection changes']
      : ['Run customer discovery', 'Build a simple pilot', 'Measure willingness to pay'],
    investor_verdict: 'Not ready for a formal raise yet; ready for structured validation and pilot milestones.',
  };
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
  if (endpoint.includes('/auth/login')) {
    data = {
      access_token: 'mock-jwt-token-demo-founder',
      token_type: 'bearer',
      expires_in: 3600,
    };
  } else if (endpoint.includes('/auth/register')) {
    data = {
      access_token: 'mock-jwt-token-demo-founder',
      token_type: 'bearer',
      expires_in: 3600,
    };
  } else if (endpoint.includes('/auth/me')) {
    data = {
      id: '00000000-0000-0000-0000-000000000001',
      email: (parsedBody.email as string) || 'founder@hyperscale.ai',
    };
  } else if (endpoint.includes('/startups') && method === 'GET') {
    data = mockStore.listStartups();
  } else if (endpoint.includes('/startups') && method === 'POST') {
    data = mockStore.createStartup(
      (parsedBody.name as string) || 'My New Startup',
      (parsedBody.raw_idea as string) || ''
    );
  } else if (endpoint.includes('/profile/') && method === 'GET') {
    const startupId = endpoint.split('/').pop() || 'hyperscale-ai-001';
    const profile = mockStore.getProfile(startupId);
    data = profile;
    meta.profile_version = profile.schema_version;
  } else if (endpoint.includes('/profile/') && method === 'PATCH') {
    const startupId = endpoint.split('/').pop() || 'hyperscale-ai-001';
    const ops = (parsedBody.ops || []) as any[];
    const expectedVer = parsedBody.expected_version as number | undefined;
    const profile = mockStore.patchProfile(startupId, ops, expectedVer);
    data = profile;
    meta.profile_version = profile.schema_version;
  }
  // AI capabilities
  else if (endpoint.includes('/ai/analyze_idea')) {
    data = generateIdeaAnalysis(getContext(parsedBody, endpoint));
  } else if (endpoint.includes('/ai/generate_clarification_question')) {
    const ctx = getContext(parsedBody, endpoint);
    data = {
      id: `clarify-${Date.now()}`,
      text: ctx.isFood
        ? 'Which campus/hostel cluster will you launch with first, and how will you collect accurate menu, price, and nutrition data?'
        : 'What is the most important missing detail investors would need to trust this startup thesis?',
      target_field: ctx.isFood ? 'market.summary' : 'customer.primary_segment',
      topic: ctx.isFood ? 'market' : 'validation',
    };
  } else if (endpoint.includes('/ai/extract_profile_patch')) {
    const ctx = getContext(parsedBody, endpoint);
    const answer = String(parsedBody.answer || '');
    data = {
      ops: [
        {
          op: 'set',
          path: ctx.isFood ? '/market/summary' : '/problem/statement',
          value: answer,
          reason: 'Extracted from founder clarification answer',
        },
      ],
    };
  } else if (endpoint.includes('/ai/generate_value_proposition')) {
    data = generateValueProposition(getContext(parsedBody, endpoint));
  } else if (endpoint.includes('/ai/analyze_competitors')) {
    data = generateCompetitors(getContext(parsedBody, endpoint));
  } else if (endpoint.includes('/ai/analyze_market')) {
    data = generateMarket(getContext(parsedBody, endpoint));
  } else if (endpoint.includes('/ai/analyze_business_model')) {
    data = generateBusinessModel(getContext(parsedBody, endpoint));
  } else if (endpoint.includes('/ai/generate_pitch')) {
    data = generatePitch(getContext(parsedBody, endpoint));
  } else if (endpoint.includes('/ai/critique_pitch')) {
    const ctx = getContext(parsedBody, endpoint);
    data = {
      overall_score: ctx.isFood ? 6.2 : 6,
      issues: [
        {
          slide_key: 'traction',
          severity: 'high',
          title: 'Validation evidence is still thin',
          explanation: ctx.isFood
            ? 'The pitch needs real student interview counts, vendor signups, and repeat usage from a campus pilot.'
            : 'The pitch needs stronger customer evidence.',
          suggestion: ctx.isFood
            ? 'Add survey results from hostel students and a vendor pilot plan.'
            : 'Add customer discovery and willingness-to-pay evidence.',
        },
      ],
      investor_objections: ctx.isFood
        ? ['Why will students use this instead of existing food delivery apps or Google Maps?', 'How will you keep price and nutrition data accurate?']
        : ['What proves customers will switch?'],
      top_priorities: ctx.isFood
        ? ['Run hostel student interviews', 'Validate vendor data workflow', 'Define monetization']
        : ['Validate demand', 'Define pricing'],
    };
  } else if (endpoint.includes('/ai/generate_investor_question')) {
    data = generateInvestorQuestion(getContext(parsedBody, endpoint), parsedBody);
  } else if (endpoint.includes('/ai/evaluate_answer')) {
    const answer = String(parsedBody.answer || '');
    const hasNumbers = /\d/.test(answer);
    data = {
      scores: {
        clarity: answer.length > 30 ? 7 : 5,
        specificity: hasNumbers ? 7 : 4,
        evidence: hasNumbers ? 6 : 3,
        business_reasoning: 6,
        differentiation: 5,
        scalability: 5,
      },
      explanation: hasNumbers
        ? 'The answer is clearer because it includes concrete details, but still needs stronger validation evidence.'
        : 'The answer is directionally useful but needs numbers, pilot evidence, and proof from users or vendors.',
      strengths: ['Addresses the question directly'],
      weaknesses: ['Needs more empirical evidence'],
      recommended_improvement: 'Add specific interview counts, pilot metrics, vendor commitments, or willingness-to-pay data.',
      weakest_criterion: 'evidence',
      claims_made: answer ? [answer] : [],
      follow_up_question: 'What concrete pilot result can you show to prove this?',
    };
  } else if (endpoint.includes('/ai/generate_readiness_narrative')) {
    data = generateReadiness(getContext(parsedBody, endpoint));
  } else if (endpoint.includes('/ai/extract_feedback_patches')) {
    const ctx = getContext(parsedBody, endpoint);
    data = {
      ops: [
        {
          op: 'set',
          path: ctx.isFood ? '/traction/interviews' : '/traction/notes',
          value: ctx.isFood ? 'Founder should add hostel student interview results here.' : 'Founder should add validation evidence here.',
          reason: 'Converted feedback into a profile validation field',
        },
      ],
    };
  } else {
    // Default fallback
    data = { success: true };
  }

  return {
    data: data as T,
    meta,
  };
}
