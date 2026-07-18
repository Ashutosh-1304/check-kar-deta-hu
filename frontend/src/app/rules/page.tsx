import { RuleEditor } from '@/components/rules/RuleEditor';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

export default function RulesPage() {
  return (
    <div className="container mx-auto px-4 py-8 max-w-5xl">
      <div className="mb-8">
        <h1 className="text-3xl font-bold tracking-tight mb-2">Rule Templates</h1>
        <p className="text-muted-foreground">
          Create and manage compliance profiles to enforce document standards across the organization.
        </p>
      </div>

      <div className="grid lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2">
          <RuleEditor />
        </div>
        
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">About Rules</CardTitle>
              <CardDescription>How the compliance engine uses templates</CardDescription>
            </CardHeader>
            <CardContent className="text-sm text-muted-foreground space-y-4">
              <p>
                Rule templates dictate the exact structural requirements a DOCX document must adhere to.
              </p>
              <p>
                When a document is uploaded on the dashboard, it is executed against the selected template via a strict Chain of Responsibility validation pipeline.
              </p>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
