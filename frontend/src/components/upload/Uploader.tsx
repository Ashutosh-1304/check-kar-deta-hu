'use client';

import { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { UploadCloud, File, AlertCircle, CheckCircle2 } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { useUploadDocument, useRules, useValidateDocument } from '@/lib/queries';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { useRouter } from 'next/navigation';

export function Uploader() {
  const router = useRouter();
  const [file, setFile] = useState<File | null>(null);
  const [selectedRuleId, setSelectedRuleId] = useState<string>('');
  
  const { data: rules, isLoading: rulesLoading } = useRules();
  const uploadMutation = useUploadDocument();
  const validateMutation = useValidateDocument();

  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      setFile(acceptedFiles[0]);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
    },
    maxFiles: 1,
  });

  const handleProcess = async () => {
    if (!file || !selectedRuleId) return;

    try {
      const uploadRes = await uploadMutation.mutateAsync(file);
      const validateRes = await validateMutation.mutateAsync({
        documentId: uploadRes.document_id,
        ruleTemplateId: parseInt(selectedRuleId),
      });

      // Redirect to report view
      router.push(`/report/${validateRes.report_id}`);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <Card className="w-full max-w-2xl mx-auto mt-8">
      <CardHeader>
        <CardTitle>Upload Document</CardTitle>
        <CardDescription>Upload a .docx file to validate against your compliance rules.</CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        
        <div className="space-y-2">
          <label className="text-sm font-medium">Select Rule Template</label>
          <Select value={selectedRuleId} onValueChange={(val) => setSelectedRuleId(val || '')} disabled={rulesLoading}>
            <SelectTrigger>
              <SelectValue placeholder="Select a rule template..." />
            </SelectTrigger>
            <SelectContent>
              {rules?.map((r: any) => (
                <SelectItem key={r.id} value={r.id}>
                  {r.name} (v{r.version})
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <div
          {...getRootProps()}
          className={`border-2 border-dashed rounded-lg p-10 flex flex-col items-center justify-center cursor-pointer transition-colors ${
            isDragActive ? 'border-primary bg-primary/10' : 'border-border hover:bg-accent/50'
          }`}
        >
          <input {...getInputProps()} />
          <UploadCloud className="h-12 w-12 text-muted-foreground mb-4" />
          {isDragActive ? (
            <p className="text-sm text-foreground font-medium">Drop the DOCX file here ...</p>
          ) : (
            <div className="text-center">
              <p className="text-sm font-medium text-foreground">Drag & drop your DOCX file here</p>
              <p className="text-xs text-muted-foreground mt-1">or click to browse from your computer</p>
            </div>
          )}
        </div>

        {file && (
          <div className="flex items-center p-4 border rounded-md bg-accent/30">
            <File className="h-6 w-6 text-primary mr-3" />
            <div className="flex-1 overflow-hidden">
              <p className="text-sm font-medium truncate">{file.name}</p>
              <p className="text-xs text-muted-foreground">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
            </div>
            <Button variant="ghost" size="sm" onClick={() => setFile(null)}>
              Remove
            </Button>
          </div>
        )}

        <Button 
          className="w-full" 
          disabled={!file || !selectedRuleId || uploadMutation.isPending || validateMutation.isPending}
          onClick={handleProcess}
        >
          {uploadMutation.isPending || validateMutation.isPending ? 'Processing...' : 'Validate Document'}
        </Button>
      </CardContent>
    </Card>
  );
}
