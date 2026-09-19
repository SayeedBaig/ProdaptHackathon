import React from 'react';
import { Profile } from '../../types/profile';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { ProvenanceBadge } from '../../components/provenance/ProvenanceBadge';
import { renderNullSafe } from '../../components/ui/NullValue';
import { Badge } from '../../components/ui/Badge';
import {
  Sparkles,
  AlertCircle,
  Users,
  Lightbulb,
  DollarSign,
  TrendingUp,
  ShieldCheck,
  Building,
} from 'lucide-react';

interface ProfileFieldsProps {
  profile: Profile;
}

export const ProfileFields: React.FC<ProfileFieldsProps> = ({ profile }) => {
  const prov = profile.provenance || {};

  return (
    <div className="space-y-6">
      {/* 1. Identity & Overview */}
      <Card>
        <CardHeader>
          <div className="flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-brand-600" />
            <CardTitle>Startup Identity & Concept</CardTitle>
          </div>
          <div className="flex items-center gap-2">
            <Badge variant="brand" size="sm">
              Version {profile.schema_version}
            </Badge>
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <div className="flex items-center justify-between mb-1">
              <span className="text-xs font-bold uppercase tracking-wider text-slate-500">
                Startup Name
              </span>
              <ProvenanceBadge provenance={prov['identity.startup_name'] || 'source_backed'} />
            </div>
            <div className="text-xl font-bold text-slate-900">
              {profile.identity.startup_name}
            </div>
          </div>

          <div>
            <div className="flex items-center justify-between mb-1">
              <span className="text-xs font-bold uppercase tracking-wider text-slate-500">
                One-Liner / Value Statement
              </span>
              <ProvenanceBadge provenance={prov['identity.one_liner'] || 'ai_analysis'} />
            </div>
            <div className="text-base text-slate-700 bg-slate-50 p-3 rounded-lg border border-slate-100 italic">
              {renderNullSafe(profile.identity.one_liner)}
            </div>
          </div>

          <div>
            <div className="flex items-center justify-between mb-1">
              <span className="text-xs font-bold uppercase tracking-wider text-slate-500">
                Raw Idea / Founder Thesis
              </span>
              <ProvenanceBadge provenance={prov['identity.raw_idea'] || 'founder_assumption'} />
            </div>
            <p className="text-base text-slate-700 leading-relaxed">
              {renderNullSafe(profile.identity.raw_idea)}
            </p>
          </div>
        </CardContent>
      </Card>

      {/* 2. Problem & Solution 2-column grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Problem Card */}
        <Card>
          <CardHeader>
            <div className="flex items-center gap-2">
              <AlertCircle className="w-5 h-5 text-rose-500" />
              <CardTitle>Problem & Pain Points</CardTitle>
            </div>
            <ProvenanceBadge provenance={prov['problem.statement'] || 'source_backed'} />
          </CardHeader>
          <CardContent className="space-y-3">
            <div>
              <span className="text-xs font-bold uppercase text-slate-400 block mb-1">
                Statement
              </span>
              <p className="text-base text-slate-800">
                {renderNullSafe(profile.problem.statement)}
              </p>
            </div>

            <div>
              <span className="text-xs font-bold uppercase text-slate-400 block mb-1.5">
                Key Pain Points
              </span>
              {profile.problem.pain_points.length === 0 ? (
                renderNullSafe(null)
              ) : (
                <ul className="space-y-1.5 list-disc list-inside text-sm text-slate-700">
                  {profile.problem.pain_points.map((pt, i) => (
                    <li key={i} className="leading-snug">{pt}</li>
                  ))}
                </ul>
              )}
            </div>
          </CardContent>
        </Card>

        {/* Solution Card */}
        <Card>
          <CardHeader>
            <div className="flex items-center gap-2">
              <Lightbulb className="w-5 h-5 text-emerald-600" />
              <CardTitle>Solution & Key Features</CardTitle>
            </div>
            <ProvenanceBadge provenance={prov['solution.description'] || 'ai_analysis'} />
          </CardHeader>
          <CardContent className="space-y-3">
            <div>
              <span className="text-xs font-bold uppercase text-slate-400 block mb-1">
                Description
              </span>
              <p className="text-base text-slate-800">
                {renderNullSafe(profile.solution.description)}
              </p>
            </div>

            <div>
              <span className="text-xs font-bold uppercase text-slate-400 block mb-1.5">
                Core Features
              </span>
              {profile.solution.key_features.length === 0 ? (
                renderNullSafe(null)
              ) : (
                <ul className="space-y-1.5 list-disc list-inside text-sm text-slate-700">
                  {profile.solution.key_features.map((feat, i) => (
                    <li key={i} className="leading-snug">{feat}</li>
                  ))}
                </ul>
              )}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* 3. Customer & Persona */}
      <Card>
        <CardHeader>
          <div className="flex items-center gap-2">
            <Users className="w-5 h-5 text-indigo-600" />
            <CardTitle>Customer Segment & ICP Persona</CardTitle>
          </div>
          <ProvenanceBadge provenance={prov['customer.primary_segment'] || 'source_backed'} />
        </CardHeader>
        <CardContent className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <span className="text-xs font-bold uppercase text-slate-400 block mb-1">
              Primary Segment
            </span>
            <div className="text-base font-semibold text-slate-800">
              {renderNullSafe(profile.customer.primary_segment)}
            </div>
          </div>

          <div>
            <span className="text-xs font-bold uppercase text-slate-400 block mb-1">
              Target Persona / Title
            </span>
            <div className="text-base font-semibold text-slate-800">
              {renderNullSafe(profile.customer.persona)}
            </div>
          </div>

          <div className="md:col-span-2">
            <span className="text-xs font-bold uppercase text-slate-400 block mb-1.5">
              Sub-Segments / Use Cases
            </span>
            {profile.customer.segments.length === 0 ? (
              renderNullSafe(null)
            ) : (
              <div className="flex flex-wrap gap-2">
                {profile.customer.segments.map((seg, i) => (
                  <Badge key={i} variant="default" size="sm">
                    {seg}
                  </Badge>
                ))}
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      {/* 4. Business Model & Traction Highlights */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Business Model */}
        <Card>
          <CardHeader>
            <div className="flex items-center gap-2">
              <DollarSign className="w-5 h-5 text-purple-600" />
              <CardTitle>Business Model & Pricing</CardTitle>
            </div>
            <ProvenanceBadge provenance={prov['business_model.pricing'] || 'calculated'} />
          </CardHeader>
          <CardContent className="space-y-3 text-sm">
            <div>
              <span className="text-xs font-bold uppercase text-slate-400 block">Model Type</span>
              <div className="font-semibold text-slate-800">{renderNullSafe(profile.business_model.type)}</div>
            </div>
            <div>
              <span className="text-xs font-bold uppercase text-slate-400 block">Pricing Structure</span>
              <div className="text-slate-700">{renderNullSafe(profile.business_model.pricing)}</div>
            </div>
            <div>
              <span className="text-xs font-bold uppercase text-slate-400 block">Cost Structure</span>
              <div className="text-slate-700">{renderNullSafe(profile.business_model.costs)}</div>
            </div>
            <div>
              <span className="text-xs font-bold uppercase text-slate-400 block">GTM Channel</span>
              <div className="text-slate-700">{renderNullSafe(profile.business_model.go_to_market)}</div>
            </div>
          </CardContent>
        </Card>

        {/* Traction */}
        <Card>
          <CardHeader>
            <div className="flex items-center gap-2">
              <TrendingUp className="w-5 h-5 text-emerald-600" />
              <CardTitle>Validation & Traction</CardTitle>
            </div>
            <ProvenanceBadge provenance={prov['traction.users'] || 'source_backed'} />
          </CardHeader>
          <CardContent className="space-y-3 text-sm">
            <div className="grid grid-cols-2 gap-2">
              <div>
                <span className="text-xs font-bold uppercase text-slate-400 block">Discovery</span>
                <div className="font-medium text-slate-800">{renderNullSafe(profile.traction.interviews)}</div>
              </div>
              <div>
                <span className="text-xs font-bold uppercase text-slate-400 block">Active Pilots</span>
                <div className="font-medium text-slate-800">{renderNullSafe(profile.traction.users)}</div>
              </div>
            </div>
            <div>
              <span className="text-xs font-bold uppercase text-slate-400 block">Revenue / Pipeline</span>
              <div className="font-medium text-slate-800">{renderNullSafe(profile.traction.revenue)}</div>
            </div>
            <div>
              <span className="text-xs font-bold uppercase text-slate-400 block">Traction Notes</span>
              <div className="text-slate-700">{renderNullSafe(profile.traction.notes)}</div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* 5. Assumptions & Risks */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <div className="flex items-center gap-2">
              <ShieldCheck className="w-5 h-5 text-amber-500" />
              <CardTitle>Core Assumptions</CardTitle>
            </div>
          </CardHeader>
          <CardContent className="space-y-2">
            {profile.assumptions.length === 0 ? (
              renderNullSafe(null)
            ) : (
              profile.assumptions.map((asm) => (
                <div key={asm.id} className="p-2.5 rounded-lg bg-slate-50 border border-slate-100 flex items-start justify-between gap-2">
                  <span className="text-sm text-slate-700 leading-snug">{asm.text}</span>
                  <Badge
                    variant={asm.status === 'validated' ? 'success' : 'warning'}
                    size="sm"
                  >
                    {asm.status}
                  </Badge>
                </div>
              ))
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <div className="flex items-center gap-2">
              <Building className="w-5 h-5 text-rose-500" />
              <CardTitle>Critical Risks</CardTitle>
            </div>
          </CardHeader>
          <CardContent className="space-y-2">
            {profile.risks.length === 0 ? (
              renderNullSafe(null)
            ) : (
              profile.risks.map((risk) => (
                <div key={risk.id} className="p-2.5 rounded-lg bg-slate-50 border border-slate-100 flex items-start justify-between gap-2">
                  <span className="text-sm text-slate-700 leading-snug">{risk.text}</span>
                  <Badge
                    variant={risk.severity === 'high' ? 'danger' : 'warning'}
                    size="sm"
                  >
                    {risk.severity} risk
                  </Badge>
                </div>
              ))
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};
