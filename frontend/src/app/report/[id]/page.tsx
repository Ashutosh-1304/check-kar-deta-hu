'use client';

import { useParams } from 'next/navigation';
import { useReport } from '@/lib/queries';
import { ComplianceScoreCard } from '@/components/report/ComplianceScoreCard';
import { Charts } from '@/components/report/Charts';
import { IssueTimeline } from '@/components/report/IssueTimeline';
import { Button } from '@/components/ui/button';
import { Download } from 'lucide-react';
import Link from 'next/link';
import { api } from '@/lib/api';

export default function ReportPage() {
  const params = useParams();
  const reportId = params?.id as string;
  const { data: report, isLoading, error } = useReport(reportId);

  if (isLoading || (report && report.status === 'VALIDATING')) {
    return (
      <div className="container mx-auto px-4 py-20 text-center">
        <h2 className="text-2xl font-semibold mb-4 animate-pulse">Analyzing Document...</h2>
        <p className="text-muted-foreground">Please wait while the compliance engine evaluates the document against the selected rules.</p>
      </div>
    );
  }

  if (error || !report) {
    return (
      <div className="container mx-auto px-4 py-20 text-center">
        <h2 className="text-2xl font-semibold text-red-500 mb-4">Error loading report</h2>
        <p className="text-muted-foreground">Could not fetch validation report {reportId}</p>
        <Link href="/">
            <Button className="mt-6">Back to Dashboard</Button>
        </Link>
      </div>
    );
  }

  const handleExport = () => {
    const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';
    window.open(`${API_BASE_URL}/reports/${reportId}/html`, '_blank');
  };

  return (
    <div className="container mx-auto px-4 py-8 max-w-6xl">
      <div className="flex justify-between items-center mb-8 border-b pb-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Compliance Report</h1>
          <p className="text-muted-foreground text-sm mt-1">ID: {reportId}</p>
        </div>
        <div className="flex gap-4">
          <Button variant="outline" onClick={handleExport}>
            <Download className="mr-2 h-4 w-4" />
            Export HTML
          </Button>
          <Link href="/">
            <Button>New Validation</Button>
          </Link>
        </div>
      </div>

      <ComplianceScoreCard 
        score={report.overall_score}
        totalChecks={report.metrics?.total_checks || 0}
        passedChecks={report.metrics?.passed_checks || 0}
        failedChecks={report.metrics?.failed_checks || 0}
      />

      <Charts 
        passed={report.metrics?.passed_checks || 0}
        failed={report.metrics?.failed_checks || 0}
        issues={report.issues || []}
      />

      <IssueTimeline issues={report.issues || []} />
    </div>
  );
}
