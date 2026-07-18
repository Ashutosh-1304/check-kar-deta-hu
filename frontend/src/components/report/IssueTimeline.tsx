'use client';

import { useRef } from 'react';
import { useVirtualizer } from '@tanstack/react-virtual';
import { Card, CardContent } from '@/components/ui/card';
import { AlertCircle, AlertTriangle } from 'lucide-react';

interface IssueTimelineProps {
  issues: any[];
}

export function IssueTimeline({ issues }: IssueTimelineProps) {
  const parentRef = useRef<HTMLDivElement>(null);

  const rowVirtualizer = useVirtualizer({
    count: issues.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 140, // Estimated pixel height of each issue card
    overscan: 5,
  });

  if (issues.length === 0) {
    return (
      <div className="p-8 text-center border rounded-lg bg-accent/20">
        <h3 className="font-semibold text-lg">No Issues Found</h3>
        <p className="text-muted-foreground">The document complies perfectly with the template.</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">Violation Timeline</h2>
      <div 
        ref={parentRef} 
        className="h-[600px] overflow-auto rounded-md border bg-background"
      >
        <div
          style={{
            height: `${rowVirtualizer.getTotalSize()}px`,
            width: '100%',
            position: 'relative',
          }}
        >
          {rowVirtualizer.getVirtualItems().map((virtualItem) => {
            const issue = issues[virtualItem.index];
            const isError = issue.severity === 'ERROR';

            return (
              <div
                key={virtualItem.key}
                style={{
                  position: 'absolute',
                  top: 0,
                  left: 0,
                  width: '100%',
                  height: `${virtualItem.size}px`,
                  transform: `translateY(${virtualItem.start}px)`,
                }}
                className="p-2"
              >
                <Card className={`h-full border-l-4 ${isError ? 'border-l-red-500 bg-red-500/5' : 'border-l-orange-500 bg-orange-500/5'}`}>
                  <CardContent className="p-4 flex gap-4 h-full">
                    <div className="mt-1">
                      {isError ? <AlertCircle className="h-5 w-5 text-red-500" /> : <AlertTriangle className="h-5 w-5 text-orange-500" />}
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex justify-between items-start mb-1">
                        <h4 className="font-semibold text-sm truncate uppercase tracking-wider">{issue.element_type || issue.category}</h4>
                        <span className="text-xs font-mono bg-background px-2 py-1 rounded border">Page {issue.page || 1}</span>
                      </div>
                      <div className="grid md:grid-cols-2 gap-4 text-sm mt-2">
                        <div>
                          <span className="text-muted-foreground text-xs uppercase block">Expected</span>
                          <span className="font-medium">{issue.expected_value || issue.expected || 'N/A'}</span>
                        </div>
                        <div>
                          <span className="text-muted-foreground text-xs uppercase block">Actual</span>
                          <span className="font-medium">{issue.actual_value || issue.actual || 'N/A'}</span>
                        </div>
                      </div>
                      {(issue.message || issue.suggestion) && (
                        <div className="mt-3 text-xs bg-background/50 p-2 rounded inline-block text-muted-foreground">
                          💡 Suggestion: {issue.message || issue.suggestion}
                        </div>
                      )}
                    </div>
                  </CardContent>
                </Card>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
