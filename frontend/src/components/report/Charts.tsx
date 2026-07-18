'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, BarChart, Bar, XAxis, YAxis, CartesianGrid } from 'recharts';

interface ChartsProps {
  passed: number;
  failed: number;
  issues: any[];
}

export function Charts({ passed, failed, issues }: ChartsProps) {
  const pieData = [
    { name: 'Passed', value: passed, color: '#22c55e' },
    { name: 'Failed', value: failed, color: '#ef4444' },
  ];

  // Group issues by category
  const categoryCount: Record<string, number> = {};
  issues.forEach(issue => {
    const cat = issue.category || 'General';
    categoryCount[cat] = (categoryCount[cat] || 0) + 1;
  });

  const barData = Object.keys(categoryCount).map(key => ({
    category: key,
    count: categoryCount[key]
  }));

  return (
    <div className="grid md:grid-cols-2 gap-8 mb-8">
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Pass / Fail Ratio</CardTitle>
        </CardHeader>
        <CardContent className="h-[300px]">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={pieData}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={100}
                paddingAngle={5}
                dataKey="value"
              >
                {pieData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Issues by Category</CardTitle>
        </CardHeader>
        <CardContent className="h-[300px]">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={barData} layout="vertical" margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" />
              <YAxis dataKey="category" type="category" width={80} />
              <Tooltip />
              <Bar dataKey="count" fill="#ef4444" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </div>
  );
}
