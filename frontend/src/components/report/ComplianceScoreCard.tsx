import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { ShieldAlert, ShieldCheck, FileWarning, Hash } from 'lucide-react';

interface ComplianceScoreCardProps {
  score: number;
  totalChecks: number;
  passedChecks: number;
  failedChecks: number;
}

export function ComplianceScoreCard({ score, totalChecks, passedChecks, failedChecks }: ComplianceScoreCardProps) {
  const isPerfect = score === 100;

  return (
    <div className="grid md:grid-cols-4 gap-4 mb-8">
      <Card className={`col-span-1 md:col-span-1 border-l-4 ${isPerfect ? 'border-l-green-500' : 'border-l-red-500'}`}>
        <CardHeader className="pb-2">
          <CardTitle className="text-sm font-medium text-muted-foreground">Overall Compliance</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-4xl font-bold">{score.toFixed(1)}%</div>
          <p className="text-xs text-muted-foreground mt-1">
            {isPerfect ? 'Perfect Score!' : 'Needs Revision'}
          </p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="flex flex-row items-center justify-between pb-2">
          <CardTitle className="text-sm font-medium text-muted-foreground">Total Checks</CardTitle>
          <Hash className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{totalChecks}</div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="flex flex-row items-center justify-between pb-2">
          <CardTitle className="text-sm font-medium text-muted-foreground">Passed</CardTitle>
          <ShieldCheck className="h-4 w-4 text-green-500" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{passedChecks}</div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="flex flex-row items-center justify-between pb-2">
          <CardTitle className="text-sm font-medium text-muted-foreground">Failed (Issues)</CardTitle>
          <ShieldAlert className="h-4 w-4 text-red-500" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{failedChecks}</div>
        </CardContent>
      </Card>
    </div>
  );
}
