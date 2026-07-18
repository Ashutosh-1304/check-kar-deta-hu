'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { useCreateRule } from '@/lib/queries';

export function RuleEditor() {
  const createMutation = useCreateRule();
  const [jsonMode, setJsonMode] = useState(false);
  const [jsonText, setJsonText] = useState('');

  const { register, handleSubmit, reset } = useForm({
    defaultValues: {
      name: '',
      description: '',
      margins: { top: 1.0, bottom: 1.0, left: 1.0, right: 1.0 },
      font: { family: 'Times New Roman', size: 12 },
    },
  });

  const onSubmit = async (data: any) => {
    try {
      await createMutation.mutateAsync(data);
      reset();
      alert('Rule created successfully!');
    } catch (e) {
      console.error(e);
      alert('Failed to create rule.');
    }
  };

  const handleJsonSubmit = async () => {
    try {
      const data = JSON.parse(jsonText);
      await createMutation.mutateAsync(data);
      setJsonText('');
      alert('Rule created successfully!');
    } catch (e) {
      console.error(e);
      alert('Invalid JSON or server error.');
    }
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>Create Rule Template</CardTitle>
        <CardDescription>Define the compliance constraints for documents.</CardDescription>
      </CardHeader>
      <CardContent>
        <Tabs defaultValue="form">
          <TabsList className="mb-4">
            <TabsTrigger value="form">Form Editor</TabsTrigger>
            <TabsTrigger value="json">JSON Editor</TabsTrigger>
          </TabsList>
          
          <TabsContent value="form">
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
              <div className="space-y-4">
                <div>
                  <Label>Rule Name</Label>
                  <Input {...register('name')} required placeholder="e.g. Standard Corporate Policy" />
                </div>
                <div>
                  <Label>Description</Label>
                  <Input {...register('description')} placeholder="Brief description..." />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-4 border p-4 rounded-md">
                  <h3 className="font-semibold text-sm">Margins (inches)</h3>
                  <div>
                    <Label>Top</Label>
                    <Input type="number" step="0.1" {...register('margins.top', { valueAsNumber: true })} />
                  </div>
                  <div>
                    <Label>Bottom</Label>
                    <Input type="number" step="0.1" {...register('margins.bottom', { valueAsNumber: true })} />
                  </div>
                  <div>
                    <Label>Left</Label>
                    <Input type="number" step="0.1" {...register('margins.left', { valueAsNumber: true })} />
                  </div>
                  <div>
                    <Label>Right</Label>
                    <Input type="number" step="0.1" {...register('margins.right', { valueAsNumber: true })} />
                  </div>
                </div>

                <div className="space-y-4 border p-4 rounded-md">
                  <h3 className="font-semibold text-sm">Global Font</h3>
                  <div>
                    <Label>Font Family</Label>
                    <Input {...register('font.family')} />
                  </div>
                  <div>
                    <Label>Font Size (pt)</Label>
                    <Input type="number" {...register('font.size', { valueAsNumber: true })} />
                  </div>
                </div>
              </div>

              <Button type="submit" disabled={createMutation.isPending}>
                Save Rule Template
              </Button>
            </form>
          </TabsContent>

          <TabsContent value="json">
            <div className="space-y-4">
              <textarea
                className="w-full h-64 p-4 font-mono text-sm border rounded-md bg-accent/20"
                value={jsonText}
                onChange={(e) => setJsonText(e.target.value)}
                placeholder="Paste JSON rule definition here..."
              />
              <Button onClick={handleJsonSubmit} disabled={createMutation.isPending || !jsonText}>
                Import JSON Rule
              </Button>
            </div>
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  );
}
