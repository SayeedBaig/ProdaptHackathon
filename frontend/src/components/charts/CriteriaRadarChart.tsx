import React from 'react';
import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
  Tooltip,
} from 'recharts';
import { CriteriaKey, CRITERIA_LABELS } from '../../types/contracts';

interface CriteriaRadarChartProps {
  scores: Record<CriteriaKey, number>;
  height?: number;
}

export const CriteriaRadarChart: React.FC<CriteriaRadarChartProps> = ({
  scores,
  height = 320,
}) => {
  const data = (Object.keys(scores) as CriteriaKey[]).map((key) => ({
    criterion: CRITERIA_LABELS[key] || key,
    score: scores[key],
    fullMark: 10,
  }));

  return (
    <div className="w-full flex justify-center items-center select-none" style={{ height }}>
      <ResponsiveContainer width="100%" height="100%">
        <RadarChart cx="50%" cy="50%" outerRadius="75%" data={data}>
          <PolarGrid stroke="#e2e8f0" strokeDasharray="3 3" />
          <PolarAngleAxis
            dataKey="criterion"
            tick={{ fill: '#334155', fontSize: 12, fontWeight: 600 }}
          />
          <PolarRadiusAxis
            angle={30}
            domain={[0, 10]}
            tick={{ fill: '#94a3b8', fontSize: 10 }}
          />
          <Radar
            name="Score (0-10)"
            dataKey="score"
            stroke="#4f46e5"
            fill="#6366f1"
            fillOpacity={0.45}
          />
          <Tooltip
            formatter={(value: any) => [`${value} / 10`, 'Score']}
            contentStyle={{
              backgroundColor: '#0f172a',
              borderRadius: '8px',
              border: 'none',
              color: '#ffffff',
              fontSize: '12px',
            }}
          />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
};
