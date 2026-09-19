import { FeedbackStatus, GapStatus, Topic } from '../types/contracts';
import { Profile, StartupSummary, Gap } from '../types/profile';
import { FeedbackItemDraft, Pitch, ProfilePatchOp } from '../types/capabilities';
import pitchFixture from './fixtures/generate_pitch.json';

const SAMPLE_STARTUP_ID = 'hyperscale-ai-001';

export const INITIAL_SAMPLE_PROFILE: Profile = {
  id: SAMPLE_STARTUP_ID,
  schema_version: 3,
  identity: {
    startup_name: 'HyperScale AI',
    raw_idea: 'Autonomous Kubernetes infrastructure optimization agent that analyzes real-time telemetry to right-size CPU/RAM allocations, reducing cloud bills by 35% with zero downtime.',
    one_liner: 'Autonomous Kubernetes optimization that slashes cloud bills by 35% with zero human tuning.',
  },
  problem: {
    statement: 'Enterprises running Kubernetes routinely over-provision cluster compute by 40-60% to avoid outages, while DevOps teams are overwhelmed by passive FinOps alerts and manual pod tuning.',
    pain_points: [
      'Engineers spend 10+ hours per week manually tuning Kubernetes HPA and resource limits',
      'Cloud bills regularly exceed quarterly forecasts by 30-40%',
      'Over-provisioning is the default fear response because downtime damages customer SLAs',
    ],
  },
  customer: {
    primary_segment: 'Mid-market & Enterprise Cloud-Native Engineering Teams',
    persona: 'Head of Platform / Lead Site Reliability Engineer managing 20+ Kubernetes clusters',
    segments: [
      'B2B SaaS companies ($20k-$200k/mo cloud spend)',
      'Fintech and Payment Processors with high throughput volatility',
      'AI & ML inference API providers with spikey GPU/CPU loads',
    ],
  },
  solution: {
    description: 'An autonomous reinforcement-learning agent deployed via a single Helm chart that continuously monitors pod telemetry and non-disruptively applies predictive right-sizing recommendations in real-time.',
    key_features: [
      'Zero-downtime predictive pod right-sizing',
      'Automated cluster bin-packing and node defragmentation',
      'Instant 1-click rollback and sandbox simulation',
      'Multi-cloud support across AWS EKS, GCP GKE, and Azure AKS',
    ],
  },
  value_proposition: {
    one_line: 'Autonomous Kubernetes optimization that slashes cloud bills by 35% with zero human tuning.',
    elevator: 'For DevOps teams struggling with ballooning AWS and GCP infrastructure bills, HyperScale AI is an autonomous agent that continuously right-sizes pod resource allocations in real time. Unlike static cost dashboards like Datadog or CloudHealth that only generate alert fatigue, HyperScale AI takes safe, automated actions with instant rollback guarantees.',
    differentiation: 'Closed-loop reinforcement learning agent that acts directly on telemetry rather than generating manual ticket backlogs.',
    advantage: 'Proprietary predictive workload model trained on 50M+ container telemetry hours, achieving sub-minute right-sizing without restart evictions.',
  },
  market: {
    summary: 'The FinOps and cloud cost management market is expanding at 24.8% CAGR toward $28.5B by 2028, driven by enterprise cloud cost mandates and the sheer complexity of multi-cloud Kubernetes architectures.',
    size_inputs: {
      customers: '50,000 global enterprise accounts',
      price: '$30,000 average annual contract',
      frequency: 'Annual recurring subscription',
    },
  },
  competitor_summary: [
    { name: 'Kubecost', competitor_id: 'comp-1' },
    { name: 'Cast AI', competitor_id: 'comp-2' },
    { name: 'Datadog Cloud Cost', competitor_id: 'comp-3' },
  ],
  business_model: {
    type: 'B2B SaaS with Value-Share Hybrid Pricing',
    customer: 'VP of Engineering, Head of Infrastructure, CFO',
    payer: 'Engineering & Infrastructure budget',
    revenue_source: 'Platform subscription + percentage of verified net cloud savings',
    pricing: '$18/node/month + 12% of verified cloud savings beyond baseline',
    costs: 'Telemetry ingestion cloud compute (8%), Sales & DevRel (38%), Engineering (42%)',
    go_to_market: 'Developer-led bottoms-up open source benchmark CLI + cloud marketplace co-selling',
  },
  traction: {
    interviews: '42 customer discovery interviews with DevOps leads',
    interested: '18 qualified prospects in pipeline',
    users: '8 active production pilots managing 320 nodes',
    revenue: '$0 MRR during closed beta ($240K qualified pipeline)',
    partnerships: 'AWS Partner Network member; GCP Marketplace listing in progress',
    notes: 'Zero downtime incidents across all active customer clusters over 4 months of automated operation.',
  },
  team: {
    founder_ceo: 'Alex Vance (Ex-AWS Kubernetes SRE lead)',
    founder_cto: 'Dr. Maya Lin (PhD in Distributed Systems; Ex-Google Cloud ML)',
  },
  funding_ask: {
    amount: '$2,000,000',
    round: 'Seed',
    use_of_funds: '65% Engineering & ML R&D, 25% GTM & DevRel, 10% SOC2 Compliance',
    target_milestones: 'Reach $1.2M ARR and 50 enterprise customers within 15 months',
  },
  assumptions: [
    {
      id: 'asm-1',
      text: 'Enterprise DevOps teams will grant autonomous write permissions to an AI agent if dry-run audit logs and rollback safety are proven.',
      status: 'validated',
      source: 'founder',
    },
    {
      id: 'asm-2',
      text: 'AWS and Google Cloud will not release a native zero-touch pod right-sizer that works seamlessly across multi-cloud.',
      status: 'unvalidated',
      source: 'ai',
    },
  ],
  risks: [
    {
      id: 'risk-1',
      text: 'Misconfiguration in pod limits could trigger cascading evictions or latency spikes under unexpected traffic surges.',
      severity: 'high',
      source: 'founder',
    },
    {
      id: 'risk-2',
      text: 'Long enterprise security review cycles regarding cluster agent permissions.',
      severity: 'med',
      source: 'ai',
    },
  ],
  gaps: [
    {
      id: 'gap-1',
      topic: 'business_model',
      text: 'Determine exact gain-share audit methodology: how to mathematically separate HyperScale savings from seasonal organic traffic drops.',
      severity: 4,
      status: 'open',
      raised_by: 'idea_analysis',
    },
    {
      id: 'gap-2',
      topic: 'validation',
      text: 'Convert top 3 pilot customers from free beta to binding paid Letters of Intent (LOIs) with committed ACV.',
      severity: 5,
      status: 'open',
      raised_by: 'critique',
    },
    {
      id: 'gap-3',
      topic: 'differentiation',
      text: 'Quantify engineering hours saved per week directly from pilot feedback to prove operational ROI beyond cloud cost savings.',
      severity: 3,
      status: 'resolved',
      raised_by: 'investor',
    },
  ],
  provenance: {
    'identity.startup_name': 'source_backed',
    'identity.raw_idea': 'founder_assumption',
    'identity.one_liner': 'ai_analysis',
    'problem.statement': 'source_backed',
    'customer.primary_segment': 'source_backed',
    'solution.description': 'ai_analysis',
    'value_proposition.one_line': 'ai_analysis',
    'value_proposition.advantage': 'founder_assumption',
    'market.summary': 'source_backed',
    'business_model.pricing': 'calculated',
    'business_model.costs': 'calculated',
    'traction.users': 'source_backed',
  },
};

export const INITIAL_SAMPLE_FEEDBACK: FeedbackItemDraft[] = [
  {
    id: 'fb-001',
    topic: 'differentiation',
    title: 'Validate telemetry defensibility with benchmark data',
    description: 'Investors will push hard on defensibility against Datadog. Incorporate proprietary synthetic stress-test data and telemetry network effect claims into your advantage slide.',
    source: 'critique',
    status: 'accepted',
    suggested_patch: {
      ops: [
        {
          op: 'set',
          path: '/value_proposition/advantage',
          value: 'Proprietary predictive workload model trained on 50M+ container telemetry hours, achieving sub-minute right-sizing without restart evictions.',
          reason: 'Enhanced defensibility wording',
        },
      ],
    },
  },
  {
    id: 'fb-002',
    topic: 'validation',
    title: 'Quantify pilot pipeline terms and LOI status',
    description: 'Traction slide mentions 8 pilots but is vague on commercial commitment. Add dollar-weighted pipeline and letters of intent.',
    source: 'critique',
    status: 'open',
    suggested_patch: {
      ops: [
        {
          op: 'set',
          path: '/traction/notes',
          value: '8 active production pilots managing 320 nodes across AWS/GCP, representing $240K in qualified pipeline ARR with 3 signed enterprise LOIs.',
          reason: 'Clarified traction pipeline',
        },
      ],
    },
  },
  {
    id: 'fb-003',
    topic: 'business_model',
    title: 'Clarify gain-share baseline audit calculation',
    description: 'Ensure the contract methodology for determining verified savings is crystal clear so enterprise procurement does not view it as opaque.',
    source: 'investor',
    status: 'open',
    suggested_patch: null,
  },
  {
    id: 'fb-004',
    topic: 'market',
    title: 'Exclude on-prem legacy virtualization from SAM calculation',
    description: 'Focus strictly on cloud-native containerized workloads to keep the pitch laser-focused.',
    source: 'peer',
    status: 'done',
    suggested_patch: null,
  },
];

class MockStore {
  private startups: StartupSummary[] = [
    {
      id: SAMPLE_STARTUP_ID,
      name: 'HyperScale AI',
      one_liner: 'Autonomous Kubernetes optimization that slashes cloud bills by 35% with zero human tuning.',
      updated_at: new Date().toISOString(),
      profile_version: 3,
    },
  ];

  private profiles: Map<string, Profile> = new Map([
    [SAMPLE_STARTUP_ID, JSON.parse(JSON.stringify(INITIAL_SAMPLE_PROFILE))],
  ]);

  private feedbackItems: FeedbackItemDraft[] = JSON.parse(
    JSON.stringify(INITIAL_SAMPLE_FEEDBACK)
  );

  private pitchDeck: Pitch = JSON.parse(JSON.stringify(pitchFixture));

  // Reset entire mock state to rich sample (Safety net for demo)
  public resetToSample(): void {
    this.profiles.set(
      SAMPLE_STARTUP_ID,
      JSON.parse(JSON.stringify(INITIAL_SAMPLE_PROFILE))
    );
    this.feedbackItems = JSON.parse(JSON.stringify(INITIAL_SAMPLE_FEEDBACK));
    this.pitchDeck = JSON.parse(JSON.stringify(pitchFixture));
    this.startups = [
      {
        id: SAMPLE_STARTUP_ID,
        name: 'HyperScale AI',
        one_liner: 'Autonomous Kubernetes optimization that slashes cloud bills by 35% with zero human tuning.',
        updated_at: new Date().toISOString(),
        profile_version: 3,
      },
    ];
  }

  public listStartups(): StartupSummary[] {
    return [...this.startups];
  }

  public createStartup(name: string, raw_idea: string): StartupSummary {
    const id = `startup-${Date.now().toString(36)}`;
    const newSummary: StartupSummary = {
      id,
      name,
      one_liner: null,
      updated_at: new Date().toISOString(),
      profile_version: 1,
    };
    this.startups.unshift(newSummary);

    const newProfile: Profile = {
      id,
      schema_version: 1,
      identity: {
        startup_name: name,
        raw_idea,
        one_liner: null,
      },
      problem: { statement: null, pain_points: [] },
      customer: { primary_segment: null, persona: null, segments: [] },
      solution: { description: null, key_features: [] },
      value_proposition: {
        one_line: null,
        elevator: null,
        differentiation: null,
        advantage: null,
      },
      market: {
        summary: null,
        size_inputs: { customers: null, price: null, frequency: null },
      },
      competitor_summary: [],
      business_model: {
        type: null,
        customer: null,
        payer: null,
        revenue_source: null,
        pricing: null,
        costs: null,
        go_to_market: null,
      },
      traction: {
        interviews: null,
        interested: null,
        users: null,
        revenue: null,
        partnerships: null,
        notes: null,
      },
      team: null,
      funding_ask: null,
      assumptions: [],
      risks: [],
      gaps: [],
      provenance: {},
    };
    this.profiles.set(id, newProfile);
    return newSummary;
  }

  public getProfile(startupId: string): Profile {
    const p = this.profiles.get(startupId);
    if (!p) {
      // Auto create or fallback to sample
      return JSON.parse(JSON.stringify(INITIAL_SAMPLE_PROFILE));
    }
    return JSON.parse(JSON.stringify(p));
  }

  public patchProfile(
    startupId: string,
    ops: ProfilePatchOp[],
    expectedVersion?: number
  ): Profile {
    const profile = this.profiles.get(startupId) || this.profiles.get(SAMPLE_STARTUP_ID)!;

    if (expectedVersion !== undefined && profile.schema_version !== expectedVersion) {
      // Version conflict simulated if mismatched
      const err = new Error('Profile schema version conflict');
      (err as unknown as { code: string }).code = 'VERSION_CONFLICT';
      throw err;
    }

    for (const op of ops) {
      this.applyOp(profile, op);
    }

    profile.schema_version += 1;
    this.profiles.set(startupId, profile);

    // Update startup summary
    const s = this.startups.find((item) => item.id === startupId);
    if (s) {
      s.profile_version = profile.schema_version;
      s.updated_at = new Date().toISOString();
      if (profile.identity.one_liner) {
        s.one_liner = profile.identity.one_liner;
      }
    }

    return JSON.parse(JSON.stringify(profile));
  }

  private applyOp(profile: Profile, op: ProfilePatchOp): void {
    const parts = op.path.replace(/^\//, '').split('/');
    let curr: Record<string, unknown> = profile as unknown as Record<string, unknown>;
    for (let i = 0; i < parts.length - 1; i++) {
      const part = parts[i];
      if (!curr[part]) {
        curr[part] = {};
      }
      curr = curr[part] as Record<string, unknown>;
    }
    const finalKey = parts[parts.length - 1];

    if (op.op === 'set') {
      curr[finalKey] = op.value;
      profile.provenance[op.path.replace(/^\//, '').replace(/\//g, '.')] = 'ai_analysis';
    } else if (op.op === 'add' && Array.isArray(curr[finalKey])) {
      (curr[finalKey] as unknown[]).push(op.value);
    } else if (op.op === 'remove' && Array.isArray(curr[finalKey])) {
      curr[finalKey] = (curr[finalKey] as unknown[]).filter((x) => x !== op.value);
    }
  }

  public getFeedbackItems(): FeedbackItemDraft[] {
    return [...this.feedbackItems];
  }

  public updateFeedbackStatus(id: string, status: FeedbackStatus): void {
    const item = this.feedbackItems.find((f) => f.id === id);
    if (item) {
      item.status = status;
    }
  }

  public toggleGapStatus(startupId: string, gapId: string): void {
    const profile = this.profiles.get(startupId) || this.profiles.get(SAMPLE_STARTUP_ID);
    if (profile) {
      const gap = profile.gaps.find((g) => g.id === gapId);
      if (gap) {
        gap.status = (gap.status === 'open' ? 'resolved' : 'open') as GapStatus;
        profile.schema_version += 1;
      }
    }
  }

  public addGap(startupId: string, gap: Gap): void {
    const profile = this.profiles.get(startupId) || this.profiles.get(SAMPLE_STARTUP_ID);
    if (profile) {
      profile.gaps.push(gap);
      profile.schema_version += 1;
    }
  }

  public getPitch(): Pitch {
    return JSON.parse(JSON.stringify(this.pitchDeck));
  }
}

export const mockStore = new MockStore();
