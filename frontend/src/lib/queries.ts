import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from './api';

export const useRules = () => {
  return useQuery({
    queryKey: ['rules'],
    queryFn: api.getRules,
  });
};

export const useCreateRule = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.createRule,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['rules'] });
    },
  });
};

export const useUploadDocument = () => {
  return useMutation({
    mutationFn: api.uploadDocument,
  });
};

export const useValidateDocument = () => {
  return useMutation({
    mutationFn: (data: { documentId: string; ruleTemplateId: number }) =>
      api.validateDocument(data.documentId, data.ruleTemplateId),
  });
};

export const useReport = (reportId: string | null) => {
  return useQuery({
    queryKey: ['report', reportId],
    queryFn: () => api.getReport(reportId as string),
    enabled: !!reportId,
    refetchInterval: (query) => {
        // Poll every 2 seconds if status is VALIDATING
        const data = query.state?.data as any;
        if (data && data.status === 'VALIDATING') {
            return 2000;
        }
        return false;
    }
  });
};
